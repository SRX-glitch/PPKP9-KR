#!/usr/bin/env python3
"""Render every glyph in the ROM font using the exact codec."""
import os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
import fontcodec as F

ROM = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
OUT = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font"
PAL = {0: (255, 255, 255), 1: (150, 150, 150), 2: (0, 0, 0), 3: (255, 0, 0)}

rom = open(ROM, "rb").read()
tbl = F.load_table(rom)
os.makedirs(OUT, exist_ok=True)

CW, CH = 13, 13
COLS = 64
img = Image.new("RGB", (COLS * CW, F.NBLOCK * CH), (60, 60, 110))
p = img.load()
empty = []
for b in range(F.NBLOCK):
    region = F.block_region(rom, tbl, b)
    for w in range(64):
        cc = b * 64 + w
        g = F.decode_glyph(region, cc)
        if not any(any(r) for r in g):
            empty.append(cc)
        for r in range(12):
            for c in range(len(g[r])):
                p[w * CW + c, b * CH + r] = PAL[g[r][c]]
img.save(os.path.join(OUT, "font_all_v2.png"))
print("blocks:", F.NBLOCK, "glyphs:", F.NBLOCK * 64, "empty:", len(empty))

# zoomed first 4 blocks
z = 5
img.crop((0, 0, COLS * CW, 4 * CH)).resize((COLS * CW * z, 4 * CH * z), Image.NEAREST) \
   .save(os.path.join(OUT, "font_v2_blocks0-3.png"))
# a kanji block
img.crop((0, 8 * CH, COLS * CW, 12 * CH)).resize((COLS * CW * z, 4 * CH * z), Image.NEAREST) \
   .save(os.path.join(OUT, "font_v2_blocks8-11.png"))
print("wrote", OUT)

# empty-slot report per block (candidates for Hangul)
import collections
per = collections.Counter(cc // 64 for cc in empty)
print("blocks with empty slots:", sorted(per.items())[:80])
