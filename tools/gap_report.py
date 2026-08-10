#!/usr/bin/env python3
"""Split the still-Japanese text in a built ROM into the buckets that matter.

"N runs are still Japanese" is not actionable, because three completely different
problems hide inside it and each needs a different fix:

  known-over-budget : the line HAS Korean, it just does not fit and has no
                      redirect path. Fix = shorten, or give that path a redirect.
  never-extracted   : the Japanese is not in ANY worklist. Fix = extract it and
                      translate it. This is the only bucket that is real
                      "untranslated" work.
  not-text          : decodes to kana-ish noise -- pointer tables, ASCII asset
                      paths, binary records. Fix = nothing, and counting it
                      inflates every coverage number.

    python tools/gap_report.py [rom]
    python tools/gap_report.py [rom] --list 40      # dump the never-extracted
"""
import os, sys, glob, json, argparse, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P

BASE = r"C:/Users/jngji/Desktop/실험실"
DEFAULT_ROM = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/builds/PPKP9_mte.nds"
KR = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font/kr_map.json"
TRANS = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/translation"
COMMON = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/common"


def is_jp(ch):
    o = ord(ch)
    if o in (0x30FB, 0x30FC):          # ・ ー are shared punctuation
        return False
    return 0x3040 <= o <= 0x30FF or 0x4E00 <= o <= 0x9FFF


def known_japanese():
    """Every Japanese string any worklist already has a Korean for."""
    out = set()
    for fn in sorted(glob.glob(os.path.join(TRANS, "*.tsv"))):
        if os.path.basename(fn).startswith("worksheet"):
            continue
        for ln in open(fn, encoding="utf-8").read().splitlines()[1:]:
            p = ln.split("\t")
            if len(p) >= 2 and p[-1].strip():
                out.add(p[1] if p[0].startswith("0x") and len(p) >= 3 else p[0])
    for fn in sorted(glob.glob(os.path.join(COMMON, "file*_runs.tsv"))):
        for ln in open(fn, encoding="utf-8").read().splitlines()[1:]:
            p = ln.split("\t")
            if len(p) >= 4 and p[3].strip():
                out.add(p[2])
    for fn in sorted(glob.glob(os.path.join(COMMON, "*_table.tsv"))):
        for ln in open(fn, encoding="utf-8").read().splitlines()[1:]:
            p = ln.split("\t")
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


def owner(files, off):
    for s, e, i in files:
        if s <= off < e:
            return i
    return -1


def runs(rom):
    """(offset, text) for every `F8 6B` message run.

    ⚠ Anchoring on the message opener is what makes this meaningful. A naive walk
    that just decodes any byte < 0xF8 as a charcode treats the ROM's graphics and
    audio as text: it reported **2.4 million** "never-extracted strings" out of a
    64 MB file, because random bytes decode to plausible kana. The opener is a
    structural marker, so it only fires on real script.
    """
    i, n = 0, len(rom)
    while i < n - 3:
        if rom[i] == 0xF8 and rom[i + 1] == 0x6B:
            j, s = i + 3, []
            while j < n and rom[j] != 0 and rom[j] < 0xF8:
                b = rom[j]
                if 1 <= b <= 231:
                    s.append(P.CC2CH.get(b - 1, "�"))
                    j += 1
                else:
                    cc = 256 + (b - 232) * 256 + rom[j + 1]
                    s.append(P.CC2CH.get(cc, "�"))
                    j += 2
            yield i, "".join(s)
            i = j
        else:
            i += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rom", nargs="?", default=DEFAULT_ROM)
    ap.add_argument("--list", type=int, default=0)
    ap.add_argument("--file", type=int)
    a = ap.parse_args()

    rom = open(a.rom, "rb").read()
    known = known_japanese()
    files = fat(rom)

    buckets = collections.Counter()
    per_file = collections.defaultdict(lambda: collections.Counter())
    unknown = collections.Counter()
    unknown_where = {}

    for off, text in runs(rom):
        jp = sum(1 for c in text if is_jp(c))
        if jp < 2:
            continue
        # a run is "text" only if a decent share of it is Japanese; the binary
        # records decode to scattered kana and would otherwise dominate
        if jp / len(text) < 0.5:
            buckets["not-text"] += 1
            continue
        f = owner(files, off)
        if text in known:
            buckets["known-over-budget"] += 1
            per_file[f]["known"] += 1
        else:
            buckets["never-extracted"] += 1
            per_file[f]["new"] += 1
            unknown[text] += 1
            unknown_where.setdefault(text, (f, off))

    print(f"{os.path.basename(a.rom)}   still-Japanese runs by bucket:")
    for k in ("known-over-budget", "never-extracted", "not-text"):
        print(f"  {k:20s} {buckets[k]:6d}")
    print(f"\n  distinct never-extracted strings: {len(unknown)}")

    print("\n  by FAT file (never-extracted / known-over-budget):")
    for f in sorted(per_file, key=lambda x: -per_file[x]["new"])[:12]:
        print(f"    file {f:<6} new {per_file[f]['new']:5d}   known {per_file[f]['known']:5d}")

    if a.list:
        print(f"\n  top {a.list} never-extracted strings by occurrences:")
        for text, n in unknown.most_common(a.list):
            f, off = unknown_where[text]
            if a.file is not None and f != a.file:
                continue
            print(f"    x{n:<4} file{f:<5} 0x{off:06X}  {text}")


if __name__ == "__main__":
    main()
