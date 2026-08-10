#!/usr/bin/env python3
"""Dump every string reachable through a file's pointer arrays, with its state.

The character-encyclopedia ("プロフィール") descriptions render as Japanese even though
file 30's other text is translated, and the reason is simply that nobody extracted
them. They ARE reachable: array 0x32ECEC index 2 and 5 both point at
「どこからともなくやってきた、」.

That matters more than it sounds. A pointered string can be **rewritten to any
length** -- `insert_pointered` moves it into the overlay's grown tail and rewrites
the pointer -- so unlike the inline-only shared files, these translations do not
have to be squeezed. Anything this tool lists is translatable naturally.

    python tools/extract_pointered.py 30      -> survey/common/file30_ptr.tsv
"""
import os, sys, glob, argparse, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P

BASE = r"C:/Users/jngji/Desktop/실험실"
ORIG = BASE + r"/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
PROJ = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr"
OUT = PROJ + r"/survey/common"

# file id -> the pointer arrays insert_pointered already knows about
ARRAYS = {
    30: [(0x32E1FC, 101), (0x32ECEC, 483)],
    18: [(0x229644, 307)],
    13: [(0x13C778, 194)],
    4:  [(0x5707A8, 166)],
}


def u32(rom, o):
    return int.from_bytes(rom[o:o + 4], "little")


def overlay_ram(rom, fid):
    ovt, n = u32(rom, 0x50), u32(rom, 0x54) // 32
    for i in range(n):
        e = ovt + i * 32
        if u32(rom, e + 24) == fid:
            return u32(rom, e + 4)
    return None


# ⚠⚠ THIS DECODER DOES NOT MATCH insert_pointered._decode, AND THAT MATTERS.
# `_decode` reads a 32-BYTE window and SKIPS 0x00 bytes, so the "Japanese at a
# pointer target" it matches on can span several fields -- that is deliberate and
# required, because `file30_album.tsv` keys on strings like `No01「StaffRoll」` that
# are exactly such a span. This decoder stops at the first 0x00, so the keys the
# two produce disagree: wiring `file30_ptr.tsv` into insert_pointered matched only
# 4 of 117 rows.
#
# Do NOT "fix" it by widening this decoder until the record layout is known. Those
# 0x00 bytes look like FIELD SEPARATORS (the profile text is several lines), and
# repointing a whole 32-byte window to one Korean string would merge or drop lines.
# The next step is to read the layout in the emulator -- breakpoint the profile
# screen's text fetch and see how many fields it reads and where it stops.
def decode(rom, o, limit=400):
    s, i = [], o
    while i < o + limit:
        b = rom[i]
        if b == 0 or b >= 0xF8:
            break
        cc, nxt = P.bytes_to_cc(rom, i)
        ch = P.CC2CH.get(cc)
        if ch is None:
            break
        s.append(ch)
        i = nxt
    return "".join(s)


def translated():
    out = set()
    for fn in sorted(glob.glob(os.path.join(PROJ, "translation", "*.tsv"))):
        if os.path.basename(fn).startswith("worksheet"):
            continue
        for ln in open(fn, encoding="utf-8").read().splitlines()[1:]:
            p = ln.split("\t")
            if len(p) >= 2 and p[-1].strip():
                out.add(p[1] if p[0].startswith("0x") and len(p) >= 3 else p[0])
    for fn in sorted(glob.glob(os.path.join(OUT, "*.tsv"))):
        for ln in open(fn, encoding="utf-8").read().splitlines()[1:]:
            p = ln.split("\t")
            if len(p) >= 4 and p[3].strip():
                out.add(p[2])
            if len(p) >= 6 and p[5].strip():
                out.add(p[4])
            if len(p) == 2 and p[1].strip():
                out.add(p[0])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fid", type=int)
    a = ap.parse_args()

    rom = open(ORIG, "rb").read()
    tr = translated()
    fat = u32(rom, 0x48)
    lo = u32(rom, fat + a.fid * 8)
    ram = overlay_ram(rom, a.fid)

    seen, rows = {}, []
    for base, cnt in ARRAYS[a.fid]:
        for k in range(cnt):
            v = u32(rom, base + k * 4)
            off = lo + (v - ram)
            if not (lo <= off < lo + 0x200000):
                continue
            t = decode(rom, off)
            if len(t) < 2:
                continue
            seen.setdefault(t, []).append((base, k, off))

    for t, where in seen.items():
        jp = sum(1 for c in t
                 if 0x3040 <= ord(c) <= 0x30FF or 0x4E00 <= ord(c) <= 0x9FFF)
        if jp < 1:
            continue
        base, k, off = where[0]
        rows.append((off, len(where), t, t in tr))

    rows.sort(key=lambda r: (r[3], -r[1]))
    path = os.path.join(OUT, f"file{a.fid}_ptr.tsv")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("offset\tpointers\tjp\tko\n")
        for off, n, t, done in rows:
            if done:
                continue
            f.write(f"0x{off:06X}\t{n}\t{t}\t\n")
    todo = sum(1 for r in rows if not r[3])
    print(f"file {a.fid}: {len(rows)} pointered strings, {todo} untranslated")
    print(f"wrote {path}   (length is UNLIMITED here -- translate naturally)")


if __name__ == "__main__":
    main()
