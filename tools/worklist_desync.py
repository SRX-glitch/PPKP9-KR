#!/usr/bin/env python3
"""Model-independent check: is each worklist offset a plausible run START?

f820_impact.py only catches desyncs caused by the one opcode we proved wrong.
This asks a question that does not depend on the width table at all:

    a text run can never begin on the byte right after an F8/F9 escape byte,
    because that byte is the opcode's SUBCODE.

So `pristine[off-1] in (F8, F9)` means the walker resumed one byte late --
whatever opcode misled it.  Writing Korean at such an offset changes the
subcode, i.e. turns one opcode into a different one.

ONE EXCEPTION, and it is the common case: `F8 F8`.  Subcodes only go up to
0x6F, so an F8 in the subcode slot is not a handler index -- it is a two-byte
token, and a run legitimately starts right after it.  Those rows are normal
(their Japanese reads cleanly), so `orig[off-2] == F8` is excluded.  Ignoring
this turns 578 "findings" into noise; the real count is far smaller.

Reported separately:
    subcode-start   off-1 is F8/F9            -> certain desync
    changed         the built ROM actually overwrote it

Usage:
    python3 worklist_desync.py [built.nds]
"""
import os, sys, glob, collections

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(HERE, "..", ".."))
ORIG = os.path.join(GAME, "Power Pro Kun Pocket 9 (Japan).nds")
WORK = os.path.join(HERE, "..", "survey", "common")

orig = open(ORIG, "rb").read()
built = open(sys.argv[1], "rb").read() if len(sys.argv) > 1 else None

print(f"{'file':22} {'rows':>6} {'subcode-start':>14} {'changed':>8}  by opcode before")
tot = collections.Counter()
allbad = []
for p in sorted(glob.glob(os.path.join(WORK, "file*_extra.tsv"))):
    rows = 0
    bad = []
    with open(p, encoding="utf-8") as fh:
        h = fh.readline().rstrip("\n").split("\t")
        io, ij = h.index("offset"), h.index("jp")
        ik = h.index("ko") if "ko" in h else None
        for ln in fh:
            f = ln.rstrip("\n").split("\t")
            if len(f) <= ij:
                continue
            rows += 1
            try:
                off = int(f[io], 16)
            except ValueError:
                continue
            if off >= 2 and orig[off - 1] in (0xF8, 0xF9) and orig[off - 2] != 0xF8:
                ko = f[ik] if ik is not None and len(f) > ik else ""
                ch = built is not None and orig[off:off + 3] != built[off:off + 3]
                bad.append((off, f[ij][:14], ko[:14], ch))
    kinds = collections.Counter()
    for off, _, _, _ in bad:
        # which opcode sits just before the mis-started run
        for back in range(2, 8):
            if off - back >= 0 and orig[off - back] == 0xF8:
                kinds[f"F8{orig[off-back+1]:02X}"] += 1
                break
    changed = sum(1 for b in bad if b[3])
    tot["rows"] += rows
    tot["bad"] += len(bad)
    tot["changed"] += changed
    allbad += [(os.path.basename(p),) + b for b in bad]
    top = " ".join(f"{k}x{v}" for k, v in kinds.most_common(4))
    print(f"{os.path.basename(p):22} {rows:>6} {len(bad):>14} {changed:>8}  {top}")

print(f"\ntotal rows {tot['rows']:,} · start on a subcode byte {tot['bad']:,} "
      f"· already overwritten in the build {tot['changed']:,}")
if allbad:
    print("\nsites whose bytes the build changed:")
    for name, off, jp, ko, ch in allbad:
        if ch:
            print(f"  {name:18} 0x{off:06X}  {orig[off-1:off+4].hex()} -> "
                  f"{built[off-1:off+4].hex()}  jp={jp!r} ko={ko!r}")
