#!/usr/bin/env python3
"""Try candidate 2bpp layouts for the 36-byte glyph; render block 3 (kana) for each."""
import os
from PIL import Image

ROM = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
OUT = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font"
FONT_TABLE_ROM = 0x92FC8
rom = open(ROM, "rb").read()


def r2o(ram):
    return ram - 0x02000000 + 0x4000


def blockdata(b):
    p = int.from_bytes(rom[FONT_TABLE_ROM + b * 4:FONT_TABLE_ROM + b * 4 + 4], "little")
    o = r2o(p)
    return rom[o:o + 0x900]


LEVEL = {0b00: 0, 0b10: 1, 0b01: 2, 0b11: 3}


def px(src, bi, pix):
    return LEVEL[(src[bi] >> (pix * 2)) & 3]


# each layout: (name, width, height, fn(r,c)->(byte_index, pixel_index))
LAYOUTS = {
    # current validated-but-partial: 12x8
    "A_cur_12x8": (12, 8, lambda r, c: (2 * r, c) if c < 4 else ((2 * r + 1, c - 4) if c < 8 else (16 + 2 * r, c - 8))),
    # column-major groups of 12 rows
    "B_colmajor_12x12": (12, 12, lambda r, c: (12 * (c // 4) + r, c % 4)),
    # row-major 3 bytes per row
    "C_rowmajor_12x12": (12, 12, lambda r, c: (3 * r + c // 4, c % 4)),
    # interleaved stride-2, 3 groups at +0/+15/+16 extended to 12 rows won't fit; try +0/+12/+24 stride1 == B
    # stride-2 groups but 12 rows using base 0 / 1 / 24 ?
    "D_stride2_pairs": (12, 12, lambda r, c: (2 * r + (c // 4), c % 4) if c < 8 else (24 + r, c - 8)),
    # 16 wide x 8 tall (4 groups incl odd bytes 17..31)
    "E_16x8": (16, 8, lambda r, c: [(2 * r, c), (2 * r + 1, c - 4), (16 + 2 * r, c - 8), (17 + 2 * r, c - 12)][c // 4]),
}

PAL = {0: (255, 255, 255), 1: (0, 0, 0), 2: (160, 160, 160), 3: (255, 0, 0)}
z = 5
for name, (W, H, fn) in LAYOUTS.items():
    data = blockdata(3)
    CW, CH = W + 1, H + 1
    cols = 16
    img = Image.new("RGB", (cols * CW, 4 * CH), (40, 40, 90))
    p = img.load()
    for g in range(64):
        src = data[g * 36:(g + 1) * 36]
        gx, gy = (g % cols) * CW, (g // cols) * CH
        for r in range(H):
            for c in range(W):
                bi, pi = fn(r, c)
                if bi >= 36:
                    continue
                p[gx + c, gy + r] = PAL[px(src, bi, pi)]
    img.resize((img.width * z, img.height * z), Image.NEAREST).save(
        os.path.join(OUT, f"layout_{name}.png"))
    print("wrote", name, img.size)
