#!/usr/bin/env python3
"""Is there contiguous free space in ARM9 for an MTE expansion hook?

Glyph storage is interleaved 16-charcodes-per-576-bytes, so a 576-byte region is
contiguous free space only if ALL 16 of its charcodes are unused. Find those
aligned groups.
"""
import os, sys, json, collections
sys.path.insert(0, os.path.dirname(__file__))
import fontcodec as F

SURVEY = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font"
ROM = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
rom = open(ROM, "rb").read()
tbl = F.load_table(rom)
slots = set(json.load(open(os.path.join(SURVEY, "usable_slots.json"))))
print(f"usable (unused, safe) charcodes: {len(slots)}")

# a 576-byte region covers charcodes [base, base+16) where base % 16 == 0
regions = []
for base in range(0, 4352, 16):
    if all(c in slots for c in range(base, base + 16)):
        block = base // 64
        sub = (base % 64) // 16
        ram = tbl[block] + sub * 576
        regions.append((base, ram))

print(f"fully-free 576-byte regions: {len(regions)}  "
      f"= {len(regions)*576} bytes ({len(regions)*576/1024:.1f} KB)")

# merge into contiguous RAM runs
regions.sort(key=lambda r: r[1])
runs = []
cur = [regions[0][1], regions[0][1] + 576, [regions[0][0]]] if regions else None
for base, ram in regions[1:]:
    if ram == cur[1]:
        cur[1] += 576
        cur[2].append(base)
    else:
        runs.append(cur)
        cur = [ram, ram + 576, [base]]
if cur:
    runs.append(cur)
runs.sort(key=lambda r: -(r[1] - r[0]))
print(f"\ncontiguous RAM runs: {len(runs)}")
for s, e, bases in runs[:10]:
    print(f"  RAM 0x{s:08X}-0x{e:08X}  {e-s:5d} bytes  "
          f"(ROM 0x{F.ram2rom(s):06X})  charcodes {bases[0]:#06x}..{bases[-1]+15:#06x}")

big = runs[0][1] - runs[0][0] if runs else 0
print(f"\nlargest contiguous free chunk: {big} bytes")
print(f"verdict: {'ENOUGH for an MTE expander hook (needs ~200-500 B)' if big >= 512 else 'too small - would need chaining'}")

# how many slots remain for glyphs if we spend the largest run on code?
spent = len(runs[0][2]) * 16 if runs else 0
print(f"cost: {spent} charcode slots -> {len(slots) - spent} left for Hangul glyphs")
