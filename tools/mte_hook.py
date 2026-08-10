#!/usr/bin/env python3
"""MTE (dictionary) expansion hook for the PPKP9 text renderer.

render_char @0x0203CCE8 draws one glyph per charcode. We patch its first
instruction (push) to `b STUB`. For a charcode that is an MTE *code* the stub
looks up a dictionary entry (<=3 expansion charcodes, 0-terminated) and calls
render_char recursively for each -- threading the glyph column (r2 in, r0 out).
Expansion charcodes are real glyphs, so they pass straight back to the original
code: recursion depth 1.

Both the MTE code space AND the dict storage are fragmented (the game already
uses most high charcodes and most alias-block glyph storage). So the stub uses
two (base,count) tables it walks at runtime:
  CODE_RANGES  -- contiguous runs of charcodes verified UNUSED by any `F8 6B`
                  text (tools/true_census.py). Concatenated, they define idx.
  DICT_REGIONS -- glyph-storage RAM spans verified unused, holding the entries.
Growing capacity later is a data edit (add a range/region), no code change.

A fast reject (cc < 0xC00 -> original) keeps normal glyph rendering cheap; only
charcodes at/above the first code range walk the table.

EVERY path that falls through to the original code must leave r0, r1 and r2
exactly as they arrived -- render_char reads all three (`movs r6,r0 / mov r5,r1 /
mov r4,r2`), and the stub sits in front of every glyph the game draws, not just
MTE codes. Two ways that was violated, both of them silent text loss:

  * `bic r0,r0,#0x8000` before the reject. The engine encodes a 1-byte charcode
    as `cc | 0x8000` and render_char masks it off itself, but `movs r6,r0 / bne`
    reads r0 == 0 as "draw nothing" -- so clearing the flag turned charcode 0,
    which is あ, blank everywhere in the game (the session-20 "blank あ"). The
    masked value now lives in ip and r0 is never written.
  * the range walk using r1 and r3 as scratch. A charcode >= FAST_REJECT that is
    *not* an MTE code walks the whole table and then falls through -- with r1,
    render_char's destination pointer, holding `cc - range_base`. The glyph was
    blitted to a junk address, i.e. nowhere: 82 kanji whose charcodes sit above
    0xC00 (話 練 理 力 料 連 立 良 ...) never appeared, 1,691 times in the corpus.
    That is what the session-20 "blank 連" was; the walk now uses r5/r8, which
    the prologue saved, and r1/r2 are only touched once an entry is certain.
"""
import os
import json
import keystone

RENDER_CHAR = 0x0203CCE8

# ---- every address and charcode range below comes from tools/alloc_plan.py ---
# ⛔ SESSION 39: these used to be literals pasted in by hand, and re-split
# incrementally by tools/plan_ext_trade.py starting from whatever was already
# here. They drifted. Audited against census v2, the shipped build had:
#     DICT_REGIONS  9 of 12 regions on drawn glyphs -- ｵｶｸｻｼｽｾｿ ｯｬｭ ﾀﾄﾊﾋﾍ 　x15
#     CODE_REGION   on ﾏﾐﾑﾒﾘﾙﾚﾛﾝｧｨ
#     STUB          on 刹
# Those halfwidth katakana and fullwidth spaces are what the ARM9 player-name
# array draws, so the MTE dictionary was writing its entries straight over
# 「ｾｷﾞﾉｰﾙ」「ｸﾛｰﾊｰ」「鈴木　」. That is the tile garbage in the session-38 lineup
# screenshot, and it is a SEPARATE bug from the census one.
#
# Reading the plan instead of copying it makes that class of drift impossible:
# there is one allocator, one census behind it, and tools/verify_alloc.py fails
# the build if any of it lands on a glyph somebody draws.
_PLAN_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "survey", "font", "alloc_plan.json")
with open(_PLAN_PATH) as _f:
    _PLAN = json.load(_f)

STUB = _PLAN["stub"]        # stub code + the extension path
STUB_MAX = _PLAN["stub_bytes"]
CODE_TBL = _PLAN["code_tbl"]        # 8 B per range + terminator
EXT_TBL = CODE_TBL + 0x100  # same 512 B allocation, second half
STORE_TBL = _PLAN["store_tbl"]      # 8 B per dict region + terminator
FAST_REJECT = 0xC00         # charcodes below this are never MTE codes

