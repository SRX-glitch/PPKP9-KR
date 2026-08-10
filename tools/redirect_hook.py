#!/usr/bin/env python3
"""Text-redirect hook: lets a dialogue line point at a long Korean string stored
in the grown tail of overlay 28, bypassing the original byte budget.

WHICH TEXT PATH
---------------
The game has two of them and only the second draws Success dialogue:

  cutscene path -- ARM9 static handler 0x0203C834 -> scanner 0x0203C978 ->
      printer 0x0203CBC8. Walks a whole line per call. Used by the intro.
  gameplay path -- overlay 1 (mode overlay, file 5, loaded at 0x020BF5A0), a
      typewriter engine at 0x020BF958 that renders exactly ONE glyph per call.

Verified on the emulator: during real Success dialogue the ARM9 handler never
executes, and render_char's caller is 0x020BFBE0, inside the overlay engine. So
the hook goes in the engine; the cutscene path is left alone (intro lines fit
inline anyway, and its whole-line scanner cannot honour the return marker).

HOW THE REDIRECT WORKS
----------------------
`[r5+0x18]` is the engine's text cursor, reloaded at the top of every call and
committed back from `[r5+0x20]` at the end -- so it is effectively the script
cursor, and a naive redirect would strand script execution inside the region.
Each region entry therefore ends with a *return marker* that sends the cursor
back to the original stream:

    <dead filler so the marker lands 4-aligned>   <- before the text, never read
    <korean bytes>
    F7 <RET_B2> 00 00                <- RET marker (RET_CC, unused ROM-wide)
    <u32 return address>             <- 4-byte aligned; the original terminator

An over-budget line's inline bytes become `F7 <ESC_B2> <u16 index>` (ESC_CC),
padded to the original budget with the narrow 0x00 blank. The engine renders
one charcode per call, so the cursor lands exactly on the marker after the last
Korean glyph, the hook swaps it back to `line_start + budget`, and the script
resumes on its original terminator byte as if nothing happened.

Both markers use lead byte 0xF7, which is a *charcode* lead, not an opcode. That
matters: the script VM finds the end of an inline string by scanning for the next
byte >= 0xF8, so an opcode-range escape would make it resume execution on the
escape itself. Charcode escapes look like ordinary text to every scanner, so
stream advancement is bit-for-bit unchanged. Both charcodes are unused in the
entire ROM (tools/global_census.py), are not the canonical charcode of any game
character, and lie outside the font pack and the MTE code ranges, so neither can
occur naturally in any scenario.
"""
import os
import keystone

ENGINE_PATCH = 0x020BF960       # `ldr r2, [r5, #0x18]`
ENGINE_CONT = 0x020BF964        # next instruction
# The engine fetches the cursor from TWO places. The entry above runs once per
# call, but after an opcode handler returns 0 the engine loops back inside the
# same call and re-reads the cursor from `[r5+0x20]` here -- bypassing the entry
# patch entirely. An escape that sits immediately after such an opcode was
# therefore rendered RAW: `F7 77` printed as a stray halfwidth glyph and the two
# index bytes as kana, and the mangled box then derailed the next box's setup
# (the session-22 "cause #2" freeze in the Success Nice Guy scene). Both sites
# must redirect, so the loop gets its own hook.
ENGINE_LOOP_PATCH = 0x020BF9C8  # `ldr r2, [r5, #0x20]` (post-opcode loop head)
ENGINE_LOOP_CONT = 0x020BF9CC   # `ldrb r4, [r2]`
# The engine maps ONE glyph's tiles per call: at 0x020BFAE8 it writes exactly two
# tilemap columns x two rows (tile `(col & ~1) + (line % 6) * 0x3C + 1`, mask
# literal 0xFFFE at 0x020BFC90), and at the start of a line it clears both
# tilemap rows. So a call can only ever *show* the glyph it was asked to draw.
# The MTE stub used to loop render_char itself, which wrote the 2nd/3rd expansion
# glyph's pixels into tile memory at columns that were never mapped -- the glyph
# threading worked (the column advanced) but nothing appeared. MTE therefore has
# to expand at the *charcode* level instead: the decoded charcode is swapped for
# the entry's first glyph and the rest are injected one per engine call, so each
# one runs the engine's own tilemap, wrap and page-break code.
ENGINE_GLYPH_PATCH = 0x020BFA40  # `ldr r0, [r5, #0x34]`, charcode decoded in r4
ENGINE_GLYPH_CONT = 0x020BFA44   # `cmp r0, #0`
ENGINE_OV_RAM = 0x020BF5A0      # overlay 1 load address
ENGINE_OV_ROM = 0x000A6A00      # overlay 1 (file 5) ROM offset, uncompressed
# ---- allocator-owned addresses ----------------------------------------------
# ⛔ SESSION 39: TINY_TBL and CODE_REGION were hand-picked here and, audited
# against census v2, sat on ﾏﾐﾑﾒﾘﾙﾚﾛﾝｧｨ -- halfwidth katakana the ARM9
# player-name array draws (「ｸﾛｰﾊｰ」「ｾｷﾞﾉｰﾙ」「野球ﾏｽｸ」). They come from
# tools/alloc_plan.py now, and tools/verify_alloc.py fails the build if any of
# them lands on a glyph somebody draws.
import json as _json
_PLAN_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "survey", "font", "alloc_plan.json")
with open(_PLAN_PATH) as _f:
    _PLAN = _json.load(_f)

