#!/usr/bin/env python3
"""Measure how far the wrong F8 20 width propagated into the worklists.

F8 20 takes no immediate (it scans forward to `F8 21 21`), but the length table
calls it 3.  A walker using 3 therefore swallows the F8 of the NEXT opcode and
resumes one byte late, so the run it records starts inside that opcode's
operand.  The signature is exact and checkable against the pristine ROM:

    ROM[off-3:off] == F8 20 F8      -> this row starts one byte too late

Such a row is not merely mistranslated: writing Korean at `off` overwrites the
tail of a real opcode, which is control-flow damage no string gate can see.

Usage:
    python3 f820_impact.py [--rom <path>]
"""
import os, sys, glob, collections

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(HERE, "..", ".."))
ROM = os.path.join(BASE, "Power Pro Kun Pocket 9 (Japan).nds")
WORK = os.path.join(HERE, "..", "survey", "common")

if "--rom" in sys.argv:
    ROM = sys.argv[sys.argv.index("--rom") + 1]

rom = open(ROM, "rb").read()
print(f"rom {os.path.basename(ROM)} {len(rom):,} bytes\n")

print(f"{'file':22} {'rows':>6} {'F820-intro':>10} {'desync':>7}  sample")
grand = collections.Counter()
for p in sorted(glob.glob(os.path.join(WORK, "file*_extra.tsv"))):
    rows = 0
    intro = 0
    desync = []
    with open(p, encoding="utf-8") as fh:
        head = fh.readline().rstrip("\n").split("\t")
        try:
            i_off, i_op, i_jp = head.index("offset"), head.index("opcode"), head.index("jp")
        except ValueError:
            print(f"{os.path.basename(p):22} (unexpected header)")
            continue
        for ln in fh:
            f = ln.rstrip("\n").split("\t")
            if len(f) <= max(i_off, i_op, i_jp):
                continue
            rows += 1
            if f[i_op].upper() in ("F820", "F8 20"):
                intro += 1
            try:
                off = int(f[i_off], 16)
            except ValueError:
                continue
            if off >= 3 and rom[off - 3:off] == b"\xf8\x20\xf8":
                desync.append((f[i_off], f[i_jp][:14]))
    grand["rows"] += rows
    grand["intro"] += intro
    grand["desync"] += len(desync)
    s = f"{desync[0][0]} {desync[0][1]!r}" if desync else ""
    print(f"{os.path.basename(p):22} {rows:>6} {intro:>10} {len(desync):>7}  {s}")

print(f"\ntotal rows {grand['rows']:,} · introduced by F8 20 {grand['intro']:,} "
      f"· one byte late {grand['desync']:,}")

# how common is the opcode at all?
n = rom.count(b"\xf8\x20")
n2 = rom.count(b"\xf8\x21\x21")
print(f"\nROM-wide: 'F8 20' appears {n:,} times, 'F8 21 21' (its jump target) {n2:,} times")
