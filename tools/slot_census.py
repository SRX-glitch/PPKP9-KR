#!/usr/bin/env python3
"""Which font charcodes does the game's text actually use?

charcode <-> PokeTEXT encoding:
  1-byte  0x01..0xE7          -> charcode = b - 1            (0..230)
  2-byte  0xE8..0xF7, b2      -> charcode = 256 + (b1-232)*256 + b2   (256..4351)
Total 4352 = 68 blocks x 64. Font table confirms the mapping.
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
import fontcodec as F

ROM = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
rom = open(ROM, "rb").read()
tbl = F.load_table(rom)

# --- 1. font-table aliasing: blocks sharing a pointer are filler ---
byptr = collections.defaultdict(list)
for i, p in enumerate(tbl):
    byptr[p].append(i)
alias = {p: b for p, b in byptr.items() if len(b) > 1}
print("aliased pointers (filler blocks):")
for p, b in sorted(alias.items()):
    print(f"  {p:08X} -> blocks {b}")
alias_blocks = sorted(b for bl in alias.values() for b in bl[1:])
print("filler blocks (dupes of an earlier block):", alias_blocks,
      f"= {len(alias_blocks)*64} charcodes")

# --- 2. duplicate glyph bitmaps across the whole font ---
bitmaps = {}
dupe_of = {}
for b in range(F.NBLOCK):
    region = F.block_region(rom, tbl, b)
    for w in range(64):
        cc = b * 64 + w
        key = bytes(v for row in F.decode_glyph(region, cc) for v in row)
        if key in bitmaps:
            dupe_of[cc] = bitmaps[key]
        else:
            bitmaps[key] = cc
print(f"\nunique glyph bitmaps: {len(bitmaps)} / 4352   duplicates: {len(dupe_of)}")

# --- 3. usage census over the whole ROM text ---
used = collections.Counter()
n = len(rom)
i = 0
runs = 0
while i < n - 1:
    b = rom[i]
    if 1 <= b <= 231:
        # try to read a plausible run
        j = i
        seq = []
        while j < n:
            c = rom[j]
            if c == 0:
                break
            if 1 <= c <= 231:
                seq.append(c - 1); j += 1
            elif 232 <= c <= 247:
                seq.append(256 + (c - 232) * 256 + rom[j + 1]); j += 2
            else:
                break
        if len(seq) >= 6:            # only count confident text runs
            runs += 1
            used.update(seq)
            i = j
            continue
    i += 1
print(f"text runs counted: {runs}, distinct charcodes used: {len(used)}")

allcc = set(range(4352))
unused = sorted(allcc - set(used))
print(f"charcodes NEVER used in ROM text: {len(unused)}")

# how many of those have a *unique* bitmap (i.e. a real distinct glyph we'd overwrite)
uniq_unused = [cc for cc in unused if cc not in dupe_of]
print(f"  of which unique-bitmap: {len(uniq_unused)}")

# contiguous runs of unused charcodes (nice for allocation)
def runs_of(lst):
    out = []
    s = p = lst[0]
    for x in lst[1:]:
        if x == p + 1:
            p = x; continue
        out.append((s, p)); s = p = x
    out.append((s, p))
    return out

r = runs_of(unused)
r.sort(key=lambda t: -(t[1] - t[0]))
print("\nlargest contiguous unused ranges (start, end, len):")
for s, e in r[:25]:
    print(f"  0x{s:04X}-0x{e:04X}  {e-s+1}")
print(f"total ranges: {len(r)}")

with open(r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font/unused_charcodes.txt", "w") as f:
    f.write("\n".join(f"{cc:04X}" for cc in unused))
print("wrote unused_charcodes.txt")