HOOK_ADDR = _PLAN["hook"]       # glyph storage no scenario draws (alloc_plan.py)
HOOK_MAX = 144 * 8              # bytes available at HOOK_ADDR
# Two words at the top of that block: [0] = the cursor the expansion belongs to
# (guard, so a stale expansion can never bleed into another box), [4] = pointer
# to the next expansion charcode, 0 when idle.
MTE_STATE = 0x02088A38          # last 8 B of the hook block
# ⭐ SLIM RETURN, second design. The entry used to end `F7 38 00 00` + a u32
# return address, 8 bytes per occurrence plus up to 3 bytes of alignment slack --
# 25% of a 487 KB region. It is now `F7 38` + a 3-BYTE OFFSET from OV28_RAM, read
# with three ldrb so no alignment is needed: 5 bytes, no slack.
#
# ⛔ The first attempt went further and dropped the address entirely, letting the
# hook stash `cursor + runlen` in a scratch word. It measured beautifully (region
# -28%, grow 0x7C000 -> 0x6C000) and it BROKE ON SCREEN: advancing with A was
# perfect, advancing with X (auto) turned whole boxes into kana soup. Traced live
# -- none of the three hooks' return paths were reached at all, and `[r5+0x20]`
# had ended up at 0x02085FEE, inside glyph storage, being drawn as text. Whatever
# consumes the script in that mode reaches the marker without having taken the
# matching escape, and a stateful return cannot survive that. Keep the address
# IN the entry: any walker that lands on the marker then recovers by itself.
SLIM = os.environ.get("PPKP9_SLIM_RET", "1") != "0"
# ⚠ These live BELOW MTE_STATE, in the slack between the hook code and it --
# MTE_STATE+8 is already the end of the reserved block (HOOK_ADDR + HOOK_MAX),
# so putting them above would write into glyph storage we never claimed.
# (the stateful-return scratch words are gone -- see the note above)

assert HOOK_ADDR % 4 == 0 and MTE_STATE % 4 == 0
assert HOOK_ADDR < MTE_STATE and MTE_STATE + 8 <= HOOK_ADDR + HOOK_MAX

# The grown overlay starts with the extension glyph pages (mte_hook.EXT_BLOCKS x
# 0x900), so the redirect region -- and every offset in its table -- begins after
# them. Both hooks build this address with mov/orr immediates, so it must stay
# expressible as a short chain; imm_chain asserts that.
EXT_PAGE_BYTES = len(_PLAN["ext_blocks"]) * 0x900   # == len(mte_hook.EXT_BLOCKS) * 0x900
REGION_BASE = 0x02253C00 + EXT_PAGE_BYTES
OV28_RAM = 0x021C0DC0           # overlay 28 load address
# ⭐ SESSION 39 -- THE RETURN ADDRESS IS RELATIVE TO MAIN RAM, NOT TO OVERLAY 28.
# The entry's return marker stores `ret - RET_BASE` as a u24. With RET_BASE =
# OV28_RAM that can only express addresses at or above overlay 28, which is fine
# while every redirect lives in the ov28/29/30 group -- all three load at
# 0x021C0DC0. It is NOT fine for the files whose text the menus draw:
#
#     f25 f4  f27   ov28 ov29 ov30   RAM 0x021C0DC0     <- the old assumption
#     f20 f18 f13   ov9  ov8  ov5    RAM 0x020CA020     <- BELOW it
#     f30           ov14            RAM 0x0216C3C0
#
# A file-20 return would be negative. Dropping the base to main RAM covers every
# overlay in one u24: the highest address any of them reaches is 0x02253C00,
# i.e. rel 0x253C00, and the grown ov28 tail 0x27B000 -- both far inside 24 bits.
# Costs nothing: the hooks build the base with imm_chain either way, and 0x02000000
# is a ONE-instruction immediate where 0x021C0DC0 took three.
RET_BASE = 0x02000000

# Both markers must be charcodes NO scenario draws, not just ones Nice Guy
# avoids: the hook fires on the bytes, so a scenario that legitimately writes the
# marker would have its own text redirected into our region. The old banked range
# held 0x106E, which one scenario really does draw. Re-picked by alloc_plan.py
# from the whole-ROM census; they stay in 0x1000-0x10FF so the lead byte is 0xF7.
ESC_CC = _PLAN["esc_cc"]        # redirect marker charcode, unused ROM-wide
RET_CC = _PLAN["ret_cc"]        # return marker charcode, unused ROM-wide
ESC_B1 = 232 + (ESC_CC - 256) // 256        # 0xF7, shared lead byte
ESC_B2 = (ESC_CC - 256) % 256               # 0x2E
RET_B2 = (RET_CC - 256) % 256               # 0x38

