#!/usr/bin/env python3
"""Dump a window of overlay 28 with hex + PokeTEXT decode side by side."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

OUT = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/ov28"
ov = open(os.path.join(OUT, "ov28.bin"), "rb").read()

# known dialogue lines, as overlay offsets (ROM offset - 0x4CC000)
SPOTS = {
    0x82339: "だから諦めるしかないって言ってるだろ。",
    0x9218D: "よくわからないけど、やってみようか。",
    0x023FC: "何もする気になれないなあ",
}


def dec_run(i, limit=200):
    s = []
    while i < len(ov) and len(s) < limit:
        if ov[i] == 0:
            break
        cc, j = P.bytes_to_cc(ov, i)
        if cc is None or cc not in P.CC2CH:
            break
        s.append(P.CC2CH[cc])
        i = j
    return "".join(s), i


for off, label in SPOTS.items():
    print(f"\n{'='*78}\n@0x{off:06X}  (RAM 0x{0x021C0DC0+off:08X})  expect: {label}\n{'='*78}")
    lo = off - 0x60
    hi = off + 0x80
    for row in range(lo, hi, 16):
        hexs = ov[row:row + 16].hex(" ")
        mark = " <<<" if row <= off < row + 16 else ""
        print(f"  {row:06X}  {hexs}{mark}")
    # decode forward from a few candidate starts
    print("  -- decoded runs in this window --")
    i = lo
    while i < hi:
        if 1 <= ov[i] <= 247 and (i == 0 or ov[i - 1] == 0 or ov[i - 1] in (0xF8, 0xFD, 0xFE, 0xFC)):
            s, j = dec_run(i)
            if len(s) >= 4:
                print(f"    0x{i:06X} (prev {ov[i-1]:02X}) len={j-i:3d}  {s}")
                i = j + 1
                continue
        i += 1
