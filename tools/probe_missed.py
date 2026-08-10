#!/usr/bin/env python3
"""Why did the corpus extractor miss 0x59681 (overlay-28 relative)?

Decodes a window of raw overlay-28 bytes and compares against the addresses the
survey recorded, so we can tell whether the region was skipped wholesale or the
line was dropped individually."""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

BASE = r"C:/Users/jngji/Desktop/실험실"
OV28 = (0x04CC000, 0x055EE40)
rom = open(f"{BASE}/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds", "rb").read()
ov = rom[OV28[0]:OV28[1]]

target = 0x525681 - OV28[0]   # 0x59681
print(f"target overlay offset: {target:#x}  (ov28 size {len(ov):#x})\n")

recorded = []
for ln in open(f"{BASE}/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/ov28/dialogue_lines.tsv", encoding="utf-8").read().splitlines():
    p = ln.split("\t")
    if len(p) >= 4:
        recorded.append((int(p[0], 16), p[3]))
recorded.sort()
addrs = [a for a, _ in recorded]
print(f"corpus entries: {len(recorded)}, address range {addrs[0]:#x}..{addrs[-1]:#x}")

import bisect
i = bisect.bisect_left(addrs, target)
print("\nnearest recorded entries around the target:")
for a, t in recorded[max(0, i - 4):i + 4]:
    mark = "  <-- target sits here" if a > target else ""
    print(f"  {a:#08x}  {t}{mark}")

print(f"\nraw bytes {target-0x40:#x}..{target+0x40:#x}:")
win = ov[target - 0x40:target + 0x40]
print("  " + win.hex())

# decode the window the way the survey's scanner would, byte by byte
print("\nbyte-wise decode of the window (op bytes >= 0xF8 shown as [XX]):")
out, k = [], 0
while k < len(win):
    b = win[k]
    if b >= 0xF8:
        out.append(f"[{b:02X}]")
        k += 1
        continue
    cc, n = P.bytes_to_cc(win, k)
    ch = P.CC2CH.get(cc)
    out.append(ch if ch else f"<{cc}>")
    k += n
print("  " + "".join(out))