# A 3-byte escape for lines whose budget is exactly 3 -- 216 distinct lines /
# 897 occurrences, which the 4-byte form cannot reach at all. The index is split
# across a bank of consecutive marker charcodes (BANK0_CC.., all unused ROM-wide,
# not canonical for any character, and outside the MTE ranges): second byte picks the bank, third byte
# the entry, so capacity is BANK_COUNT * 256. Occurrences that need this form are
# allocated the low region indices so they stay addressable.
BANK0_CC = _PLAN["bank0_cc"]
BANK_COUNT = _PLAN["bank_count"]
BANK0_B2 = (BANK0_CC - 256) % 256           # 0xA3
SHORT_CAPACITY = BANK_COUNT * 256
# ⭐⭐ SESSION 39 -- THE LONG FORM CARRIES ITS OFFSET, NOT AN INDEX.
#
# The region is `[u32 offset table][entries]`. Measured on the shipping build the
# table is 18,103 slots = 72,412 B -- 4 bytes of REGION for every occurrence, on
# top of the 5-byte return marker. That table is the single largest overhead
# left, and the region is the thing `PPKP9_REGION_CAP` has to bound to keep the
# match from hanging (0x79000 ok / 0x7D000 hang), so it is paid for directly in
# lines that stay Japanese: capping at 0x76000 dropped 1,422 occurrences and the
# user saw 1,399 previously-Korean lines revert.
#
# The escape bytes live in the SCRIPT's existing run, not in the region. So
# growing the long form from 4 to 5 bytes costs zero region bytes, and in
# exchange the entry needs no table slot at all. Only tiny (2 B) and banked
# (3 B) still carry an index, and those are ~1,700 occurrences, so the table
# shrinks 72,412 -> ~6,900 B. Net +2,375 occurrences at 27.6 B each.
#
# Budget-4 runs used to be the smallest long-form users. They are not lost: the
# banked form is 3 bytes and its capacity is BANK_COUNT*256 = 2,560 against ~860
# in use, so they move there.
#
# ⚠ Every offset byte must be < 0xF8 for the same reason indices must be (see
# SAFE_STRIDE below). Base-248 makes that automatic and needs no lookup:
#     off = b0 + 248*(b1 + 248*b2),  248**3 = 15,252,992 >> the ~490 KB region.
OFFSET_ESC = os.environ.get("PPKP9_OFFSET_ESC", "1") != "0"
LONG_BUDGET = 5 if OFFSET_ESC else 4    # smallest budget the long form fits in
ESCAPE_LEN = LONG_BUDGET        # the long form; 3 for budget-3/4 lines
MIN_BUDGET = 3                  # below this a line cannot be redirected at all
# ⭐ BASE 232, NOT 248. Two constraints, not one:
#   * < 0xF8  -- the VM's inline-string scanner ends the string at the first
#                byte >= 0xF8 (the reason `safe_index` exists)
#   * < 0xE8  -- every text walker in the game treats 0xE8..0xF7 as the LEAD of a
#                two-byte charcode. With digits below 0xE8 each payload byte is a
#                one-byte charcode, so the number of charcodes an unhooked walker
#                would count for `F7 <ESC_B2> <b0> <b1> <b2>` is a CONSTANT 4.
#                That constant is what `menu_hook` and `measure_hook` subtract
#                when they correct the ARM9 printer's precomputed loop count; at
#                base 248 it would vary with the digit values and both hooks
#                would need the branchy decode the old u16 form had.
# 232**3 = 12,487,168, still far past the ~490 KB region.
OFF_BASE = 0xE8                 # 232
PHANTOM_LONG = 4                # charcodes an unhooked walker sees in the escape


