#!/usr/bin/env python3
"""Static audit of what writing shared files 8 and 20 actually changes.

Session 29 bisected the 「終 / ファイルをけしました」 save-wipe to file 8 or 20 and left
both off, without pinning down which or why -- two more 25-minute boot cycles were
judged not worth it. This is the cheap analysis that was skipped: apply the same
patch offline and check every changed byte, the way the shipped files were checked
(file 4: 12,769 changed / 0 outside a run; file 27: 3,652 / 0 outside).

Being an overlay is NOT the distinguishing factor -- all four of 4/8/20/27 are
overlays with ARM code, so that hypothesis is dead.

    python tools/audit_file8.py
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract_common as EC
import insert_common as IC
import untranslated as U
import koenc


def runs_of(rom, lo, hi):
    """(start, end) of every `F8 6B` text run in [lo, hi), as insert_common walks."""
    out, i = [], lo
    while i < hi - 3:
        if rom[i] == 0xF8 and rom[i + 1] == 0x6B:
            j = i + 3
            while j < hi and rom[j] != 0 and rom[j] < 0xF8:
                j += 2 if rom[j] >= 0xE8 else 1
            out.append((i + 3, j))
            i = j
        else:
            i += 1
    return out


def main():
    orig = bytes(open(EC.ORIG, "rb").read())
    spans = {i: (s, e) for s, e, i in U.fat_files(orig)}
    enc = koenc.Encoder()

    for fid in (8, 20):
        rom = bytearray(orig)
        w, s = IC.patch_file(rom, fid, enc, spans)
        lo, hi = spans[fid]
        changed = [i for i in range(lo, hi) if orig[i] != rom[i]]
        rs = runs_of(orig, lo, hi)
        inside = 0
        outside = []
        for i in changed:
            if any(a <= i < b for a, b in rs):
                inside += 1
            else:
                outside.append(i)
        print(f"file {fid}: {w} runs written, {s} skipped")
        print(f"  FAT span 0x{lo:06X}-0x{hi:06X}   text runs found: {len(rs)}")
        print(f"  bytes changed: {len(changed)}   inside a run: {inside}   "
              f"OUTSIDE: {len(outside)}")
        if outside:
            print(f"    first outside offsets: "
                  f"{[hex(o) for o in outside[:12]]}")
        # what the changed regions used to be, for eyeballing
        if changed:
            a, b = min(changed), max(changed)
            print(f"  changed range spans 0x{a:06X}-0x{b:06X} "
                  f"({b - a + 1} bytes wide)")
        print()


if __name__ == "__main__":
    main()
