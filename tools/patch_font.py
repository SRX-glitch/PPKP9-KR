#!/usr/bin/env python3
"""Inject Hangul glyphs into the ROM font and verify by decoding them back.

Uses Gulim 12px (a bitmap-embedded font -> pixel-crisp at 12x12).
Writes:  rom/DS/PPKP9_kr_font.nds  +  survey/font/hangul_map.json
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import fontcodec as F
from PIL import Image, ImageDraw, ImageFont

ROMSRC = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
ROMOUT = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/builds/PPKP9_kr_font.nds"
SURVEY = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font"
TRANS = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/translation/dialogue_ko.tsv"
GULIM = r"C:/Windows/Fonts/gulim.ttc"

font = ImageFont.truetype(GULIM, 12)


def render(ch):
    img = Image.new("L", (12, 12), 0)
    d = ImageDraw.Draw(img)
    bb = d.textbbox((0, 0), ch, font=font)
    d.text(((12 - (bb[2] - bb[0])) / 2 - bb[0], (12 - (bb[3] - bb[1])) / 2 - bb[1]),
           ch, font=font, fill=255)
    p = img.load()
    return [[2 if p[x, y] >= 140 else (1 if p[x, y] >= 60 else 0) for x in range(12)]
            for y in range(12)]


def main():
    rom = bytearray(open(ROMSRC, "rb").read())
    tbl = F.load_table(bytes(rom))
    slots = json.load(open(os.path.join(SURVEY, "usable_slots.json")))

    text = open(TRANS, encoding="utf-8").read()
    syls = sorted({c for c in text if 0xAC00 <= ord(c) <= 0xD7A3})
    print(f"syllables to inject: {len(syls)}  (slots available: {len(slots)})")
    mapping = {s: slots[i] for i, s in enumerate(syls)}

    # group by block so each 0x900 region is read/modified/written once
    byblock = {}
    for ch, cc in mapping.items():
        byblock.setdefault(cc // 64, []).append((ch, cc))

    for block, items in byblock.items():
        region = F.block_region(bytes(rom), tbl, block)
        for ch, cc in items:
            F.encode_glyph(region, cc, render(ch))
        o = F.ram2rom(tbl[block])
        rom[o:o + 0x900] = region
    print(f"patched {len(byblock)} font blocks")

    open(ROMOUT, "wb").write(rom)
    print(f"wrote {ROMOUT} ({len(rom)} bytes, same size as source: "
          f"{len(rom) == os.path.getsize(ROMSRC)})")

    # ---- verify: decode the patched ROM back and compare to what we rendered ----
    rom2 = open(ROMOUT, "rb").read()
    tbl2 = F.load_table(rom2)
    bad = 0
    for ch, cc in mapping.items():
        region = F.block_region(rom2, tbl2, cc // 64)
        got = F.decode_glyph(region, cc)
        want = render(ch)
        if got != want:
            bad += 1
    print(f"round-trip verify: {len(mapping) - bad}/{len(mapping)} glyphs exact"
          f"{'  ** MISMATCHES **' if bad else '  OK'}")

    # visual sheet straight from the patched ROM
    PAL = {0: (255, 255, 255), 1: (150, 150, 150), 2: (0, 0, 0)}
    cols = 24
    rows = (len(syls) + cols - 1) // cols
    img = Image.new("RGB", (cols * 13, rows * 13), (70, 70, 120))
    p = img.load()
    for i, ch in enumerate(syls):
        cc = mapping[ch]
        g = F.decode_glyph(F.block_region(rom2, tbl2, cc // 64), cc)
        gx, gy = (i % cols) * 13, (i // cols) * 13
        for y in range(12):
            for x in range(12):
                p[gx + x, gy + y] = PAL[g[y][x]]
    img.resize((img.width * 5, img.height * 5), Image.NEAREST).save(
        os.path.join(SURVEY, "patched_hangul.png"))
    json.dump({ch: cc for ch, cc in mapping.items()},
              open(os.path.join(SURVEY, "hangul_map.json"), "w"), ensure_ascii=False)
    print("wrote patched_hangul.png + hangul_map.json")


main()