def off248(off):
    """region offset -> 3 bytes, every one < 0xF8 (little-digit first)."""
    if not 0 <= off < OFF_BASE ** 3:
        raise ValueError(f"region offset {off} does not fit three base-248 digits")
    b0 = off % OFF_BASE
    b1 = (off // OFF_BASE) % OFF_BASE
    b2 = off // (OFF_BASE * OFF_BASE)
    return bytes([b0, b1, b2])


def un248(b):
    """the hook's arithmetic, in Python -- used by the gates"""
    return b[0] + OFF_BASE * (b[1] + OFF_BASE * b[2])

# ⭐ TWO-BYTE ESCAPE. A 2-byte run is exactly one Hangul syllable and nothing
# else -- even 「아！」 needs three -- so 64 lines were stuck at "translated but
# unshippable" with no way out. The 3-byte banked escape does not fit either.
# So spend a CHARCODE per line instead of an index: `F7 <b2>` where b2 alone
# names the region entry, looked up through a 256-byte table the hook owns.
# The F7 band has 256 codes, the ROM draws 41, we reserve 12 -- 203 spare, and
# the whole problem is 64 lines. Tiny entries take region indices 0..N-1, and
# safe_index(k) == k below 248, so the table can hold the index in one byte.
TINY_BUDGET = 2
# ⭐⭐ SESSION 38 -- MOVED OUT OF THE HOOK BLOCK. This used to be `MTE_STATE - 256`,
# i.e. it ate the last 256 B of the 1,152-byte hook allocation, and session 37
# concluded from that that a proper measurement hook (~160 B) "does not fit in the
# 48 B spare". The 48 B was this table's placement, not a shortage.
#
# There is genuinely NO free glyph space to move it into -- measured: global_slots
# has 1,687 charcodes >= 256, mte_hook reserves 264, and the Hangul pack takes the
# remaining 1,423 exactly, so zero aligned 576-byte regions are free or even
# reclaimable (the 91 KS X filler syllables are scattered, never 16 in a row).
# `hook_space.py`'s "11.8 KB free" is against usable_slots.json (2,078) with
# nothing subtracted; it is an upper bound, not free space.
#
# The space came from the MTE dictionary instead. `MAX_ENTRIES = min(CODE_CAP,
# STORE_CAP)` and the build is CODE-limited at 354, while DICT_REGIONS reserved
# 765 entries = 6,120 B. Over half of that storage is never written. Handing the
# 704-byte region at 0x02087D8C back (mte_hook.DICT_REGIONS) still leaves 677
# entry slots for a 354-entry dictionary -- 1.9x headroom.
TINY_TBL = _PLAN["tiny_tbl"]    # 256 B; 448 B left in the region for hook code
TINY_NONE = 0xFF                # "this b2 is not a tiny escape"
# What the reclaimed region is for, so nothing else quietly takes it.
CODE_REGION = tuple(_PLAN["code_region"])    # allocator-owned (alloc_plan.py)
CODE_FREE = (TINY_TBL + 256, CODE_REGION[0] + CODE_REGION[1])   # 448 B

# The escape stores its region index verbatim in the script stream (as the u16
# of the long form or the u8 of the banked form), so those index bytes are read
# by the VM's inline-string scanner, which ends a string at the first byte
# >= 0xF8. If any index byte is >= 0xF8 the scanner stops mid-escape and executes
# the rest as an opcode -- a hard derail into the scenario arena (observed as a
# "breakpoint" freeze at a fixed Success line). So only indices whose *every*
# byte is < 0xF8 are usable: 248 of every 256 low-byte values. safe_index maps
# the k-th occurrence to the k-th such index, leaving the 0xF8-0xFF holes unused.
SAFE_STRIDE = 0xF8              # low-byte values 0x00-0xF7 are safe


def safe_index(k):
    """k-th region index whose byte encoding contains no 0xF8+ byte."""
    return (k // SAFE_STRIDE) * 256 + (k % SAFE_STRIDE)


def _assert_safe(index):
    if (index & 0xFF) >= 0xF8 or (index >> 8) >= 0xF8:
        raise ValueError(f"redirect index {index:#06x} has a >=0xF8 byte; the VM "
                         f"scanner would derail -- use safe_index()")


def ram2rom(a):
    return a - 0x02000000 + 0x4000


def asm(code, addr):
    ks = keystone.Ks(keystone.KS_ARCH_ARM, keystone.KS_MODE_ARM | keystone.KS_MODE_LITTLE_ENDIAN)
    enc, _ = ks.asm(code, addr)
    return bytes(enc)


def imm_chain(reg, val):
    """`reg = val` as mov/orr immediates -- no literal pool beside the code.

    ARM data-processing immediates are an 8-bit value rotated by an even amount,
    so an arbitrary address needs a chain of them. Asserting the parts add back
    up to val is the whole correctness argument: keystone rejects any chunk it
    cannot encode, so a chain that assembles and sums is exact.
    """
    parts, v = [], val
    while v:
        sh = 0
        while not (v >> sh) & 1:
            sh += 1
        sh &= ~1                       # immediates rotate by an even count
        chunk = v & (0xFF << sh)
        parts.append(chunk)
        v &= ~chunk
    assert sum(parts) == val, f"{val:#x} decomposition lost bits"
    lines = [f"mov {reg}, #0x{parts[0]:X}"]
    lines += [f"orr {reg}, {reg}, #0x{p:X}" for p in parts[1:]]
    return "\n        ".join(lines)


def _long_decode():
    """ARM for the long escape's payload, leaving the region OFFSET in `ip`.

    Old form (u16 index): the payload is an index and `lookup:` turns it into an
    offset through the table. New form: the payload IS the offset, base-248, so
    this branches straight past the table read to `have_off`.

        off = b0 + 248*(b1 + 248*b2)      248 = 256 - 8, so x*248 = (x<<8)-(x<<3)

    Registers: `ip` accumulates, `lr` is scratch, `r2` still points at the escape
    and is only overwritten at `have_off`. `lr` is reloaded with REGION_BASE
    there, so clobbering it here is safe.
    """
    if not OFFSET_ESC:
        return ("ldrb ip, [r2, #2]\n        ldrb lr, [r2, #3]\n"
                "        orr  ip, ip, lr, lsl #8")
    return "\n        ".join([
        "ldrb ip, [r2, #4]",             # b2
        "mov  lr, ip, lsl #8",
        "sub  lr, lr, ip, lsl #4",
        "sub  ip, lr, ip, lsl #3",       # ip = 232*b2  (256-16-8)
        "ldrb lr, [r2, #3]",             # b1
        "add  ip, ip, lr",
        "mov  lr, ip, lsl #8",
        "sub  lr, lr, ip, lsl #4",
        "sub  ip, lr, ip, lsl #3",       # ip = 232*(232*b2 + b1)
        "ldrb lr, [r2, #2]",             # b0
        "add  ip, ip, lr",               # ip = offset
        # ⭐ SESSION 39: the payload is an offset from RET_BASE (main RAM), not
        # from REGION_BASE. REGION_BASE is one hardcoded address, so it can only
        # ever name a region inside the ov28/29/30 group -- overlays 8/9/14 sit
        # BELOW it and padding them up to it would run straight through ov28's
        # RAM. Main-RAM-relative lets every overlay keep its region in its OWN
        # tail and still be named by one escape form. 232**3 = 12.4M covers all
        # of main RAM's 4 MB.
        imm_chain("lr", RET_BASE),
        "b    have_off",
    ])


def build_hook():
    """ARM code for the engine hook.

    r2 is the value being produced; ip and lr are scratch (the engine pushed lr
    in its prologue at 0x020BF958 and returns via `pop {..., pc}`). r0/r1/r5 are
    live and untouched. No flags are consumed between the patch site and the
    engine's first `cmp`, so clobbering them is safe.

    It also carries the MTE injection, which has to run before the escape decode
    so that an expansion finishes before the next escape is looked at. When an
    expansion is pending for exactly this cursor the next charcode is loaded into
    r4 and the call jumps straight to the glyph path, skipping the cursor
    bookkeeping at 0x020BF964-0x020BF968: `[r5+0x20]` still holds the cursor from
    the call that consumed the MTE code, so the engine's epilogue re-commits the
    same value and the script does not move while the expansion plays out. r4 is
    dead here on every other path (the engine loads it at 0x020BF96C).

    REGION_BASE is built with mov/orr immediates rather than `ldr =`, so no
    literal pool is emitted beside the code (ARMv5TE has no movw/movt).
    """
    code = f"""
        ldr  r2, [r5, #0x18]
        {imm_chain('ip', MTE_STATE)}
        ldr  lr, [ip]
        cmp  lr, r2
        bne  esc
        ldr  lr, [ip, #4]
        cmp  lr, #0
        beq  esc
        ldrh r4, [lr], #2
        cmp  r4, #0
        bne  inject
        str  r4, [ip]
        str  r4, [ip, #4]
        b    esc
    inject:
        str  lr, [ip, #4]
        b    0x{ENGINE_GLYPH_PATCH:08X}
    esc:
        ldrb ip, [r2]
        cmp  ip, #0x{ESC_B1:X}
        bne  back
        ldrb ip, [r2, #1]
        cmp  ip, #0x{RET_B2:X}
        beq  ret
        cmp  ip, #0x{ESC_B2:X}
        beq  long
        {imm_chain('lr', TINY_TBL)}
        ldrb lr, [lr, ip]
        cmp  lr, #0x{TINY_NONE:X}
        movne ip, lr
        bne  lookup
        sub  ip, ip, #0x{BANK0_B2:X}
        cmp  ip, #{BANK_COUNT}
        bhs  back
        ldrb lr, [r2, #2]
        add  ip, lr, ip, lsl #8
        b    lookup
    long:
        {_long_decode()}
    lookup:
        {imm_chain('lr', REGION_BASE)}
        ldr  ip, [lr, ip, lsl #2]
    have_off:
        add  r2, lr, ip
        b    back
    ret:
        ldrb ip, [r2, #2]
        ldrb lr, [r2, #3]
        orr  ip, ip, lr, lsl #8
        ldrb lr, [r2, #4]
        orr  ip, ip, lr, lsl #16
        {imm_chain('r2', RET_BASE)}
        add  r2, r2, ip
    back:
        b    0x{ENGINE_CONT:08X}
    """
    return asm(code, HOOK_ADDR)


def build_hook2():
    """ARM code for the post-opcode loop hook.

    Same decode as build_hook, but the cursor comes from `[r5+0x20]` and the
    redirected pointer has to be stored back there: the engine re-reads
    `[r5+0x20]` a few instructions later to advance it, so leaving the new value
    only in r2 would advance the *old* cursor. Falls through to the loop's
    `ldrb r4,[r2]` untouched when the byte is not one of our markers.
    """
    code = f"""
        ldr  r2, [r5, #0x20]
        ldrb ip, [r2]
        cmp  ip, #0x{ESC_B1:X}
        bne  back
        ldrb ip, [r2, #1]
        cmp  ip, #0x{RET_B2:X}
        beq  ret
        cmp  ip, #0x{ESC_B2:X}
        beq  long
        {imm_chain('lr', TINY_TBL)}
        ldrb lr, [lr, ip]
        cmp  lr, #0x{TINY_NONE:X}
        movne ip, lr
        bne  lookup
        sub  ip, ip, #0x{BANK0_B2:X}
        cmp  ip, #{BANK_COUNT}
        bhs  back
        ldrb lr, [r2, #2]
        add  ip, lr, ip, lsl #8
        b    lookup
    long:
        {_long_decode()}
    lookup:
        {imm_chain('lr', REGION_BASE)}
        ldr  ip, [lr, ip, lsl #2]
    have_off:
        add  r2, lr, ip
        str  r2, [r5, #0x20]
        b    back
    ret:
        ldrb ip, [r2, #2]
        ldrb lr, [r2, #3]
        orr  ip, ip, lr, lsl #8
        ldrb lr, [r2, #4]
        orr  ip, ip, lr, lsl #16
        {imm_chain('r2', RET_BASE)}
        add  r2, r2, ip
        str  r2, [r5, #0x20]
    back:
        b    0x{ENGINE_LOOP_CONT:08X}
    """
    return asm(code, hook2_addr())


def hook2_addr():
    return HOOK_ADDR + ((len(build_hook()) + 3) & ~3)


def mte_addr():
    return hook2_addr() + ((len(build_hook2()) + 3) & ~3)


def build_mte_engine():
    """Expand an MTE dictionary code at the charcode level.

    Patched over `0x020BFA40 ldr r0,[r5,#0x34]`, i.e. after the engine has
    decoded the stream into a charcode (r4) and before it draws it. If r4 is an
    MTE code the same two tables the render_char stub walks (mte_hook's
    CODE_RANGES -> index, DICT_REGIONS -> entry) give the entry; r4 becomes the
    entry's first expansion charcode and the rest are parked in MTE_STATE for the
    engine-entry hook to inject, one per call. The engine then draws every
    expansion glyph through its own path, so each gets its tilemap, its wrap test
    and its page break -- which is exactly what looping inside render_char could
    not do.

    r0-r3 and ip are dead at the patch site (the glyph path reloads all of them
    from r5), and the tail restores the r0 the replaced instruction produced.
    Codes are only ever emitted for indices below MAX_ENTRIES, so the storage
    walk cannot run past the last region -- but it checks the terminator anyway,
    because falling off it would spin on a zero-sized region forever.
    """
    import mte_hook as M
    code = f"""
        bic  r0, r4, #0x8000
        cmp  r0, #0x{M.FAST_REJECT:X}
        blo  out
        {imm_chain('r1', M.CODE_TBL)}
        mov  r3, #0
    cwalk:
        ldr  r2, [r1, #4]
        cmp  r2, #0
        beq  out
        ldr  ip, [r1]
        subs ip, r0, ip
        blo  cnext
        cmp  ip, r2
        blo  cfound
    cnext:
        add  r3, r3, r2
        add  r1, r1, #8
        b    cwalk
    cfound:
        add  r3, r3, ip
        {imm_chain('r1', M.STORE_TBL)}
    swalk:
        ldr  r2, [r1, #4]
        cmp  r2, #0
        beq  out
        cmp  r3, r2
        blo  sfound
        sub  r3, r3, r2
        add  r1, r1, #8
        b    swalk
    sfound:
        ldr  r1, [r1]
        add  r1, r1, r3, lsl #3
        ldrh r0, [r1], #2
        cmp  r0, #0
        beq  out
        mov  r4, r0
        {imm_chain('r2', MTE_STATE)}
        ldr  r3, [r5, #0x20]
        str  r3, [r2]
        str  r1, [r2, #4]
    out:
        ldr  r0, [r5, #0x34]
        b    0x{ENGINE_GLYPH_CONT:08X}
    """
    return asm(code, mte_addr())


def _patch_site(rom, ram_addr, expect_src, target):
    """Replace one overlay-1 instruction with a branch to `target`."""
    off = ENGINE_OV_ROM + (ram_addr - ENGINE_OV_RAM)
    expect = asm(expect_src, ram_addr)
    if bytes(rom[off:off + 4]) != expect:
        raise SystemExit(f"overlay 1 site 0x{off:X} is not the expected "
                         f"`{expect_src}` (found {bytes(rom[off:off+4]).hex()})")
    rom[off:off + 4] = asm(f"b 0x{target:08X}", ram_addr)


def verify_reserved():
    """CODE_REGION must be off-limits to the glyph allocator, or a Hangul syllable
    lands on the tiny table and every `F7 <b2>` escape decodes with a garbage index
    -- session 35's flood, with a new cause. Cheap to check, catastrophic to miss.
    """
    import mte_hook as M
    lo, hi = CODE_REGION[0], CODE_REGION[0] + CODE_REGION[1]
    if not any(r_lo <= lo and hi <= r_hi for r_lo, r_hi in M.RESERVED_RAM):
        raise SystemExit(
            f"CODE_REGION 0x{lo:08X}-0x{hi:08X} is not inside "
            f"mte_hook.RESERVED_RAM -- build_fontpack would hand it to Hangul")
    for b, c in M.DICT_REGIONS:
        if b < hi and lo < b + c * 8:
            raise SystemExit(f"CODE_REGION overlaps DICT_REGIONS entry 0x{b:08X}")


def install(rom: bytearray):
    hook, hook2, mte = build_hook(), build_hook2(), build_mte_engine()
    a2, a3 = hook2_addr(), mte_addr()
    total = (a3 - HOOK_ADDR) + len(mte)
    if HOOK_ADDR + total > MTE_STATE:
        raise SystemExit(f"hooks {total}B run into MTE_STATE at 0x{MTE_STATE:08X}")
    rom[ram2rom(HOOK_ADDR):ram2rom(HOOK_ADDR) + len(hook)] = hook
    rom[ram2rom(a2):ram2rom(a2) + len(hook2)] = hook2
    rom[ram2rom(a3):ram2rom(a3) + len(mte)] = mte
    # ⛔⛔ SESSION 35: THIS WRITE WAS MISSING AND EVERY BUILD SINCE THE BANKED
    # ESCAPE SHIPPED WITH IT MISSING. `build_tiny_table()` existed and was never
    # called, so TINY_TBL held untouched ARM9 static data -- measured identical in
    # the pristine ROM, the session-30 deploy ROM and v78, with **zero** 0xFF bytes.
    # The hook checks the tiny table BEFORE the banked range (see `esc:` above), so
    # a non-0xFF byte there makes every `F7 <b2>` escape decode as a 2-byte tiny
    # escape with a garbage index. Observed on hardware: 「へえ・・・」's neighbour
    # `F7 A4 E4` (banked, index 484 = 「어머？」) read as tiny index 0 = 「아～」, and
    # since that entry returns to 0x002346 the engine resumed at the TOP OF THE
    # SCRIPT and printed 「なかなか」「寝つけないなあ・・・。」. It also consumed 2 bytes
    # of a 3-byte escape, so the stream desynced -- that is the garbage flood.
    # `region verify` cannot see this: it walks with the writer's knowledge of which
    # form each escape used, while the ENGINE dispatches tiny-first. Use
    # `verify_escapes.py`, which mimics the dispatch order instead.
    tiny = build_tiny_table()
    # The table now lives in its own reclaimed region, so the gate is that region,
    # not the hook block. It must still be a span nothing else writes -- that is
    # `mte_hook.RESERVED_RAM`'s job, and `verify_reserved()` checks it holds.
    if not (CODE_REGION[0] <= TINY_TBL
            and TINY_TBL + len(tiny) <= CODE_REGION[0] + CODE_REGION[1]):
        raise SystemExit(f"tiny table 0x{TINY_TBL:08X}+{len(tiny)} does not fit "
                         f"its region 0x{CODE_REGION[0]:08X}+{CODE_REGION[1]}")
    verify_reserved()
    rom[ram2rom(TINY_TBL):ram2rom(TINY_TBL) + len(tiny)] = tiny
    rom[ram2rom(MTE_STATE):ram2rom(MTE_STATE) + 8] = b"\x00" * 8
    # the engine lives in an overlay, so patch that file, not ARM9 static
    _patch_site(rom, ENGINE_PATCH, "ldr r2, [r5, #0x18]", HOOK_ADDR)
    _patch_site(rom, ENGINE_LOOP_PATCH, "ldr r2, [r5, #0x20]", a2)
    _patch_site(rom, ENGINE_GLYPH_PATCH, "ldr r0, [r5, #0x34]", a3)
    return total


def escape_bytes(index, budget=4, offset=None):
    """Inline escape for a redirect.

    budget 2      tiny   `F7 <b2>`                     index via TINY_TBL
    budget 3-4    banked `F7 <bank> <entry>`           index in the escape
    budget >= 5   long   `F7 <ESC_B2> <o0> <o1> <o2>`  OFFSET in the escape,
                                                       base-248, no table slot

    `offset` is the entry's byte offset from REGION_BASE and is required for the
    long form. Under PPKP9_OFFSET_ESC=0 the old 4-byte u16-index form is emitted
    instead, for A/B against a build that predates this change.
    """
    if budget == TINY_BUDGET:
        return tiny_escape(index)
    if budget < MIN_BUDGET:
        raise ValueError(f"budget {budget} cannot hold any escape")
    if budget < LONG_BUDGET:
        _assert_safe(index)
        if not 0 <= index < SHORT_CAPACITY or index >> 8 >= BANK_COUNT:
            raise ValueError(f"index {index} needs the long form but the line "
                             f"only has {budget} bytes; allocate it a lower index")
        return bytes([ESC_B1, BANK0_B2 + (index >> 8), index & 0xFF])
    if not OFFSET_ESC:
        _assert_safe(index)
        if not 0 <= index < 0x10000:
            raise ValueError(f"redirect index {index} out of range")
        return bytes([ESC_B1, ESC_B2, index & 0xFF, index >> 8])
    if offset is None:
        raise ValueError("the long form needs the entry's region offset")
    return bytes([ESC_B1, ESC_B2]) + off248(offset)


def build_region(entries, n_indexed=None, ram_base=None):
    """Lay out the redirect region.

    entries: list of (encoded_korean, return_ram_addr) -- one per *occurrence*,
    because the return address is where that particular occurrence sits in the
    script.

    Returns (region_bytes, offsets). `offsets[k]` is entry k's byte offset from
    REGION_BASE -- the long escape stores it verbatim, so the table only has to
    cover the first `n_indexed` entries (the tiny and banked forms).
    """
    if SLIM:
        return _build_region_slim(entries, n_indexed, ram_base)
    n = len(entries)
    # The hook indexes the offset table by the *safe* index that the escape
    # stores, so the table must be sized to the largest safe index and carry
    # holes at the 0xF8-0xFF slots (those are never emitted, so never read).
    tbl_slots = safe_index(n - 1) + 1 if n else 0
    table = bytearray(4 * tbl_slots)
    body = bytearray()
    base = 4 * tbl_slots
    offsets = []
    for k, (text, ret) in enumerate(entries):
        # The marker's return address is read with a single aligned ldr, so the
        # marker has to start on a 4-byte boundary -- but the slack that buys
        # goes BEFORE the text, not after it. Filler after the text sits between
        # the last Korean charcode and the marker, so the engine renders it: up
        # to three blank glyphs (36px) at the end of every redirected run, which
        # is mid-sentence whenever another run follows on the same line. Before
        # the text it is dead space no one ever reads -- the offset table points
        # past it -- and it costs exactly the same bytes.
        while (base + len(body) + len(text)) % 4:
            body.append(0)
        off = base + len(body)
        offsets.append(off)
        si = safe_index(k)
        table[4 * si:4 * si + 4] = off.to_bytes(4, "little")
        body += text
        assert len(body) % 4 == 0, "RET marker lost 4-byte alignment"
        body += bytes([ESC_B1, RET_B2, 0, 0]) + ret.to_bytes(4, "little")
    return bytes(table + body), offsets


_TINY_B2 = None


def tiny_codes():
    """Second bytes of F7-band charcodes NO scenario draws, minus our markers.

    Read from the whole-ROM census, so a code the game really renders can never
    be handed out -- that is the mistake the old banked range made with 0x106E.
    """
    global _TINY_B2
    if _TINY_B2 is None:
        import json as _j, os as _o
        # ⛔⛔⛔⛔ SESSION 39, THE THIRD TIME THIS CENSUS WAS TOO NARROW.
        # This read `global_usage.json`, which counts `F8 6B` DIALOGUE only. The
        # ARM9 player-name arrays draw halfwidth katakana, and every one of those
        # is a 0xF7-band charcode -- `ｼ` is `F7 3E`, `ﾀ` is `F7 42`. Fifteen of
        # them were handed out as tiny escape codes. Nothing broke while
        # `menu_hook` was off, because only the overlay-1 dialogue engine
        # consulted TINY_TBL and it never draws those arrays. Turn the ARM9
        # printer hook on and the lineup screen reads `ｼ` in a player name, finds
        # a live tiny index, jumps into the region and corrupts R9 -- the whole
        # screen came back as scrambled tiles (v155/156/157, `_states_s39/
        # v156_lineup.png`).
        # census v2 counts array/packed/ime as well, so those codes are excluded.
        p = _o.path.join(_o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))),
                         "survey", "font", "census_v2_usage.json")
        drawn = {int(k) for k in _j.load(open(p, encoding="utf-8"))}
        ours = {ESC_CC, RET_CC} | {BANK0_CC + i for i in range(BANK_COUNT)}
        # ⛔⛔ SESSION 35, SECOND ROOT CAUSE. `global_usage.json` is a census of
        # what the ORIGINAL ROM draws. MTE dictionary codes are ours, added long
        # after that census, so the census cannot see them -- and 103 of
        # `mte_hook.CODE_RANGES` sit in this very band (0x1039/0x10AD/0x10D8/
        # 0x10F1). Every one of them was ALSO handed out as a tiny escape, so a
        # line using such a dictionary code emitted `F7 <b2>` and the engine
        # swallowed it as a redirect and jumped to an unrelated region entry --
        # "a completely different conversation appears out of nowhere", measured
        # as 392 runs on v79. Two allocators were quietly sharing one code space.
        import mte_hook as _M
        ours |= {b + i for b, c in _M.CODE_RANGES for i in range(c)}
        # ⛔⛔⛔ SESSION 36, THE OTHER HALF OF THE SAME MISTAKE. Session 35 taught
        # this census about the codes WE invented (MTE). It still knew nothing
        # about the codes we simply START USING: `global_usage.json` says which
        # charcodes the ORIGINAL ROM draws, and a half-width Latin letter the
        # Japanese script never printed reads as "free" -- while our Korean
        # prints it. Every one of those is in this band, so it encodes as
        # `F7 <b2>` and the engine eats it as a redirect.
        #   'T' 0x106E -> b2 0x6E, drawn by the original, correctly reserved
        #   'V' 0x1070 -> b2 0x70, NOT drawn by the original, handed out as tiny
        # 「TV에서 몇 번 본 적이 있어。」 therefore drew 「T」, was swallowed on 「V」,
        # jumped to an unrelated region entry, poured out a screenful of kana and
        # then never reached a message terminator -- an empty text box the player
        # cannot advance. Measured on v104/v106; the ROM bytes were perfect and
        # `scan_runs` read them back perfectly, because the fault is in who owns
        # the code, not in what we wrote.
        # The fix is the same shape as session 35's: ask the OTHER allocator.
        # Here that is the shipped font map -- every charcode any translation can
        # emit -- so the two allocators stop sharing one code space.
        _ours_font = _o.path.join(
            _o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))),
            "survey", "font", "kr_map.json")
        try:
            _km = _j.load(open(_ours_font, encoding="utf-8"))
            for _key in ("syl", "mte"):
                for _cc in _km.get(_key, {}).values():
                    ours.add(int(_cc))
        except (OSError, ValueError):
            pass
        # …and the base table, for the characters a translation copies straight
        # through (Latin, digits, the punctuation the Japanese script happens not
        # to use). `poketbl` is the same table the encoders resolve against.
        import poketbl as _P
        ours |= {cc for cc in _P.CH2CC.values() if 0x1000 <= cc <= 0x10FF}
        _TINY_B2 = [c - 4096 for c in range(0x1000, 0x1100)
                    if c not in drawn and c not in ours]
        # The invariant, asserted where the allocation happens rather than
        # re-derived by a stream walker later: a tiny code may never be a
        # charcode anything can emit. Checking it here cannot false-positive on
        # 0xF7 bytes that are merely the SECOND half of a 2-byte charcode, which
        # is the trap every "scan the written text" version of this check fell
        # into while it was being written.
        _emit = {int(cc) for k in ("syl", "mte")
                 for cc in _km.get(k, {}).values()} if "_km" in dir() else set()
        _emit |= set(_P.CH2CC.values())
        _clash = sorted({b for b in _TINY_B2 if (b + 4096) in _emit})
        assert not _clash, (
            "tiny escape codes collide with emittable charcodes: "
            + ", ".join(f"F7 {b:02X}" for b in _clash[:8]))
    return _TINY_B2


