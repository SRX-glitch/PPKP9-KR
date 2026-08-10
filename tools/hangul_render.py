#!/usr/bin/env python3
"""Render Hangul syllables into the game's 12x12 / 3-level glyph format.

Levels: 0 = transparent, 1 = ink colour (light), 2 = full ink.
Tries several fonts/sizes/offsets and writes comparison sheets so we can judge
legibility before committing.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font"
CANDS = [
    ("malgun", r"C:/Windows/Fonts/malgun.ttf"),
    ("malgunbd", r"C:/Windows/Fonts/malgunbd.ttf"),
    ("gulim", r"C:/Windows/Fonts/gulim.ttc"),
    ("batang", r"C:/Windows/Fonts/batang.ttc"),
    ("dotum", r"C:/Windows/Fonts/dotum.ttc"),
]
W = H = 12


def render(fontpath, size, syllable, dx=0, dy=0, thresh_full=140, thresh_faint=60):
    f = ImageFont.truetype(fontpath, size)
    img = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(img)
    # centre the glyph in the cell
    bbox = d.textbbox((0, 0), syllable, font=f)
    ox = (W - (bbox[2] - bbox[0])) / 2 - bbox[0] + dx
    oy = (H - (bbox[3] - bbox[1])) / 2 - bbox[1] + dy
    d.text((ox, oy), syllable, font=f, fill=255)
    px = img.load()
    grid = []
    for y in range(H):
        row = []
        for x in range(W):
            v = px[x, y]
            row.append(2 if v >= thresh_full else (1 if v >= thresh_faint else 0))
        grid.append(row)
    return grid


PAL = {0: (255, 255, 255), 1: (150, 150, 150), 2: (0, 0, 0)}
TEST = "가나다라마바사아자차카타파하강명령훈련試경험치체력야구선수감독친구학교練習"


def sheet(name, grids, cols=20, z=8):
    rows = (len(grids) + cols - 1) // cols
    img = Image.new("RGB", (cols * (W + 1), rows * (H + 1)), (70, 70, 120))
    p = img.load()
    for i, g in enumerate(grids):
        gx, gy = (i % cols) * (W + 1), (i // cols) * (H + 1)
        for y in range(H):
            for x in range(W):
                p[gx + x, gy + y] = PAL[g[y][x]]
    img.resize((img.width * z, img.height * z), Image.NEAREST).save(
        os.path.join(OUT, f"hangul_{name}.png"))


if __name__ == "__main__":
    avail = [(n, p) for n, p in CANDS if os.path.exists(p)]
    print("fonts:", [n for n, _ in avail])
    for name, path in avail:
        for size in (11, 12, 13):
            try:
                grids = [render(path, size, ch) for ch in TEST]
            except Exception as e:
                print(" fail", name, size, e)
                continue
            sheet(f"{name}_{size}", grids)
            print("wrote", f"hangul_{name}_{size}.png")
