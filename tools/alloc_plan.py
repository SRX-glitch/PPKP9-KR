#!/usr/bin/env python3
"""Allocate every charcode/RAM resource the patch needs from GLOBALLY-free space.

Until now the font pack, the MTE dictionary and the hooks were carved out of
charcodes and glyph storage that only the *Nice Guy* scenario leaves alone, so
~776 charcodes (~6,900 drawn occurrences) render wrong if the player picks any
other scenario. global_census.py measures what every scenario really draws; this
turns that into an allocation where nothing the patch touches is ever drawn.

The key asymmetry that makes it fit: an MTE code is decoded by the hook and never
reaches the glyph lookup, so it needs a charcode but NO storage. The font table's
alias blocks (55-63 alias block 0, i.e. charcodes 0x0DC0-0x0FFF) are exactly that
-- charcodes with no independent storage -- so they are the natural home for the
dictionary's codes, and every charcode that *does* own storage stays available
for Hangul.

Outputs (survey/font/):
  global_slots.json  Hangul glyph slot candidates, ascending
  alloc_plan.json    the CODE_RANGES / DICT_REGIONS / hook span to paste into
                     mte_hook.py and redirect_hook.py, with the census behind it
"""
import os, sys, json, collections
sys.path.insert(0, os.path.dirname(__file__))
import fontcodec as F

BASE = r"C:/Users/jngji/Desktop/실험실"
ROM = f"{BASE}/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
OUT = f"{BASE}/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font"

HOOK_BYTES = 1152              # redirect + loop + MTE engine hooks (460 B used)
STUB_BYTES = 0x200             # render_char stub + extension path; its tables live
CODE_TBL_BYTES = 8 * 64        # separately, because globally-free charcodes come
STORE_TBL_BYTES = 8 * 24       # in many small runs and 51 (base,count) pairs do
                               # not fit the 128 B the stub used to reserve
CODE_REGION_BYTES = 704        # redirect_hook's second code block; TINY_TBL (256 B)
                               # sits at its base, hook code fills the rest
# ⛔ CODE_REGION and TINY_TBL used to be HAND-PICKED constants in
# redirect_hook.py (session 38 moved TINY_TBL out of the hook block by eye).
# Under census v2 that address, 0x02087D8C, sits on ﾏ ﾐ ﾑ ﾒ ﾘ ﾙ ﾚ ﾛ ﾝ ｧ ｨ --
# halfwidth katakana the ARM9 player-name array really draws (ｸﾛｰﾊｰ, ﾀﾙﾋｯｼｭ,
# 野球ﾏｽｸ, ｾｷﾞﾉｰﾙ). Anything that consumes glyph storage has to be allocated
# HERE, from the same census, or it silently eats someone's glyph.

rom = open(ROM, "rb").read()
tbl = F.load_table(rom)

# ---- who really draws each charcode ----------------------------------------
# census v2 (tools/rom_census.py) replaces global_usage.json, which counted only
# `F8 6B` dialogue. That blind spot shipped Hangul on top of 笠稲鶴岡 and turned
# the baseball lineup into 小島原 / 刃葉 / 熱塁 -- those kanji appear in the ARM9
# player-name array and in no message anywhere. See survey/CENSUS_V2.md.
#
# The kanji-input dictionary in overlay 13 is the one consumer we deliberately
# sacrifice: 2,768 kanji reachable from the name-entry keyboard's 漢字 tab, of
# which 966 are drawn by NOTHING ELSE. We disable that tab (tools/name_kbd.py)
# and take those 966. Every charcode any other consumer draws stays untouched,
# so Japanese fallback text -- which is still most of the script -- is unaffected.
raw = {int(k): v for k, v in json.load(open(f"{OUT}/census_v2_usage.json")).items()}
KEEP_IME = os.environ.get("PPKP9_KEEP_IME") == "1"
used, reclaimed = {}, []
for cc, srcs in raw.items():
    other = {k: v for k, v in srcs.items() if k != "ime"}
    if other or KEEP_IME:
        used[cc] = sum(srcs.values())
    else:
        reclaimed.append(cc)
