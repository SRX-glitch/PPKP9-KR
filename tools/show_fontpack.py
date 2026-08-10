#!/usr/bin/env python3
"""Render the injected Korean font pack straight out of the patched ROM.

Reads the glyphs back the way the game will, which means two sources now: the
ARM9 font blocks for ordinary slots, and the extension pages at the front of the
grown overlay for the alias-block charcodes the stub swaps the font table to
(mte_hook.EXT_*). Extension glyphs get a tinted cell so the expansion is visible.
Drawn in the dialogue palette -- level 1 is the ink colour, level 2 the shadow --
so the sheet shows what the screen shows, not an idealised bitmap.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import fontcodec as F
import mte_hook as M
import redirect_hook as R
from PIL import Image, ImageDraw, ImageFont

ROM = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/builds/PPKP9_kr.nds"
OUT = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font"

INK = {0: None, 1: (250, 250, 250), 2: (122, 112, 168), 3: (255, 80, 80)}
BG_ARM9 = (26, 28, 38)
BG_EXT = (24, 46, 44)          # extension-page glyphs, tinted

rom = open(ROM, "rb").read()
tbl = F.load_table(rom)
m = {k: int(v) for k, v in
     json.load(open(os.path.join(OUT, "kr_font_map.json"), encoding="utf-8")).items()}

# where the relocated overlay 28 lives now, so the extension pages can be read
fat = int.from_bytes(rom[0x48:0x4C], "little")
ov_start = int.from_bytes(rom[fat + 25 * 8:fat + 25 * 8 + 4], "little")
ext_rom = ov_start + (M.EXT_BASE - R.OV28_RAM)


def glyph(cc):
    blk = cc // 64
    if blk in M.EXT_BLOCKS:
        o = ext_rom + (blk - M.EXT_BLOCK0) * 0x900
        return F.decode_glyph(bytearray(rom[o:o + 0x900]), cc)
    return F.decode_glyph(F.block_region(rom, tbl, blk), cc)


syls = sorted(m, key=lambda c: ord(c))
ext = set(M.EXT_CODES)
n_ext = sum(1 for s in syls if m[s] in ext)
blank = [s for s in syls if all(v == 0 for row in glyph(m[s]) for v in row)]

cols, cell, scale = 48, 14, 3
rows = (len(syls) + cols - 1) // cols
img = Image.new("RGB", (cols * cell, rows * cell), BG_ARM9)
px = img.load()
for i, s in enumerate(syls):
    cc = m[s]
    gx, gy = (i % cols) * cell, (i // cols) * cell
    if cc in ext:
        for y in range(cell):
            for x in range(cell):
                px[gx + x, gy + y] = BG_EXT
    g = glyph(cc)
    for y in range(12):
        for x in range(len(g[y])):
            v = INK[g[y][x]]
            if v:
                px[gx + x + 1, gy + y + 1] = v

big = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
title = 36
sheet = Image.new("RGB", (big.width, big.height + title), (16, 16, 20))
sheet.paste(big, (0, title))
d = ImageDraw.Draw(sheet)
try:
    f = ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 19)
except Exception:
    f = ImageFont.load_default()
d.text((10, 9), f"PPKP9 한글 폰트팩 {len(syls)}자   "
                f"ARM9 슬롯 {len(syls) - n_ext} · 확장 페이지 {n_ext}(초록 배경)   "
                f"빈 글리프 {len(blank)}", font=f, fill=(232, 232, 240))
sheet.save(os.path.join(OUT, "fontpack_all.png"))
print(f"{len(syls)} glyphs ({n_ext} on extension pages, {len(blank)} blank) "
      f"-> fontpack_all.png {sheet.size}")

# readable zoom of the top rows (the syllables the translation uses most)
z = 8
head = img.crop((0, 0, cols * cell, 6 * cell))
head.resize((head.width * z, head.height * z), Image.NEAREST).save(
    os.path.join(OUT, "fontpack_sample.png"))
print("wrote fontpack_sample.png")
