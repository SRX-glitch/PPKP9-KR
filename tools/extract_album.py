#!/usr/bin/env python3
"""Extract file 30's `No`-header album records at the TITLE offset.

The Success album ("デモ絵") and the profile album share one record shape:

    f7 68 f7 8c  00  f7 52 f7 51  00 00 00 00  d3  <title>  ff
    `--- "No" ---'     `- number -'                 「

Two traps live in that layout and both have already cost this project:

  * The pointer array 0x32E1FC points at the RECORD START, not at the title. A
    decoder that starts there reads 「No」, hits the 0x00, and gives up -- which is
    why `extract_pointered.py` reported 117 strings and none of the album titles.
  * The old extractor locked on two bytes LATE, inside `f7 52`'s operand, which is
    where 「エ「心の旅」」 and friends got their nonsense prefixes -- and writing at
    that offset wrecked the entry.

So: walk the record properly, and emit the offset of the title itself with the
budget running to the FF terminator. That is the shape `insert_tables` consumes,
and its `verify_offset` re-encodes the Japanese as a second check.

    python tools/extract_album.py      -> survey/common/file30_album_records.tsv
"""
import os, sys, glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P

BASE = r"C:/Users/jngji/Desktop/실험실"
ORIG = BASE + r"/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
COMMON = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/common"
TRANS = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/translation"
HEADER = bytes([0xF7, 0x68, 0xF7, 0x8C])
LO, HI = 0x320000, 0x333000
MAXREC = 160


def known():
    out = set()
    for fn in sorted(glob.glob(os.path.join(TRANS, "*.tsv"))):
        if os.path.basename(fn).startswith("worksheet"):
            continue
        for ln in open(fn, encoding="utf-8").read().splitlines()[1:]:
            p = ln.split("\t")
            if len(p) >= 2 and p[-1].strip():
                out.add(p[1] if p[0].startswith("0x") and len(p) >= 3 else p[0])
    for fn in sorted(glob.glob(os.path.join(COMMON, "*.tsv"))):
        for ln in open(fn, encoding="utf-8").read().splitlines()[1:]:
            p = ln.split("\t")
            if len(p) >= 4 and p[3].strip():
                out.add(p[2])
            if len(p) >= 6 and p[5].strip():
                out.add(p[4])
    return out


def decode(rom, o, limit):
    s, i = [], o
    while i < limit:
        b = rom[i]
        if b == 0 or b >= 0xF8:
            break
        cc, nxt = P.bytes_to_cc(rom, i)
        ch = P.CC2CH.get(cc)
        if ch is None:
            break
        s.append(ch)
        i = nxt
    return "".join(s), i


def main():
    rom = open(ORIG, "rb").read()
    tr = known()
    rows, i = [], rom.find(HEADER, LO, HI)
    while i >= 0:
        end = rom.find(b"\xff", i, i + MAXREC)
        if end > 0:
            # the title is the LAST decodable run before the terminator; walk
            # forward skipping zeros and F7/F8 opcodes until something decodes
            j, best = i + 4, None
            while j < end:
                if rom[j] == 0:
                    j += 1
                    continue
                if rom[j] >= 0xF8:
                    j += 2
                    continue
                t, nxt = decode(rom, j, end)
                if len(t) >= 2 and any(0x3040 <= ord(c) <= 0x30FF
                                       or 0x4E00 <= ord(c) <= 0x9FFF for c in t):
                    best = (j, t, end - j)
                j = max(nxt, j + 1)
            if best and best[1] not in tr:
                rows.append(best)
        i = rom.find(HEADER, i + 1, HI)

    seen, out = set(), []
    for off, t, bud in rows:
        if t in seen:
            continue
        seen.add(t)
        out.append((off, bud, t))

    path = os.path.join(COMMON, "file30_album_records.tsv")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("n\toffset\toccurrences\tmax_syl\tjp\tko\n")
        for n, (off, bud, t) in enumerate(out, 1):
            f.write(f"{n}\t0x{off:06x}\t1\t\t{t}\t\n")
    print(f"album records with an untranslated title: {len(out)}")
    print(f"wrote {path}")
    for off, bud, t in out[:16]:
        print(f"   0x{off:06X} budget {bud:3d}  {t}")


if __name__ == "__main__":
    main()