print(f"census v2: {len(raw)} charcodes drawn by someone; "
      f"kanji-dictionary-only {len(reclaimed)} "
      f"({'KEPT (PPKP9_KEEP_IME=1)' if KEEP_IME else 'RECLAIMED'})")
print(f"  -> treated as drawn: {len(used)}")

seen, alias = {}, {}
for i, p in enumerate(tbl):
    if p in seen:
        alias[i] = seen[p]
    else:
        seen[p] = i


def span(cc):
    """RAM byte span this charcode's glyph occupies (its 36 interleaved bytes)."""
    base = tbl[cc // 64]
    offs = [b for row in F.glyph_map(cc) for b, _ in row]
    return base + min(offs), base + max(offs) + 1


# ---- charcodes nobody draws -------------------------------------------------
free_storage = [cc for cc in range(0x1000)
                if cc >= 256 and cc not in used and cc // 64 not in alias]
# An MTE code or an escape must also be a charcode the ENCODER can never emit:
# poketbl maps each game character to one canonical charcode, so if a code were
# canonical for, say, a halfwidth letter, a translation containing that letter
# would emit it and the hook would expand it as a dictionary entry.
import poketbl as P
canon = set(P.CH2CC.values())
free_alias = [cc for cc in range(0x1000)
              if cc not in used and cc // 64 in alias and cc not in canon]
free_high = [cc for cc in range(0x1000, 0x1100)
             if cc not in used and cc not in canon]
print(f"globally-free charcodes: storage {len(free_storage)}, "
      f"alias(no storage) {len(free_alias)}, high(no storage) {len(free_high)}")

# ---- how many MTE codes will exist, and therefore how much dictionary --------
# Sizing this BEFORE the storage is carved matters: every byte the dictionary
# takes out of a glyph-storage hole reserves the charcodes whose 36 interleaved
# bytes overlap it, and each of those is a Hangul slot lost. The old fixed
# 6 KB bought room for 761 entries when only 234 codes can address them -- 527
# entries of dead storage, paid for in Hangul slots.
# BANK_COUNT is a design constant of the 3-byte escape, not an allocation, so it
# lives HERE rather than being imported from redirect_hook -- that module now
# reads this plan, and importing it back would be a cycle.
BANK_COUNT = 10
EXT_TARGET = int(os.environ.get("PPKP9_EXT_TARGET", "420"))
_n_escapes = 2 + BANK_COUNT                       # ESC + RET + the banks
_mte_codes = max(0, len(free_alias) - EXT_TARGET) + len(free_high) - _n_escapes
DICT_BYTES = _mte_codes * 8
print(f"MTE codes projected {_mte_codes} -> dictionary storage {DICT_BYTES} B "
      f"(was a fixed 6144 B)")

# ---- contiguous RAM runs that no drawn charcode occupies --------------------
busy = []
for cc in range(4352):
    if cc in used:
        busy.append(span(cc))
busy.sort()
merged = []
for lo, hi in busy:
    if merged and lo <= merged[-1][1]:
        merged[-1][1] = max(merged[-1][1], hi)
    else:
        merged.append([lo, hi])
lo_ram = min(tbl)
hi_ram = max(tbl) + 0x900
holes = []
cur = lo_ram
for lo, hi in merged:
    if lo > cur:
        holes.append((cur, lo))
    cur = max(cur, hi)
if cur < hi_ram:
    holes.append((cur, hi_ram))
holes.sort(key=lambda h: h[1] - h[0], reverse=True)
print(f"free glyph-storage runs: {len(holes)}, largest "
      f"{[(hex(a), b-a) for a, b in holes[:6]]}")


def take(nbytes, align=4):
    """Carve nbytes out of the largest remaining hole."""
    for i, (a, b) in enumerate(holes):
        a2 = (a + align - 1) & ~(align - 1)
        if b - a2 >= nbytes:
            holes[i] = (a2 + nbytes, b)
            holes.sort(key=lambda h: h[1] - h[0], reverse=True)
            return a2
    raise SystemExit(f"no free run holds {nbytes} B")


# Largest request first. `take` returns the first hole that fits, so asking for
# the small blocks first can drop them into the only run big enough for a large
# one -- census v2 leaves 141 runs and only ONE of them holds 1152 B.
hook_at = take(HOOK_BYTES)
code_region_at = take(CODE_REGION_BYTES)
stub_at = take(STUB_BYTES)
code_tbl_at = take(CODE_TBL_BYTES)
store_tbl_at = take(STORE_TBL_BYTES)
tiny_tbl_at = code_region_at   # TINY_TBL lives at the base of CODE_REGION
dict_at, dict_slots = [], DICT_BYTES // 8
want = DICT_BYTES
while want > 0:
    for i, (a, b) in enumerate(holes):
        a2 = (a + 3) & ~3
        n = min(want, (b - a2) // 8 * 8)
        if n >= 64:
            dict_at.append((a2, n // 8))
            holes[i] = (a2 + n, b)
            want -= n
            break
    else:
        break
holes.sort(key=lambda h: h[1] - h[0], reverse=True)
dict_at.sort()

# ---- MTE codes: alias + high charcodes, contiguous runs ---------------------
def runs(codes):
    out = []
    for cc in sorted(codes):
        if out and cc == out[-1][0] + out[-1][1]:
            out[-1][1] += 1
        else:
            out.append([cc, 1])
    return [(a, n) for a, n in out]


# The redirect escapes are charcodes too, and they must be globally unused for
# the opposite reason to a glyph slot: the hook fires on the BYTES, so if another
# scenario legitimately writes that charcode its text would be redirected into
# our region. (The old banked range held 0x106E, which one scenario really does
# draw.) They have to share the 0xF7 lead byte, i.e. live in 0x1000-0x10FF, and
# the banks have to be consecutive because the hook range-checks them.
BANKS = BANK_COUNT
hi_runs = sorted(runs(free_high), key=lambda r: -r[1])
bank0 = next(a for a, n in hi_runs if n >= BANKS)
rest = [c for c in free_high
        if not (bank0 <= c < bank0 + BANKS)]
esc_cc, ret_cc = rest[0], rest[1]
escapes = {esc_cc, ret_cc} | set(range(bank0, bank0 + BANKS))
assert all(0x1000 <= c <= 0x10FF for c in escapes), "escapes must share the 0xF7 lead"
# The alias charcodes can be EITHER dictionary codes (no storage needed) or
# Hangul slots (storage supplied by tools/build_kr.py as extension pages in the
# grown overlay, reached through the stub's font-table swap). The charcode space
# is capped at 0x1100 by the stream encoding, so this really is a split, not a
# free expansion: every alias code handed to a glyph is one the dictionary loses.
# EXT_TARGET is sized from the syllable demand a fully translated script projects
# (~1,600) minus the slots that already own storage. It is read once, above, so
# the dictionary storage can be sized from the split it implies.
ext_codes = [c for c in free_alias if c not in escapes][:EXT_TARGET]
ext_ranges = runs(ext_codes)
mte_codes = [c for c in free_alias + free_high
             if c not in escapes and c not in set(ext_codes)]
code_ranges = runs(mte_codes)
code_cap = sum(n for _, n in code_ranges)
store_cap = sum(n for _, n in dict_at)
ext_blocks = sorted({c // 64 for c in ext_codes})
print(f"extension pages: {len(ext_codes)} Hangul slots in blocks {ext_blocks} "
      f"({len(ext_blocks)} x 0x900 = {len(ext_blocks)*0x900} B of region)")
for cc in escapes:
    assert cc not in used, f"escape charcode {cc:#x} is drawn {used[cc]}x ROM-wide"
    assert not any(a <= cc < a + n for a, n in code_ranges), "escape inside MTE range"
print(f"escapes: ESC 0x{esc_cc:04X}, RET 0x{ret_cc:04X}, "
      f"banks 0x{bank0:04X}-0x{bank0+BANKS-1:04X}")

# ---- glyph slots: everything else that owns storage ------------------------
resv = set()
spans = [(hook_at, hook_at + HOOK_BYTES), (stub_at, stub_at + STUB_BYTES),
         (code_tbl_at, code_tbl_at + CODE_TBL_BYTES),
         (store_tbl_at, store_tbl_at + STORE_TBL_BYTES),
         (code_region_at, code_region_at + CODE_REGION_BYTES)]
spans += [(a, a + n * 8) for a, n in dict_at]
for cc in range(4352):
    s, e = span(cc)
    if any(not (e <= lo or s >= hi) for lo, hi in spans):
        resv.add(cc)
slots = [cc for cc in free_storage if cc not in resv] + ext_codes
slots.sort()

print(f"\nhook      @0x{hook_at:08X} ({HOOK_BYTES} B)")
print(f"stub      @0x{stub_at:08X} ({STUB_BYTES} B)")
print(f"code tbl  @0x{code_tbl_at:08X} ({CODE_TBL_BYTES} B, {len(code_ranges)} ranges)")
print(f"store tbl @0x{store_tbl_at:08X} ({STORE_TBL_BYTES} B, {len(dict_at)} regions)")
print(f"code rgn  @0x{code_region_at:08X} ({CODE_REGION_BYTES} B, TINY_TBL at base)")
print(f"dict      {[(hex(a), n) for a, n in dict_at]} = {store_cap} entries")
print(f"MTE codes: {len(code_ranges)} ranges, {code_cap} codes "
      f"-> dictionary capacity {min(code_cap, store_cap)}")
print(f"Hangul glyph slots: {len(slots)} (0x{slots[0]:04X}-0x{slots[-1]:04X})")
assert 8 * (len(code_ranges) + 1) <= CODE_TBL_BYTES, "code table overflows"
assert 8 * (len(dict_at) + 1) <= STORE_TBL_BYTES, "store table overflows"

json.dump(slots, open(f"{OUT}/global_slots.json", "w"))
json.dump({"hook": hook_at, "hook_bytes": HOOK_BYTES, "stub": stub_at,
           "code_tbl": code_tbl_at, "store_tbl": store_tbl_at,
           "tiny_tbl": tiny_tbl_at,
           "code_region": [code_region_at, CODE_REGION_BYTES],
           "stub_bytes": STUB_BYTES, "code_tbl_bytes": CODE_TBL_BYTES,
           "store_tbl_bytes": STORE_TBL_BYTES,
           "dict_regions": dict_at, "code_ranges": code_ranges,
           "ext_ranges": ext_ranges, "ext_blocks": ext_blocks,
           "esc_cc": esc_cc, "ret_cc": ret_cc, "bank0_cc": bank0,
           "bank_count": BANK_COUNT,
           "glyph_slots": len(slots), "dict_capacity": min(code_cap, store_cap)},
          open(f"{OUT}/alloc_plan.json", "w"), indent=1)
print(f"\nwrote {OUT}/global_slots.json and alloc_plan.json")
print("\npaste into mte_hook.py:")
print(f"STUB = 0x{stub_at:08X}\nCODE_TBL = 0x{code_tbl_at:08X}\n"
      f"STORE_TBL = 0x{store_tbl_at:08X}")
print("CODE_RANGES = [" + ", ".join(f"(0x{a:04X}, {n})" for a, n in code_ranges) + "]")
print("EXT_RANGES = [" + ", ".join(f"(0x{a:04X}, {n})" for a, n in ext_ranges) + "]")
print("DICT_REGIONS = [" + ", ".join(f"(0x{a:08X}, {n})" for a, n in dict_at) + "]")
print(f"\npaste into redirect_hook.py:\nHOOK_ADDR = 0x{hook_at:08X}\n"
      f"TINY_TBL = 0x{tiny_tbl_at:08X}\n"
      f"ESC_CC = {esc_cc}\nRET_CC = {ret_cc}\nBANK0_CC = 0x{bank0:04X}")
