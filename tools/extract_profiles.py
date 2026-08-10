#!/usr/bin/env python3
"""Extract file 30's pointered RECORDS whole -- profile text, album titles.

The character-encyclopedia ("プロフィール") descriptions ship in Japanese because no
tool ever read them correctly. The record is:

    line1  FA  line2  FA  line3  FA  line4  FF

`FA` is a ONE-byte newline opcode, and the whole thing is a single record ended by
`FF`. Two earlier readings both got it wrong:
  * `insert_pointered._decode` reads a 32-byte window and skips 0x00 -- it has no
    idea about FA, so it decodes 0xFA as a charcode and produces junk.
  * `extract_pointered.decode` stops at the first byte >= 0xF8, so it saw only
    line 1 and reported 117 "strings" that are really 117 first lines.

Reading the record whole is also what makes translating it worth doing: the
pointer can be moved, so the Korean may be **any length** -- unlike everything in
the inline-only shared files.

Lines are joined with a literal \\n in the worklist so one row = one record.

    python tools/extract_profiles.py      -> survey/common/file30_profiles.tsv
"""
import os, sys, glob, argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P

BASE = r"C:/Users/jngji/Desktop/실험실"
ORIG = BASE + r"/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
COMMON = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/common"
ARRAYS = [(0x32E1FC, 101), (0x32ECEC, 483)]
NEWLINE = 0xFA
END = 0xFF
MAXREC = 512


def u32(rom, o):
    return int.from_bytes(rom[o:o + 4], "little")


def overlay_ram(rom, fid):
    ovt, n = u32(rom, 0x50), u32(rom, 0x54) // 32
    for i in range(n):
        e = ovt + i * 32
        if u32(rom, e + 24) == fid:
            return u32(rom, e + 4)
    return None


def read_record(rom, off):
    """(text with \\n for FA, byte length) or None if this is not a text record."""
    out, i, junk = [], off, 0
    while i < off + MAXREC:
        b = rom[i]
        if b == END:
            i += 1
            break
        if b == NEWLINE:
            out.append("\n")
            i += 1
            continue
        if b == 0:
            out.append("\x00")          # kept so the record round-trips exactly
            i += 1
            continue
        if b >= 0xF8:                   # any other opcode: not plain text
            return None
        cc, nxt = P.bytes_to_cc(rom, i)
        ch = P.CC2CH.get(cc)
        if ch is None:
            return None
        out.append(ch)
        i = nxt
    t = "".join(out)
    return (t, i - off) if t.strip("\x00\n") else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", type=int, default=0)
    a = ap.parse_args()
    rom = open(ORIG, "rb").read()
    fat = u32(rom, 0x48)
    lo = u32(rom, fat + 30 * 8)
    ram = overlay_ram(rom, 30)

    seen, rows = set(), []
    for base, cnt in ARRAYS:
        for k in range(cnt):
            v = u32(rom, base + k * 4)
            off = lo + (v - ram)
            if not (lo <= off < lo + 0x40000):
                continue
            r = read_record(rom, off)
            if not r:
                continue
            t, blen = r
            jp = sum(1 for c in t
                     if 0x3040 <= ord(c) <= 0x30FF or 0x4E00 <= ord(c) <= 0x9FFF)
            if jp < 2 or t in seen:
                continue
            seen.add(t)
            rows.append((off, blen, base, k, t))

    path = os.path.join(COMMON, "file30_profiles.tsv")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("offset\tbytes\tarray\tindex\tjp\tko\n")
        for off, blen, base, k, t in rows:
            f.write(f"0x{off:06X}\t{blen}\t0x{base:06X}\t{k}\t"
                    f"{t.replace(chr(10), '\\n').replace(chr(0), '\\0')}\t\n")
    print(f"pointered records with text: {len(rows)}")
    print(f"wrote {path}   (pointer path -> LENGTH IS FREE)")
    for off, blen, base, k, t in rows[:a.list or 6]:
        print(f"  0x{off:06X} {blen:3d}B  {t.replace(chr(10), ' / ')[:70]}")


if __name__ == "__main__":
    main()
