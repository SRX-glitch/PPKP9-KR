#!/usr/bin/env python3
"""Locate an arbitrary Japanese line's encoded bytes in the ROM images, to tell
whether it lives in overlay 28 (our corpus) or somewhere we never surveyed."""
import os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

BASE = r"C:/Users/jngji/Desktop/실험실"
ROMS = {
    "orig": f"{BASE}/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds",
    "kr":   f"{BASE}/rom/DS/파워프로군 포켓9/ppkp9-kr/builds/PPKP9_kr.nds",
}
# overlay 28 in the original image (from build_kr output)
OV28_ORIG = (0x04CC000, 0x055EE40)

for s in sys.argv[1:]:
    ccs = [P.CH2CC.get(c) for c in s]
    if any(c is None for c in ccs):
        miss = [c for c, cc in zip(s, ccs) if cc is None]
        print(f"{s!r}: unencodable chars {miss}")
        continue
    b = b"".join(P.cc_to_bytes(c) for c in ccs)
    print(f"\n{s!r}  -> {b.hex()}")
    for tag, path in ROMS.items():
        rom = open(path, "rb").read()
        hits = [m.start() for m in re.finditer(re.escape(b), rom)]
        where = ""
        if tag == "orig":
            where = " ".join(
                "OV28" if OV28_ORIG[0] <= h < OV28_ORIG[1] else "elsewhere"
                for h in hits[:8])
        print(f"  {tag}: {len(hits)} hit(s) {[hex(h) for h in hits[:8]]} {where}")