def build_tiny_table():
    """b2 -> region index, TINY_NONE elsewhere. Tiny entries are indices 0..N-1."""
    tbl = bytearray([TINY_NONE] * 256)
    for k, b2 in enumerate(tiny_codes()):
        if k >= TINY_NONE:
            break
        tbl[b2] = k
    return bytes(tbl)


def tiny_escape(index):
    codes = tiny_codes()
    if not 0 <= index < min(len(codes), TINY_NONE):
        raise ValueError(f"tiny index {index} out of range ({len(codes)} codes)")
    return bytes([ESC_B1, codes[index]])


def _build_region_slim(entries, n_indexed=None, ram_base=None):
    """`[text][F7 38][u24 offset from RET_BASE]` -- 5 B, no alignment.

    `n_indexed` is how many LEADING entries still need a table slot: the tiny and
    banked forms carry an index, the long form carries its offset. Callers must
    therefore order the entries so every index-carrying one comes first. Passing
    None keeps the old behaviour (a slot for every entry).

    Returns (region_bytes, esc_off) -- `esc_off[k]` is what the LONG escape
    stores for entry k: its address minus RET_BASE. `ram_base` is where this
    region will live in main RAM (REGION_BASE for the ov28 group). The table the
    tiny/banked forms index still holds plain byte offsets from the region start.
    """
    n = len(entries)
    if n_indexed is None or not OFFSET_ESC:
        n_indexed = n
    tbl_slots = safe_index(n_indexed - 1) + 1 if n_indexed else 0
    table = bytearray(4 * tbl_slots)
    body = bytearray()
    base = 4 * tbl_slots
    offsets = []
    for k, (text, ret) in enumerate(entries):
        rel = ret - RET_BASE
        if not 0 <= rel < (1 << 24):
            raise SystemExit(f"return 0x{ret:08X} is outside overlay 28")
        off = base + len(body)
        offsets.append(off + (ram_base - RET_BASE) if ram_base is not None else off)
        if k < n_indexed:
            si = safe_index(k)
            table[4 * si:4 * si + 4] = off.to_bytes(4, "little")
        body += text + bytes([ESC_B1, RET_B2]) + rel.to_bytes(3, "little")
    return bytes(table + body), offsets


if __name__ == "__main__":
    import capstone
    md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)
    blobs = [("hook", build_hook(), HOOK_ADDR),
             ("hook2", build_hook2(), hook2_addr()),
             ("mte", build_mte_engine(), mte_addr())]
    print(f"escape charcode {ESC_CC} -> {ESC_B1:02X} {ESC_B2:02X} + u16 index")
    print(f"return charcode {RET_CC} -> {ESC_B1:02X} {RET_B2:02X} + u32 address")
    print(f"budget: 0x{HOOK_ADDR:08X}..0x{MTE_STATE:08X} "
          f"({MTE_STATE - HOOK_ADDR} B), state @0x{MTE_STATE:08X}")
    for name, blob, addr in blobs:
        print(f"\n{name}: {len(blob)} bytes @0x{addr:08X}")
        for i in md.disasm(blob, addr):
            print("  %08X  %-8s %s" % (i.address, i.mnemonic, i.op_str))
