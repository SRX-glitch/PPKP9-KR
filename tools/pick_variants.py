#!/usr/bin/env python3
"""Decide which PokeTEXT table variant matches the real ROM font.

Renders each candidate character with a reference CJK font at 12x12 and scores
pixel agreement against the actual glyph decoded from the ROM.
"""
import os, re, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import fontcodec as F
from PIL import Image, ImageDraw, ImageFont

ROM = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
CS = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/poketext_src/PokeTEXT.decompiled.cs"
REF_FONT = r"C:/Windows/Fonts/msgothic.ttc"

rom = open(ROM, "rb").read()
tbl = F.load_table(rom)

lines = open(CS, encoding="utf-8").read().splitlines()
in3 = False
tables = {}
pat = re.compile(r'array4\[(\d+)\]\s*=\s*"(.*)";\s*$')
for ln in lines:
    if "ポケ3以降の文字コード変換処理" in ln:
        in3 = True
    m = pat.search(ln)
    if m and in3:
        s = re.sub(r'\\u([0-9a-fA-F]{4})', lambda x: chr(int(x.group(1), 16)), m.group(2))
        tables.setdefault(int(m.group(1)), []).append(s)

font = ImageFont.truetype(REF_FONT, 12)


def ref_bits(ch):
    img = Image.new("L", (12, 12), 0)
    d = ImageDraw.Draw(img)
    try:
        bb = d.textbbox((0, 0), ch, font=font)
    except Exception:
        return None
    d.text(((12 - (bb[2] - bb[0])) / 2 - bb[0], (12 - (bb[3] - bb[1])) / 2 - bb[1]),
           ch, font=font, fill=255)
    p = img.load()
    return [[1 if p[x, y] >= 110 else 0 for x in range(12)] for y in range(12)]


def rom_bits(cc):
    region = F.block_region(rom, tbl, cc // 64)
    g = F.decode_glyph(region, cc)
    return [[1 if v else 0 for v in row] + [0] * (12 - len(row)) for row in g]


def score(a, b):
    inter = same = 0
    for y in range(12):
        for x in range(12):
            if a[y][x] and b[y][x]:
                inter += 1
            if a[y][x] == b[y][x]:
                same += 1
    return same / 144.0, inter


def cc_for(table, idx):
    """table 2..17, index 0..255 -> charcode"""
    return 256 + (table - 2) * 256 + idx


SAMPLE = list(range(0, 256, 7))  # ~37 chars per variant
results = {}
for t in sorted(tables):
    if t == 1:
        continue
    best = None
    for vi, s in enumerate(tables[t]):
        tot = 0.0
        n = 0
        for idx in SAMPLE:
            if idx >= len(s):
                continue
            ch = s[idx]
            if ch in ("　", " ", ""):
                continue
            r = ref_bits(ch)
            if r is None:
                continue
            sc, _ = score(r, rom_bits(cc_for(t, idx)))
            tot += sc
            n += 1
        avg = tot / n if n else 0
        print(f"  table {t:2d} variant {vi}: agreement {avg:.3f}  (n={n})  head={s[:12]!r}")
        if best is None or avg > best[1]:
            best = (vi, avg)
    results[t] = best[0]
    print(f"  -> table {t}: variant {best[0]} (score {best[1]:.3f})\n")

# table 1: compare all 4 variants over charcodes 0..230
best = None
for vi, s in enumerate(tables[1]):
    tot = n = 0
    for idx in range(0, min(len(s), 231), 5):
        ch = s[idx]
        r = ref_bits(ch)
        if r is None:
            continue
        sc, _ = score(r, rom_bits(idx))
        tot += sc
        n += 1
    avg = tot / n
    print(f"  table 1 variant {vi}: agreement {avg:.3f} (len {len(s)})")
    if best is None or avg > best[1]:
        best = (vi, avg)
results[1] = best[0]
print(f"  -> table 1: variant {best[0]}")

json.dump(results, open(r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font/variants.json", "w"))
print("\nchosen variants:", results)