# ---- extension glyph pages --------------------------------------------------
# The charcode space stops at 0x1100, so the only way to give Hangul more slots
# is to use the alias-block charcodes (0x0DC0-0x0FFF) -- which have no glyph
# storage of their own, since blocks 55-63 all alias block 0. build_kr lays 0x900
# storage pages for them at the front of the grown overlay, and the stub points
# the font table at the right page for the duration of one render_char call.
#
# The swap has to be temporary. The same alias blocks hold 37 charcodes that
# OTHER scenarios really draw (36 of them outside Nice Guy), and those must keep
# resolving to block 0 -- which they do, because they are not in EXT_RANGES and
# so never take this path. Leaving the table repointed would break them, and the
# pages are not even resident when another scenario is loaded.
EXT_BASE = 0x02253C00       # grown overlay start; pages sit before the region
EXT_BLOCK0 = 55             # first alias block == 0x0DC0 >> 6
EXT_STATE = 0x02088A30      # 8 B scratch in the redirect hook's block
FONT_TABLE = 0x0208EFC8     # == fontcodec.FONT_TABLE_RAM
# ⚠ 85 charcodes that used to live here were handed to CODE_RANGES in session 30
# (0x0F0E+17, 0x0F20+17, 0x0F46+25, 0x0F60+11, 0x0F6C+15). The alias charcode
# space is FULL, so more MTE codes can only come out of this list -- and the ones
# to give up are the TOP of it: build_fontpack fills `extra` in ascending charcode
# order from a priority-ordered syllable list, so the highest extension slots hold
# the LOWEST-priority KS X 1001 filler (밍 섣 톡 뻤 측 …), which no translation uses.
# After the trade: 335 glyph slots, and 1238 + 335 = 1573 mapped syllables against
# the 1,276 that real translations actually need.
#
# ⚠⚠ The cut was chosen so all SEVEN pages (blocks 55-61) keep at least one
# charcode. Emptying a block would change len(EXT_BLOCKS), and that moves
# redirect_hook.EXT_PAGE_BYTES and REGION_BASE with it -- i.e. it relays the whole
# redirect region. `(0x0F32, 45)` is therefore split rather than taken whole:
# `(0x0F32, 20)` stays so block 61 still owns 0x0F40-0x0F45.
EXT_RANGES = [tuple(r) for r in _PLAN["ext_ranges"]]
# ⚠ SESSION 39: this list is now the allocator's, sized by PPKP9_EXT_TARGET
# (default 420). It used to be hand-split by `tools/plan_ext_trade.py`, which
# started from whatever literal was already here -- and census v2 finds 3 of
# those 185 charcodes (にわぃ) genuinely drawn.
# ⛔ DIAGNOSTIC (session 35): `PPKP9_NO_EXT=1` empties this list, which stops the
# stub swapping FONT_TABLE to the extension pages. Those pages live at EXT_BASE =
# the GROWN OVERLAY 28's front, so they are only resident while overlay 28 is --
# and the match is the one place it may not be. Suspected cause of "the game
# freezes entering the batter's box", which reproduces on the shipped v0.9 deploy
# and survived MTE_MAX=0 and a lower grow. Hangul that needed an extension slot
# will render wrong in this build; the ONLY question it answers is whether the
# match still hangs.
if os.environ.get("PPKP9_NO_EXT") == "1":
    EXT_RANGES = []
