#!/usr/bin/env python3
"""Enumerate every CONTAINER that holds on-screen text, and its translation state.

Why this exists
---------------
Session 30 kept reporting "only N strings are untranslated" and kept being wrong,
because every count was anchored on `F8 6B` -- the dialogue message opener. That
one anchor is a small slice of the text in this ROM. The ability panel is opened
by `f8 08`, choice options by `F8 15`/`F8 F8`, the album by an `No` header, the
tables by an `FF` terminator, the intro by nothing at all (absolute offsets). Each
miss surfaced only when the user photographed it.

So: do not guess the anchors, DERIVE them. Walk the ROM, and every time a
decodable text run begins, record the two bytes immediately before it. Group by
that prefix. The result is the list of containers, ranked by how much text each
holds -- including ones nobody has thought of yet.

    python tools/audit_containers.py              # the container table
    python tools/audit_containers.py --anchor f808 --list 40
"""
import os, sys, glob, argparse, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P

BASE = r"C:/Users/jngji/Desktop/실험실"
ORIG = BASE + r"/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
PROJ = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr"
MIN_CHARS = 3
# ⚠ Restrict to the files that actually hold script. Without this the scan reports
# 2.25 MILLION "runs" -- a 64 MB ROM of graphics and audio decodes to plausible
# kana, and file 2029 alone (a bulk asset file) contributes a third of it. These
# eight are every file this project has ever found real text in.
SCRIPT_FILES = {4, 8, 13, 18, 20, 25, 27, 30}
JP_DENSITY = 0.7


def is_jp(ch):
    o = ord(ch)
    if o in (0x30FB, 0x30FC):          # ・ ー are shared with Korean
        return False
    return 0x3040 <= o <= 0x30FF or 0x4E00 <= o <= 0x9FFF


def translated_set():
    """Every Japanese string any worklist has a Korean for, all worklist shapes."""
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


def fat(rom):
    base = int.from_bytes(rom[0x48:0x4C], "little")
    n = int.from_bytes(rom[0x4C:0x50], "little") // 8
    out = []
    for i in range(n):
        s = int.from_bytes(rom[base + i * 8:base + i * 8 + 4], "little")
        e = int.from_bytes(rom[base + i * 8 + 4:base + i * 8 + 8], "little")
        if 0 < s < e <= len(rom):
            out.append((s, e, i))
    return sorted(out)


def scan(rom):
    """Yield (prefix2, offset, text) for every decodable run of MIN_CHARS+ chars.

    The prefix is the two bytes before the run -- that is the container's
    signature. A run is only reported when at least half its characters are
    Japanese, which keeps binary data (graphics, audio, pointer tables) out: those
    decode to scattered kana and would otherwise swamp everything.
    """
    i, n = 0, len(rom)
    while i < n - 1:
        b = rom[i]
        if b == 0 or b >= 0xF8:
            i += 1
            continue
        st, chars = i, []
        while i < n - 1:
            c = rom[i]
            if c == 0 or c >= 0xF8:
                break
            cc, nxt = P.bytes_to_cc(rom, i)
            ch = P.CC2CH.get(cc)
            if ch is None:
                break
            chars.append(ch)
            i = nxt
        if len(chars) >= MIN_CHARS:
            t = "".join(chars)
            jp = sum(1 for c in t if is_jp(c))
            if jp >= 2 and jp / len(t) >= JP_DENSITY:
                yield rom[max(0, st - 2):st].hex(), st, t
        if i == st:
            i += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--anchor")
    ap.add_argument("--list", type=int, default=0)
    a = ap.parse_args()

    rom = open(ORIG, "rb").read()
    tr = translated_set()
    files = fat(rom)

    def owner(o):
        for s, e, i in files:
            if s <= o < e:
                return i
        return -1

    per = collections.defaultdict(lambda: {"n": 0, "new": 0, "distinct": set(),
                                           "files": collections.Counter(),
                                           "samples": []})
    for pre, off, t in scan(rom):
        if owner(off) not in SCRIPT_FILES:
            continue
        d = per[pre]
        d["n"] += 1
        d["distinct"].add(t)
        d["files"][owner(off)] += 1
        if t not in tr:
            d["new"] += 1
            if len(d["samples"]) < 60:
                d["samples"].append((off, t))

    if a.anchor:
        d = per.get(a.anchor)
        if not d:
            print(f"no runs with prefix {a.anchor}")
            return
        print(f"anchor {a.anchor}: {d['n']} runs, {d['new']} untranslated, "
              f"files {dict(d['files'].most_common(6))}")
        for off, t in d["samples"][:a.list or 30]:
            print(f"  0x{off:06X}  {t}")
        return

    rows = sorted(per.items(), key=lambda kv: -kv[1]["new"])
    print(f"{'prefix':>8}  {'runs':>6} {'untrans':>8} {'distinct':>8}   files")
    tot = totnew = 0
    for pre, d in rows[:26]:
        tot += d["n"]
        totnew += d["new"]
        print(f"{pre:>8}  {d['n']:6d} {d['new']:8d} {len(d['distinct']):8d}   "
              f"{dict(d['files'].most_common(4))}")
    print(f"\nshown: {tot} runs, {totnew} untranslated")
    print(f"all prefixes: {sum(d['n'] for _, d in rows)} runs, "
          f"{sum(d['new'] for _, d in rows)} untranslated, "
          f"{len(rows)} distinct prefixes")


if __name__ == "__main__":
    main()
