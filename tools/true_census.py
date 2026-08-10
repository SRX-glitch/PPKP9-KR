#!/usr/bin/env python3
"""Authoritative charcode-usage census: parse EVERY `F8 6B` text command in the
whole ROM and count the charcodes emitted. A charcode is safe to repurpose (for
a Hangul glyph OR as MTE dict storage) only if it is never emitted here.

This supersedes census_final.json / usable_slots.json, which were built from a
looser scan and wrongly marked some in-use charcodes (e.g. 0x0BEE) as free.
"""
import os, sys, json, collections
sys.path.insert(0, os.path.dirname(__file__))
import fontcodec as F

ROM = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
OUT = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font"
rom = open(ROM, "rb").read()
N = len(rom)

used = collections.Counter()
i = 0
while i < N - 2:
    if rom[i] == 0xF8 and rom[i + 1] == 0x6B:
        j = i + 3
        while j < N and rom[j] != 0 and rom[j] < 0xF8:
            b = rom[j]
            if 1 <= b <= 231:
                used[b - 1] += 1
                j += 1
            elif 232 <= b <= 247:
                used[256 + (b - 232) * 256 + rom[j + 1]] += 1
                j += 2
            else:
                j += 1
        i = j
        continue
    i += 1

print(f"F8 6B commands parsed; distinct charcodes emitted: {len(used)}")

# alias/filler blocks (FONT_TABLE entry duplicates an earlier block -> no storage)
tbl = F.load_table(rom)
seen = {}
alias = set()
for idx, p in enumerate(tbl):
    if p in seen:
        alias.add(idx)
    else:
        seen[p] = idx

# safe glyph slots: charcode never emitted AND its block has real glyph storage
safe = []
for cc in range(4352):
    if cc in used:
        continue
    if cc // 64 in alias:
        continue
    safe.append(cc)
# prefer rarest-JIS-first (high charcode first) as before
safe.sort(reverse=True)
print(f"safe repurposable charcodes: {len(safe)}  (range {min(safe):#06x}..{max(safe):#06x})")

# sanity: were any previously-allocated slots actually in use?
old = set(json.load(open(os.path.join(OUT, "usable_slots.json"))))
bad = sorted(c for c in old if c in used)
print(f"OLD usable_slots that are actually USED by text: {len(bad)}  {[hex(c) for c in bad[:20]]}")

json.dump(safe, open(os.path.join(OUT, "usable_slots.json"), "w"))
json.dump({str(k): v for k, v in used.items()},
          open(os.path.join(OUT, "true_usage.json"), "w"))
print("rewrote usable_slots.json (authoritative)")

# which mte_hook regions are clean?
import mte_hook
print("\nmte_hook region charcode ranges vs usage:")
for lo, hi in mte_hook.RESERVED_CC:
    hits = sum(used.get(c, 0) for c in range(lo, hi + 1))
    print(f"  0x{lo:04X}-0x{hi:04X}: {hits} text hits  {'OK' if hits == 0 else '** IN USE **'}")
