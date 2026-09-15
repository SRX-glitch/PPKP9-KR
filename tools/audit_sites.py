# -*- coding: utf-8 -*-
"""audit_sites.py -- session 45 full audit of every in-place byte the build wrote.

Motivation: the バンザイ freeze was caused by ONE worklist row (「はい」, 2 encoded
bytes) that `insert_extra.sites()` pattern-expanded onto 19 false sites in file
20 -- BNE opcodes, a u32 ID array, an asset table.  `MIN_MULTI_BYTES` now gates
that, but nothing ever audited the writes we ALREADY ship.  This tool does:

  For each dialogue file (4, 8, 18, 20, 25, 27, 30):
    diff pristine bytes vs the build's live copy (FAT-resolved, relocation-aware)
    over the file's PRISTINE extent (appended blobs/regions are new data, skipped),
    then score each changed chunk's ORIGINAL surroundings:
      * arm-code likeness  -- fraction of aligned words around the site whose
        condition nibble is 0xE / branch 0xEA-0xEB (real text scores ~0)
      * u32-table likeness -- fraction of aligned words that look like small
        integers / pointers (the 0x2A0F40 ID-array case)

  Verdict: chunks whose surroundings look like code or tables are printed with
  hex context for eyeballing.  A clean build prints nothing above the threshold.

Usage:  PYTHONIOENCODING=utf-8 python tools/audit_sites.py [build.nds]
"""
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAMEDIR = os.path.dirname(BASE)
ORIG = os.path.join(GAMEDIR, "Power Pro Kun Pocket 9 (Japan).nds")
BUILD = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    BASE, "builds", "PPKP9_kr_v215_haisites.nds")

FIDS = (4, 8, 18, 20, 25, 27, 30)


def fat_span(rom, fid):
    fat = int.from_bytes(rom[0x48:0x4C], "little")
    lo = int.from_bytes(rom[fat + fid * 8:fat + fid * 8 + 4], "little")
    hi = int.from_bytes(rom[fat + fid * 8 + 4:fat + fid * 8 + 8], "little")
    return lo, hi


def arm_likeness(buf, off, half=64):
    """Fraction of aligned words around `off` that decode like ARM code."""
    lo = max(0, (off - half) & ~3)
    hits = total = 0
    for a in range(lo, min(len(buf) - 4, off + half), 4):
        w = int.from_bytes(buf[a:a + 4], "little")
        cond = w >> 28
        op = (w >> 24) & 0xF
        total += 1
        if cond == 0xE or (cond < 0xF and op in (0xA, 0xB)):  # AL / B / BL
            hits += 1
    return hits / total if total else 0.0


def table_likeness(buf, off, half=32):
    """Fraction of aligned words that look like small ints or RAM pointers."""
    lo = max(0, (off - half) & ~3)
    hits = total = 0
    for a in range(lo, min(len(buf) - 4, off + half), 4):
        w = int.from_bytes(buf[a:a + 4], "little")
        total += 1
        if w < 0x10000 or 0x02000000 <= w < 0x02400000:
            hits += 1
    return hits / total if total else 0.0


def main():
    orig = open(ORIG, "rb").read()
    build = open(BUILD, "rb").read()
    print(f"audit: {os.path.basename(BUILD)} vs pristine")
    total_chunks = total_bytes = flagged = 0
    for fid in FIDS:
        p_lo, p_hi = fat_span(orig, fid)
        l_lo, l_hi = fat_span(build, fid)
        size = p_hi - p_lo
        delta = l_lo - p_lo
        chunks = []
        i = 0
        po, lo = p_lo, l_lo
        while i < size:
            if orig[po + i] != build[lo + i]:
                j = i
                while j < size and orig[po + j] != build[lo + j]:
                    j += 1
                chunks.append((i, j - i))
                i = j
            else:
                i += 1
        nb = sum(c[1] for c in chunks)
        total_chunks += len(chunks)
        total_bytes += nb
        repointed = 0
        print(f"\nfile {fid:2d}: pristine 0x{p_lo:06X}+0x{size:X}, live delta "
              f"{'+' if delta >= 0 else ''}0x{delta:X}, {len(chunks)} chunks / {nb}B changed")
        for rel, ln in chunks:
            a = arm_likeness(orig, p_lo + rel)
            t = table_likeness(orig, p_lo + rel)
            if a >= 0.5 or t >= 0.75:
                o = p_lo + rel
                # A change whose every touched aligned u32 went pointer->pointer
                # is a sanctioned repoint (insert_file8 / insert_profiles /
                # tail regions carry their own read-back gates).  The 「はい」
                # class stomps NON-pointer bytes into such structures.
                w0 = (o & ~3)
                w1 = (o + ln + 3) & ~3
                ptr_ok = True
                for wa in range(w0, w1, 4):
                    ov = int.from_bytes(orig[wa:wa + 4], "little")
                    nv = int.from_bytes(build[wa + delta:wa + delta + 4], "little")
                    if ov == nv:
                        continue
                    if not (0x02000000 <= ov < 0x02400000
                            and 0x02000000 <= nv < 0x02400000):
                        ptr_ok = False
                        break
                if t >= 0.75 and ptr_ok:
                    repointed += 1
                    continue
                flagged += 1
                print(f"  ⛔ SUSPECT 0x{o:06X} len={ln:3d} arm={a:.2f} tbl={t:.2f}")
                print(f"     orig : {orig[o-12:o+ln+12].hex()}")
                print(f"     build: {build[o-12+delta:o+ln+12+delta].hex()}")
        if repointed:
            print(f"  (pointer->pointer rewrites, sanctioned: {repointed})")
    print(f"\ntotal: {total_chunks} chunks / {total_bytes}B changed in place, "
          f"{flagged} flagged as code/table-like")
    if not flagged:
        print("CLEAN -- no in-place write sits in code- or table-looking bytes")


if __name__ == "__main__":
    main()
