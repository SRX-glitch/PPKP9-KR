#!/usr/bin/env python3
"""Dump the whole PPKP9 font straight out of the ROM file (ARM9 is uncompressed).

FONT_TABLE @ RAM 0x0208EFC8 = ROM 0x92FC8, 512 entries of u32 RAM pointers.
FONT_TABLE[block] -> 64 glyphs x 36 bytes (0x900) for charcodes block*64 .. +63.
Glyph decode layout per tools/fontenc.py (validated on screen).
"""
import sys, os
from PIL import Image

ROM = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
OUT = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font"
FONT_TABLE_ROM = 0x92FC8
NBLOCK = 512
GLYPH = 36


def r2o(ram):
    """RAM address -> ROM offset (ARM9 static, uncompressed)."""
    return ram - 0x02000000 + 0x4000


def decode_glyph(src, w=12, h=8):
    """src: 36 bytes -> h rows of w values (0=off,1=full ink,2=faint)."""
    rows = []
    for r in range(h):
        row = []
        for c in range(w):
            if c < 4:
                bi, pix = 2 * r, c
            elif c < 8:
                bi, pix = 2 * r + 1, c - 4
            else:
                bi, pix = 16 + 2 * r, c - 8
            bits = (src[bi] >> (pix * 2)) & 0b11
            row.append({0b00: 0, 0b10: 1, 0b01: 2}.get(bits, 3))
        rows.append(row)
    return rows


PAL = {0: (255, 255, 255), 1: (0, 0, 0), 2: (170, 170, 170), 3: (255, 0, 0)}


def main():
    os.makedirs(OUT, exist_ok=True)
    rom = open(ROM, "rb").read()
    tbl = []
    for i in range(NBLOCK):
        o = FONT_TABLE_ROM + i * 4
        tbl.append(int.from_bytes(rom[o:o + 4], "little"))

    # classify entries
    valid = [(i, p) for i, p in enumerate(tbl) if 0x02000000 <= p < 0x02400000]
    print(f"valid ptrs: {len(valid)}/{NBLOCK}")
    print("first 8:", [f"{i}:{p:08X}" for i, p in valid[:8]])
    print("last 8:", [f"{i}:{p:08X}" for i, p in valid[-8:]])
    if len(valid) < NBLOCK:
        bad = [(i, p) for i, p in enumerate(tbl) if not (0x02000000 <= p < 0x02400000)]
        print(f"non-ptr entries: {len(bad)}, sample:", [f"{i}:{p:08X}" for i, p in bad[:8]])

    ptrs = sorted(set(p for _, p in valid))
    print(f"unique ptrs: {len(ptrs)}  range {ptrs[0]:08X}..{ptrs[-1]:08X}")
    # spacing between consecutive unique ptrs (expect 0x900)
    gaps = {}
    for a, b in zip(ptrs, ptrs[1:]):
        gaps[b - a] = gaps.get(b - a, 0) + 1
    print("ptr gaps:", dict(sorted(gaps.items(), key=lambda x: -x[1])[:5]))

    # render one big sheet: rows = blocks, 64 glyphs per row
    CW, CH = 13, 9  # cell with 1px gutter
    blocks = [i for i, p in valid]
    img = Image.new("RGB", (64 * CW, len(blocks) * CH), (40, 40, 80))
    px = img.load()
    blank_blocks = []
    for bi, block in enumerate(blocks):
        off = r2o(tbl[block])
        if off < 0 or off + 0x900 > len(rom):
            continue
        data = rom[off:off + 0x900]
        if not any(data):
            blank_blocks.append(block)
        for g in range(64):
            rows = decode_glyph(data[g * GLYPH:(g + 1) * GLYPH])
            for r in range(8):
                for c in range(12):
                    px[g * CW + c, bi * CH + r] = PAL[rows[r][c]]
    img.save(os.path.join(OUT, "font_sheet_all.png"))
    print("sheet:", img.size, "blocks:", len(blocks), "blank blocks:", blank_blocks[:20],
          f"({len(blank_blocks)} total)")

    # also a zoomed sheet of the first 8 blocks for legibility check
    z = 6
    sub = img.crop((0, 0, 64 * CW, 8 * CH)).resize((64 * CW * z, 8 * CH * z), Image.NEAREST)
    sub.save(os.path.join(OUT, "font_sheet_first8_zoom.png"))
    print("wrote", OUT)


main()
