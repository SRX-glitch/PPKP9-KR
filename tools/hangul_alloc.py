#!/usr/bin/env python3
"""Allocate font charcodes for Hangul syllables.

Safety rules for picking a slot:
  * NEVER touch blocks 55-63 / 67 -- their FONT_TABLE entries alias block 0, so
    writing there would corrupt あ-おetc. (they are filler, not free space).
  * Only charcodes with zero hits in the text-region census.
  * Prefer the rarest JIS kanji: highest charcode first (tables 13-14 are JIS
    level-2 obscure), and skip tables 15-17 (kana/katakana/half-width repeats,
    likely used by menus we haven't censused).
"""
import os, sys, json, collections
sys.path.insert(0, os.path.dirname(__file__))
import fontcodec as F

SURVEY = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font"
ROM = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"

ALIAS_BLOCKS = {55, 56, 57, 58, 59, 60, 61, 62, 63, 67}
# tables 15,16,17 = charcodes 3584-4351 -> blocks 56-67 (already mostly alias);
# table 14 = 3328-3583 (blocks 52-55). Keep block 55 out via ALIAS_BLOCKS.
SAFE_BLOCK_MAX = 54          # blocks 1..54 = tables 2..14 kanji


def usable_slots():
    census = json.load(open(os.path.join(SURVEY, "census_final.json")))
    counts = {int(k): v for k, v in census["counts"].items()}
    rom = open(ROM, "rb").read()
    tbl = F.load_table(rom)

    # blocks that share a pointer with an earlier block are unusable
    seen = {}
    aliased = set()
    for i, p in enumerate(tbl):
        if p in seen:
            aliased.add(i)
        else:
            seen[p] = i

    slots = []
    for cc in range(4352):
        b = cc // 64
        if b in aliased or b in ALIAS_BLOCKS:
            continue
        if b < 1 or b > SAFE_BLOCK_MAX:
            continue
        if counts.get(cc, 0) != 0:
            continue
        slots.append(cc)
    # rarest-JIS-first = highest charcode first
    slots.sort(reverse=True)
    return slots, counts, aliased


def allocate(syllables, slots):
    """syllables: list ordered by frequency (most common first)."""
    if len(syllables) > len(slots):
        raise SystemExit(f"need {len(syllables)} slots but only {len(slots)} available")
    return {s: slots[i] for i, s in enumerate(syllables)}


if __name__ == "__main__":
    slots, counts, aliased = usable_slots()
    print(f"aliased blocks detected: {sorted(aliased)}")
    print(f"usable Hangul slots: {len(slots)}")
    if slots:
        print(f"  charcode range {min(slots):#06x}..{max(slots):#06x}")
        perblock = collections.Counter(c // 64 for c in slots)
        print(f"  spread over {len(perblock)} blocks; fullest: "
              f"{perblock.most_common(8)}")
    json.dump(slots, open(os.path.join(SURVEY, "usable_slots.json"), "w"))
    print("wrote usable_slots.json")
