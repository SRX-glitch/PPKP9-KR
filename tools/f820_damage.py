#!/usr/bin/env python3
"""Did the F8 20 desync rows actually overwrite opcode bytes in a built ROM?

f820_impact.py finds worklist rows whose offset lands on the SUBCODE byte of a
live `F8 1x xx` marker (signature: pristine ROM[off-3:off] == F8 20 F8).  This
checks the consequence: compare the built ROM against the pristine one at those
offsets.  A difference there means the build changed an opcode's subcode --
control-flow damage that the string-level gates cannot see, and that the
`opcode gate` misses because it walks with the same wrong width table.

Usage:
    python3 f820_damage.py <built.nds>
"""
import os, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(HERE, "..", ".."))
ORIG = os.path.join(GAME, "Power Pro Kun Pocket 9 (Japan).nds")
WORK = os.path.join(HERE, "..", "survey", "common")

built_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(GAME, "ppkp9-kr", "builds", "PPKP9_pathcheck.nds")
orig = open(ORIG, "rb").read()
built = open(built_path, "rb").read()
print(f"built {os.path.basename(built_path)}  same size as pristine: {len(orig) == len(built)}\n")

rows = []
for p in sorted(glob.glob(os.path.join(WORK, "file*_extra.tsv"))):
    with open(p, encoding="utf-8") as fh:
        h = fh.readline().rstrip("\n").split("\t")
        io, ij = h.index("offset"), h.index("jp")
        for ln in fh:
            f = ln.rstrip("\n").split("\t")
            if len(f) <= ij:
                continue
            try:
                off = int(f[io], 16)
            except ValueError:
                continue
            if off >= 3 and orig[off - 3:off] == b"\xf8\x20\xf8":
                rows.append((os.path.basename(p), off, f[ij][:16]))

changed = 0
for name, off, jp in rows:
    a, b = orig[off - 1:off + 4], built[off - 1:off + 4]
    tag = "CHANGED" if a != b else "same"
    changed += a != b
    print(f"{name:18} 0x{off:06X}  orig {a.hex()}  built {b.hex()}  {tag:8} {jp!r}")

print(f"\n{changed}/{len(rows)} desync sites have opcode bytes overwritten in the built ROM")