EXT_BLOCKS = sorted({cc // 64 for b, c in EXT_RANGES for cc in range(b, b + c)})
EXT_CODES = [cc for b, c in EXT_RANGES for cc in range(b, b + c)]

# contiguous UNUSED charcode runs used as MTE codes (verified by true_census).
# Scenario-scoped (Nice Guy only): charcodes/regions unused by file25+intro are
# free, even if other scenarios use them. From tools/scenario_census.py.
# ⚠ Re-derived from scenario_census2.py after the corpus fix. The previous values
# -- (0x0C97,140), (0x0D24,813), (0x107A,134) -- were computed from the truncated
# corpus and overran into charcodes that really do render (0xCC0-0xCDA, 0xD24-0xDA7,
# 0x1018-0x1050), so the hook was expanding real kanji as dictionary entries.
# Re-derived from scenario_census2.py (corrected corpus). The old values
# (0x0C97,140),(0x0D24,813),(0x107A,134) overran into 41 charcodes that really
# render (dominated by the gaiji-decode 尅), expanding them as dictionary entries.
# ⚠ MUST stay sorted ascending: an unsorted permutation of this exact set crashes
# the intro (pc=0x0F000000) -- see the E/G/H isolation in RESUME. build_stub()
# asserts sortedness so a future edit can't silently reintroduce it.
# What EXT_RANGES does not take: the alias codes above the extension pages plus
# the high band. Every alias code is either a glyph slot or a dictionary code --
# the charcode space is full, so this is a split, not a choice of both.
# ★ Session 30: the first five ranges were TAKEN FROM EXT_RANGES (see the note
# there). 222 codes was the binding limit on the whole patch -- storage had 765
# slots and only 222 could be addressed -- and it is why 611 choice options
# shipped in Japanese: a choice has no redirect fallback, so it needs an MTE entry
# or nothing, and the 222 went to higher-weight lines first. Cost of the trade is
# 85 KS X filler glyphs nothing uses.
CODE_RANGES = [tuple(r) for r in _PLAN["code_ranges"]]
# ⚠ SESSION 39: allocator-owned, like EXT_RANGES -- the two are one split of the
# same alias/high charcode space. Census v2 finds 4 of the previous 354 literals
# (ゅぜらぃ) genuinely drawn.
# ⛔⛔ SESSION 35: the four spans that used to close this list -- (0x1039,24)
# (0x10AD,42) (0x10D8,24) (0x10F1,13), 103 codes -- were REMOVED. They sit at
# charcode >= 0x1000, so they encode as `F7 xx`, and `F7` is the redirect escape
# lead. `redirect_hook.tiny_codes()` hands out F7-band codes the ORIGINAL ROM
# never draws, and its census cannot see codes we invented afterwards, so all 103
# were handed out twice -- once as a dictionary code, once as a tiny escape. A
# line using such a code was swallowed as a redirect and the engine jumped to an
# unrelated region entry: "a completely different conversation out of nowhere",
# measured as 392 mangled runs on v79.
# ⚠ Relocating them BELOW 0x1000 instead is the better trade (it would keep both
# 457 dictionary entries and 203 tiny codes) but it is not safe to do from
# `global_usage.json` alone: the free-looking runs there overlap 0xCC0-0xCDA and
# 0xD24-0xDA7, which the note above records as charcodes that REALLY RENDER --
# the exact mistake that made the hook expand real kanji in session 30. Redo it
# from `scenario_census2.py`, not from the global census.
# free glyph-storage RAM spans (unused by Nice Guy), holding dict entries (8 B).
# ⚠ 0x02075DDC is NOT here: it hosts the text-redirect hook (redirect_hook.py).
# Capacity stays 1087 either way -- the dictionary is code-limited, not storage-
# limited (1087 codes vs 1728 slots), so giving the region up costs nothing.
# Likewise re-derived: the old spans held glyphs for characters the truncated
# corpus never saw. These are the census's free RAM runs, minus 0x02075DDC (the
# redirect hook) and 0x02082F1C (this stub).
# Re-derived from scenario_census2.py, sorted ascending, excluding 0x02075DDC
# (redirect hook) and 0x02082F1C (this stub). The old spans held glyphs for
# characters the truncated corpus never counted, which is why 39 real chars were
# clobbered. 720 slots > 904? no -- code-limited stays at min = 720 entries.
DICT_REGIONS = [tuple(r) for r in _PLAN["dict_regions"]]
# ⛔⛔ SESSION 39: the previous literal list had NINE of its twelve regions on
# glyphs that are really drawn -- ｵｶｸｻｼｽｾｿ, ｯｬｭ, ﾀﾄﾊﾋﾍ, 廣 苳 麓 禄 蕾 唔, and
# fifteen copies of the fullwidth space the name array pads with. The dictionary
# wrote its entries over them, which is why 「ｾｷﾞﾉｰﾙ」 and the whole upper lineup
# came out as tile garbage.
# ⭐ The allocator now sizes this to the MTE code count instead of a flat 6 KB.
# The dictionary is CODE-limited, so storage beyond the code count was never
# written -- and it was paid for in Hangul slots, because every charcode whose
# interleaved bytes touch a reserved span is one the font pack cannot use.
CODE_REGION = tuple(_PLAN["code_region"])   # == redirect_hook.CODE_REGION
# Previous known-good (pre-corpus-fix): (0x0208705C,864),(0x0206881C,432),
#   (0x0206D25C,288),(0x0206815C,144)  # 1728, but overlapped 39 real glyphs
CODE_CAP = sum(c for _, c in CODE_RANGES)
STORE_CAP = sum(c for _, c in DICT_REGIONS)
MAX_ENTRIES = min(CODE_CAP, STORE_CAP)
# Session 38 took a dictionary region for hook code on the grounds that this build
# is CODE-limited. If that ever stops being true the dictionary shrinks silently
# and lines lose their compression with nothing in the log to say why.
assert STORE_CAP >= CODE_CAP, (
    f"MTE storage ({STORE_CAP}) now caps the dictionary below its code space "
    f"({CODE_CAP}) -- give redirect_hook.CODE_REGION back to DICT_REGIONS")

# Every span the patch writes into glyph storage. The redirect hook's block is
# here too: it is not ours to hand out as a Hangul slot, and leaving it out is
# what let two drawn charcodes get overwritten before.
HOOK_RAM = (0x020885C4, 1152)   # == redirect_hook.HOOK_ADDR / HOOK_MAX
RESERVED_RAM = ([(STUB, STUB + STUB_MAX),
                 (CODE_TBL, CODE_TBL + 8 * 64),
                 (STORE_TBL, STORE_TBL + 8 * 24),
                 (HOOK_RAM[0], HOOK_RAM[0] + HOOK_RAM[1]),
                 # Reclaimed from DICT_REGIONS for the tiny table + hook code.
                 # It leaves this list ONLY when it goes back to DICT_REGIONS --
                 # drop it from both and build_fontpack hands it to Hangul, which
                 # would put a syllable's glyph on top of the tiny table.
                 (CODE_REGION[0], CODE_REGION[0] + CODE_REGION[1])]
                + [(b, b + c * 8) for b, c in DICT_REGIONS])


def ram2rom(a):
    return a - 0x02000000 + 0x4000


def assemble(code, addr):
    ks = keystone.Ks(keystone.KS_ARCH_ARM, keystone.KS_MODE_ARM | keystone.KS_MODE_LITTLE_ENDIAN)
    enc, _ = ks.asm(code, addr)
    return bytes(enc)


def _check_sorted():
    """CODE_RANGES must be ascending and non-overlapping: an unsorted permutation
    of the same charcode set crashes the intro (E/G/H isolation, RESUME)."""
    prev = -1
    for base, count in CODE_RANGES:
        assert base > prev, f"CODE_RANGES must be sorted ascending: {hex(base)} after {hex(prev)}"
        prev = base + count - 1
    prev = -1
    for base, count in DICT_REGIONS:
        assert base > prev, f"DICT_REGIONS must be sorted ascending: {hex(base)} after {hex(prev)}"
        prev = base + count * 8 - 1


_check_sorted()


def build_stub():
    asm = f"""
        push {{r4, r5, r6, r7, r8, lr}}
        bic  ip, r0, #0x8000
        cmp  ip, #0x{FAST_REJECT:X}
        blo  orig
        ldr  r6, =0x{CODE_TBL:08X}
        mov  r8, #0
    cwalk:
        ldr  r7, [r6, #4]
        cmp  r7, #0
        beq  ext
        ldr  r5, [r6]
        subs r5, ip, r5
        blo  cnext
        cmp  r5, r7
        blo  cfound
    cnext:
        add  r8, r8, r7
        add  r6, r6, #8
        b    cwalk
    cfound:
        add  r8, r8, r5
        ldr  r6, =0x{STORE_TBL:08X}
    swalk:
        ldr  r7, [r6, #4]
        cmp  r7, #0
        beq  orig
        cmp  r8, r7
        blo  sfound
        sub  r8, r8, r7
        add  r6, r6, #8
        b    swalk
    sfound:
        ldr  r6, [r6]
        add  r6, r6, r8, lsl #3
        mov  r4, r1
        mov  r5, r2
    loop:
        ldrh r0, [r6], #2
        cmp  r0, #0
        beq  done
        mov  r1, r4
        mov  r2, r5
        bl   0x{RENDER_CHAR:08X}
        mov  r5, r0
        b    loop
    done:
        mov  r0, r5
        pop  {{r4, r5, r6, r7, r8, pc}}
    ext:
        ldr  r6, =0x{EXT_TBL:08X}
    ewalk:
        ldr  r7, [r6, #4]
        cmp  r7, #0
        beq  orig
        ldr  r5, [r6]
        subs r5, ip, r5
        blo  enext
        cmp  r5, r7
        blo  efound
    enext:
        add  r6, r6, #8
        b    ewalk
    efound:
        mov  r5, ip, lsr #6
        ldr  r7, =0x{FONT_TABLE:08X}
        add  r7, r7, r5, lsl #2
        sub  r5, r5, #{EXT_BLOCK0}
        mov  r6, #0x900
        mul  r6, r5, r6
        ldr  r5, =0x{EXT_BASE:08X}
        add  r6, r5, r6
        ldr  r5, [r7]
        str  r6, [r7]
        ldr  r6, =0x{EXT_STATE:08X}
        stmia r6, {{r5, r7}}
        adr  lr, eback
        push {{r4, r5, r6, r7, r8, lr}}
        b    0x{RENDER_CHAR + 4:08X}
    eback:
        ldr  r6, =0x{EXT_STATE:08X}
        ldmia r6, {{r5, r7}}
        str  r5, [r7]
        pop  {{r4, r5, r6, r7, r8, pc}}
    orig:
        b    0x{RENDER_CHAR + 4:08X}
    """
    return assemble(asm, STUB)


def build_code_table():
    blob = bytearray()
    for base, count in CODE_RANGES:
        blob += base.to_bytes(4, "little") + count.to_bytes(4, "little")
    blob += b"\x00" * 8
    return bytes(blob)


def build_store_table():
    blob = bytearray()
    for base, count in DICT_REGIONS:
        blob += base.to_bytes(4, "little") + count.to_bytes(4, "little")
    blob += b"\x00" * 8
    return bytes(blob)


def build_ext_table():
    blob = bytearray()
    for base, count in EXT_RANGES:
        blob += base.to_bytes(4, "little") + count.to_bytes(4, "little")
    blob += b"\x00" * 8
    return bytes(blob)


def code_for(i):
    """dictionary index i -> its MTE charcode."""
    for base, count in CODE_RANGES:
        if i < count:
            return base + i
        i -= count
    raise IndexError


def entry_addr(i):
    for base, count in DICT_REGIONS:
        if i < count:
            return base + i * 8
        i -= count
    raise IndexError


def pack_entry(ccs):
    assert 1 <= len(ccs) <= 3, ccs
    codeset = set()  # expansion charcodes must be real glyphs, never MTE codes
    row = bytearray()
    for cc in ccs:
        assert 0 < cc < 0x8000, cc
        for b, c in CODE_RANGES:
            assert not (b <= cc < b + c), f"expansion {cc:#x} is itself an MTE code"
        row += cc.to_bytes(2, "little")
    row += b"\x00" * (8 - len(row))
    return bytes(row)


def apply(rom: bytearray, entries):
    n = len(entries)
    assert n <= MAX_ENTRIES, f"{n} > {MAX_ENTRIES}"
    stub = build_stub()
    assert len(stub) <= STUB_MAX, f"stub {len(stub)}B > {STUB_MAX}"
    rom[ram2rom(RENDER_CHAR):ram2rom(RENDER_CHAR) + 4] = assemble(
        f"b 0x{STUB:08X}", RENDER_CHAR)
    rom[ram2rom(STUB):ram2rom(STUB) + len(stub)] = stub
    ct, st, et = build_code_table(), build_store_table(), build_ext_table()
    assert len(ct) <= EXT_TBL - CODE_TBL, "code table runs into the ext table"
    assert len(et) <= 0x100, "ext table overflows its half of the allocation"
    rom[ram2rom(CODE_TBL):ram2rom(CODE_TBL) + len(ct)] = ct
    rom[ram2rom(EXT_TBL):ram2rom(EXT_TBL) + len(et)] = et
    rom[ram2rom(STORE_TBL):ram2rom(STORE_TBL) + len(st)] = st
    for i, e in enumerate(entries):
        a = entry_addr(i)
        rom[ram2rom(a):ram2rom(a) + 8] = pack_entry(e)
    return {"stub_bytes": len(stub), "dict_entries": n, "capacity": MAX_ENTRIES,
            "code_ranges": len(CODE_RANGES), "dict_regions": len(DICT_REGIONS)}


def reserved_charcodes(font_table):
    """Charcodes the hook consumes: dict-storage glyph slots + all MTE codes."""
    out = set()
    for cc in range(4352):
        addr = font_table[cc // 64] + ((cc & 0x30) >> 4) * 576
        if any(lo <= addr < hi for lo, hi in RESERVED_RAM):
            out.add(cc)
    for b, c in CODE_RANGES:
        out |= set(range(b, b + c))
    return out


if __name__ == "__main__":
    s = build_stub()
    print(f"stub: {len(s)} bytes (budget {STUB_MAX})")
    print(f"code cap {CODE_CAP}, store cap {STORE_CAP} -> {MAX_ENTRIES} entries")
    print(f"code0 for idx0 = 0x{code_for(0):04X}, idx {MAX_ENTRIES-1} = 0x{code_for(MAX_ENTRIES-1):04X}")
