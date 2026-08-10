#!/usr/bin/env python3
"""Walk ANY script file with the validated opcode table, the way extract_all.py
walks overlay 28 -- and report which opcode introduced each text run.

Why this had to be written
--------------------------
Every "how much is untranslated" number this session was wrong, three times, for
the same reason: the scanner walked BYTES instead of OPCODES. A byte walker
cannot know that `F8 29` carries a one-byte speaker id, so it drops the operand
into the text, splits one run into several, and then reports the fragments'
neighbouring bytes as if they were container signatures. That produced 2.4M,
then 891, then 121k "untranslated runs" -- all noise.

`survey/ov28/opcode_lengths.json` already holds 112 validated F8 subcode widths,
and `extract_all.py` already uses them correctly. It just only ever ran on overlay
28. The other script files (4, 8, 13, 18, 20, 27, 30) were only ever scanned by
`extract_common.py`, which anchors on `F8 6B` alone -- so the ability panel
(`F8 08`), the town map names and the action templates were never even looked at.

    python tools/walk_file.py 8            # runs by introducing opcode
    python tools/walk_file.py 8 --list 40  # the untranslated ones
    python tools/walk_file.py --all        # every script file, summary
"""
import os, sys, json, glob, argparse, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P

BASE = r"C:/Users/jngji/Desktop/실험실"
ORIG = BASE + r"/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
PROJ = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr"
L = json.load(open(PROJ + r"/survey/ov28/opcode_lengths.json"))
BARE = {int(k): v for k, v in L["bare"].items()}
F8 = {int(k): v for k, v in L["f8"].items() if v}
SCRIPT_FILES = [4, 8, 13, 18, 20, 25, 27, 30]


def is_jp(ch):
    o = ord(ch)
    if o in (0x30FB, 0x30FC):
        return False
    return 0x3040 <= o <= 0x30FF or 0x4E00 <= o <= 0x9FFF


# Characters that never appear in real dialogue but are everywhere in decoded
# binary. The walker desyncs the moment it starts inside a pointer table or a
# record array -- file 4's first "runs" are 「プ㎏あぃペ￥」 at the very start of the
# file -- and without this the report is inflated by thousands of them. Every one
# of these is a gaiji/unit glyph the script itself does not use.
JUNK = set("㎏㎞￥％＝◎★☆♂♀→←↑↓№㎡‰§¶†‡")


def looks_like_text(t):
    if any(c in JUNK for c in t):
        return False
    # An embedded ASCII asset path. Every one ends in ".bin", which decodes to
    # 「ツノホ」 -- `/FsBin/hakata/album/...` comes out as 「ぁどモだノホぁネチヒチヤチ…んツノホ」.
    # file 8 alone has 1,262 of them and they were the bulk of its "untranslated"
    # rows.
    if t.endswith("ツノホ"):
        return False
    # Kana tables: the font's own character list and similar arrays decode to
    # enormous repetitive runs (「ううううううええええええ…」, 985 bytes). Real dialogue is
    # neither that long nor that repetitive.
    if len(t) > 40 or len(set(t)) / len(t) < 0.35:
        return False
    jp = sum(1 for c in t if is_jp(c))
    return jp >= 2 and jp / len(t) >= 0.6


def translated():
    out = set()
    for fn in sorted(glob.glob(os.path.join(PROJ, "translation", "*.tsv"))):
        if os.path.basename(fn).startswith("worksheet"):
            continue
        for ln in open(fn, encoding="utf-8").read().splitlines()[1:]:
            p = ln.split("\t")
            if len(p) >= 2 and p[-1].strip():
                out.add(p[1] if p[0].startswith("0x") and len(p) >= 3 else p[0])
    for fn in sorted(glob.glob(os.path.join(PROJ, "survey", "common", "*.tsv"))):
        for ln in open(fn, encoding="utf-8").read().splitlines()[1:]:
            p = ln.split("\t")
            if len(p) >= 4 and p[3].strip():
                out.add(p[2])
            if len(p) >= 6 and p[5].strip():
                out.add(p[4])
    return out


def fat_span(rom, fid):
    base = int.from_bytes(rom[0x48:0x4C], "little")
    s = int.from_bytes(rom[base + fid * 8:base + fid * 8 + 4], "little")
    e = int.from_bytes(rom[base + fid * 8 + 4:base + fid * 8 + 8], "little")
    return s, e


def walk(rom, lo, hi):
    """Yield (opcode_tag, offset, byte_len, text).

    The opcode tag is the LAST opcode seen before the run -- with the widths
    honoured, so it is the real introducer rather than whatever byte happened to
    sit two positions back.
    """
    i, last = lo, "-"
    while i < hi - 1:
        b = rom[i]
        if b == 0:
            i += 1
            continue
        if b >= 0xF8:
            if b == 0xF8:
                sub = rom[i + 1]
                last = f"F8{sub:02X}"
                i += F8.get(sub, 2)
            else:
                last = f"{b:02X}"
                i += BARE.get(b, 1)
            continue
        st, chars = i, []
        while i < hi:
            c = rom[i]
            if c == 0 or c >= 0xF8:
                break
            cc, nxt = P.bytes_to_cc(rom, i)
            ch = P.CC2CH.get(cc)
            if ch is None:
                break
            chars.append(ch)
            i = nxt
        if chars:
            t = "".join(chars)
            if len(t) >= 2 and looks_like_text(t):
                yield last, st, i - st, t
        if i == st:
            i += 1


def report(rom, tr, fid, listn=0, only=None):
    lo, hi = fat_span(rom, fid)
    per = collections.defaultdict(lambda: {"n": 0, "new": 0, "s": []})
    for tag, off, blen, t in walk(rom, lo, hi):
        d = per[tag]
        d["n"] += 1
        if t not in tr:
            d["new"] += 1
            if len(d["s"]) < 400:
                d["s"].append((off, blen, t))
    tot = sum(d["n"] for d in per.values())
    new = sum(d["new"] for d in per.values())
    print(f"file {fid}: {tot} text runs, {new} untranslated, "
          f"{len(per)} introducing opcodes")
    for tag, d in sorted(per.items(), key=lambda kv: -kv[1]["new"])[:10]:
        if d["new"] == 0:
            continue
        print(f"    {tag:>6}  runs {d['n']:5d}  untranslated {d['new']:5d}")
        if listn and (only is None or only == tag):
            for off, blen, t in d["s"][:listn]:
                print(f"        0x{off:06X} b{blen:<3d} {t}")
    return tot, new


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fid", nargs="?", type=int)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--list", type=int, default=0)
    ap.add_argument("--op")
    a = ap.parse_args()

    rom = open(ORIG, "rb").read()
    tr = translated()
    ids = SCRIPT_FILES if a.all else [a.fid]
    T = N = 0
    for fid in ids:
        t, n = report(rom, tr, fid, a.list, a.op)
        T += t
        N += n
        print()
    print(f"TOTAL {T} runs, {N} untranslated")


if __name__ == "__main__":
    main()
