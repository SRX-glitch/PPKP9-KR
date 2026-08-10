#!/usr/bin/env python3
"""Whole-ROM charcode census with the VALIDATED opcode walker.

true_census.py answers the same question with the old scanner, which ends a text
run at the first byte >= 0xF8 or 0x00 and then jumps to the next `F8 6B` -- the
session-20 truncation bug. Everything after an inline control code went uncounted,
so charcodes that only ever appear in those tails were reported free. That is the
dangerous direction for a census: a "free" slot we then overwrite with a Hangul
glyph is a character some scenario really draws.

Here the run continues *through* control codes using survey/ov28/opcode_lengths.json
(disassembly-derived, 9,957/9,957 corpus anchors), exactly like extract_all.py, and
the scan covers the whole ROM rather than overlay 28 -- so the answer is
"unused by EVERY scenario", which is what a font expansion that must not disturb
other scenarios needs.

The in_dialogue gate keeps binary data from being counted as text: a run only
counts once an `F8 6B` (message start) has been seen, and the gate closes on 3+
zero bytes, an `FF`, or an unregistered subcode. Between messages we jump
straight to the next `F8 6B`, which is both faster and the same semantics.
"""
import os, sys, json, collections
sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P
import fontcodec as F

BASE = r"C:/Users/jngji/Desktop/실험실"
ROM = f"{BASE}/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
OV = f"{BASE}/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/ov28"
OUT = f"{BASE}/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font"

rom = open(ROM, "rb").read()
L = json.load(open(f"{OV}/opcode_lengths.json"))
BARE = {int(k): v for k, v in L["bare"].items()}
F8 = {int(k): v for k, v in L["f8"].items()}
N = len(rom)

used = collections.Counter()
runs = chars = desync = 0
i, in_dialogue, zeros = 0, False, 0
while i < N - 2:
    if not in_dialogue:
        j = rom.find(b"\xf8\x6b", i)
        if j < 0:
            break
        i = j
    b = rom[i]
    if b == 0:
        zeros += 1
        if zeros >= 3:
            in_dialogue = False
        i += 1
        continue
    zeros = 0
    if b < 0xF8:
        st, n = i, 0
        while i < N - 2 and 0 < rom[i] < 0xF8:
            cc, nxt = P.bytes_to_cc(rom, i)
            if P.CC2CH.get(cc) is None:
                break
            used[cc] += 1
            n += 1
            i = nxt
        if n:
            runs += 1
            chars += n
        if i == st:
            i += 1
    elif b in BARE:
        if b == 0xFF:
            in_dialogue = False
        i += BARE[b]
    elif b in (0xF8, 0xF9):
        s = rom[i + 1]
        if s == 0x6B:
            in_dialogue = True
        n = F8.get(s)
        if n is None:
            desync += 1
            in_dialogue = False
            n = 2
        i += n
    else:
        desync += 1
        i += 1

print(f"whole-ROM walk: {runs} text runs, {chars} chars, {desync} unknown opcodes")
print(f"distinct charcodes emitted anywhere: {len(used)}")

tbl = F.load_table(rom)
seen, alias = {}, set()
for idx, p in enumerate(tbl):
    if p in seen:
        alias.add(idx)
    else:
        seen[p] = idx
print(f"font table: {len(tbl)} blocks, {len(alias)} alias blocks "
      f"(no independent glyph storage) -> {(len(tbl)-len(alias))*64} addressable glyphs")

free = [cc for cc in range(4352)
        if cc not in used and cc // 64 not in alias]
free_lo = [cc for cc in free if 256 <= cc < 0x1000]     # 2-byte code, 12px full width
print(f"\nGLOBALLY unused charcodes with real storage: {len(free)}")
print(f"  of those usable as Hangul glyph slots (256 <= cc < 0x1000): {len(free_lo)}")

# what the current build actually took, and how much of it belongs to someone else
try:
    m = json.load(open(f"{OUT}/kr_font_map.json", encoding="utf-8"))
    taken = sorted(m.values())
    clash = [cc for cc in taken if cc in used]
    print(f"\ncurrent font pack: {len(taken)} slots, charcodes "
          f"0x{min(taken):04X}-0x{max(taken):04X}")
    print(f"  slots that ANOTHER scenario really draws: {len(clash)} "
          f"({sum(used[c] for c in clash)} occurrences ROM-wide)")
except FileNotFoundError:
    pass

json.dump({str(k): v for k, v in used.items()},
          open(f"{OUT}/global_usage.json", "w"))
json.dump(free, open(f"{OUT}/global_free.json", "w"))
print(f"\nwrote {OUT}/global_usage.json and global_free.json")
