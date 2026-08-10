#!/usr/bin/env python3
"""Teach the ARM9 string drawer about our redirect escape.

There are TWO text walkers in this game. The dialogue engine in overlay 1 is the
one `redirect_hook` patches. The other lives in ARM9 static at **0x0203CBC8**,
takes `(…, R2 = charcode count, R3 = text pointer)` and is what draws menus,
FF-terminated tables and **choice options**:

    0203CC04  LDRB R0,[R8],#1     <- the fetch; this is what we hook
    0203CC08  CMP  R0,#F8
    0203CC0C  BCC  0203CC2C       <- anything under 0xF8 is treated as a charcode
    0203CC10  …CMPEQ R0,#5A       <- it understands exactly one opcode, F8 5A
    0203CC80  BL   0203CCE8       <- render_char
    0203CC90  CMP  R7,R9 / BLT    <- COUNT-bounded loop, no terminator

Our escape lead `F7` is *below* 0xF8, so this walker decoded `F7 2E lo hi` as
charcodes and drew three stray kana -- 「단축한다」 came out 「ヴごん」. That is why
session 29 banned redirects inside choice blocks, and the ban cost 430 lines.

Observed, not inferred: breakpoint on render_char with an A/B choice on screen
returned LR = 0x0203CC84, i.e. this loop (savestate /root/v16_choice.dss).

⚠ The count is the hard part. R9 bounds the loop and there is no terminator, so
redirecting has to raise it: the entry's charcodes are counted here at runtime
and the phantom charcodes the escape bytes would have produced are subtracted,
so the walker draws the Korean and then resumes the original stream exactly
where it would have.

Registers: the function pushes {R3-R11,LR}, so R0, R1, R12 and LR are scratch at
the fetch (R0/R1 are dead -- both are re-loaded further down the loop).
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import redirect_hook as R

SITE = 0x0203CC04                # LDRB R0,[R8],#1
CONT = 0x0203CC08                # CMP R0,#F8


def hook_addr():
    """First free word after redirect_hook's own three blobs."""
    a = R.mte_addr() + len(R.build_mte_engine())
    return (a + 3) & ~3


def _long_body():
    """The long escape, for THIS walker.

    ⛔ SESSION 39. This used to read a u16 index out of `[r8,#2..3]`, consume 4
    bytes, and guess the phantom charcode count with `cmp r0,#0xE8`. The long form
    is now FIVE bytes and its payload is the entry's region offset in base 232
    (redirect_hook.off248), so:

      * there is no table lookup -- the offset goes straight into r1
      * every payload digit is < 0xE8, so an unhooked walker would have counted
        exactly PHANTOM_LONG charcodes for the escape. No branchy guess.

    Registers: r0, r1, r12 and lr are the scratch this fetch site allows.
    """
    if not R.OFFSET_ESC:
        return "\n        ".join([
            "ldrb r12, [r8, #2]",
            "ldrb r0, [r8, #3]",
            "orr  r12, r12, r0, lsl #8",
            "ldrb r0, [r8, #2]",
            "cmp  r0, #0xE8",
            "movhs lr, #2",
            "movlo lr, #3",
            "add  r8, r8, #4",
        ])
    return "\n        ".join([
        "ldrb r1, [r8, #4]",             # b2
        "mov  r0, r1, lsl #8",
        "sub  r0, r0, r1, lsl #4",
        "sub  r1, r0, r1, lsl #3",       # r1 = 232*b2
        "ldrb r0, [r8, #3]",
        "add  r1, r1, r0",
        "mov  r0, r1, lsl #8",
        "sub  r0, r0, r1, lsl #4",
        "sub  r1, r0, r1, lsl #3",       # r1 = 232*(232*b2 + b1)
        "ldrb r0, [r8, #2]",
        "add  r1, r1, r0",               # r1 = region offset
        f"mov  lr, #{R.PHANTOM_LONG}",
        f"add  r8, r8, #{R.LONG_BUDGET}",
        f"{R.imm_chain('r0', R.RET_BASE)}",
        "b    have_ent",
    ])


def build(addr=None):
    addr = addr or hook_addr()
    code = f"""
        ldrb r0, [r8]
        cmp  r0, #0x{R.ESC_B1:X}
        bne  plain
        ldrb r0, [r8, #1]
        cmp  r0, #0x{R.RET_B2:X}
        beq  do_ret
        cmp  r0, #0x{R.ESC_B2:X}
        beq  do_long
        {R.imm_chain('r1', R.TINY_TBL)}
        ldrb r1, [r1, r0]
        cmp  r1, #0x{R.TINY_NONE:X}
        beq  try_bank
        mov  r12, r1
        mov  lr, #1
        add  r8, r8, #2
        b    lookup
    try_bank:
        sub  r0, r0, #0x{R.BANK0_B2:X}
        cmp  r0, #{R.BANK_COUNT}
        bhs  plain
        ldrb r12, [r8, #2]
        add  r12, r12, r0, lsl #8
        mov  lr, #2
        add  r8, r8, #3
        b    lookup
    do_long:
        {_long_body()}
    lookup:
        {R.imm_chain('r0', R.REGION_BASE)}
        ldr  r1, [r0, r12, lsl #2]
    have_ent:
        add  r8, r0, r1
        mov  r1, r8
        mov  r12, #0
    cnt:
        ldrb r0, [r1]
        cmp  r0, #0x{R.ESC_B1:X}
        bne  cnt_adv
        ldrb r0, [r1, #1]
        cmp  r0, #0x{R.RET_B2:X}
        beq  cnt_done
        mov  r0, #0x{R.ESC_B1:X}
    cnt_adv:
        cmp  r0, #0xE8
        addhs r1, r1, #2
        addlo r1, r1, #1
        add  r12, r12, #1
        b    cnt
    cnt_done:
        sub  r12, r12, lr
        add  r9, r9, r12
        b    plain
    do_ret:
        ldrb r0, [r8, #2]
        ldrb r1, [r8, #3]
        orr  r0, r0, r1, lsl #8
        ldrb r1, [r8, #4]
        orr  r0, r0, r1, lsl #16
        {R.imm_chain('r8', R.RET_BASE)}
        add  r8, r8, r0
    plain:
        ldrb r0, [r8], #1
        b    0x{CONT:08X}
    """
    return R.asm(code, addr)


def install(rom: bytearray):
    a = hook_addr()
    blob = build(a)
    # ⭐ SESSION 38: the limit is MTE_STATE again. TINY_TBL used to sit in the last
    # 256 B of this block and that is where "only 48 B spare" came from; it now
    # lives in redirect_hook.CODE_REGION, so the spare is ~304 B here plus 448 B
    # there. (Historic note kept below because the failure it describes is real if
    # anyone moves TINY_TBL back.)
    # ⚠ The limit WAS TINY_TBL, not MTE_STATE: the 256-byte tiny-escape table sat
    # between them (session 35 -- it is a real table now, it used to be left
    # unwritten). Growing into it silently breaks every `F7 <b2>` escape.
    if a + len(blob) > R.MTE_STATE:
        raise SystemExit(f"menu hook ({len(blob)}B at 0x{a:08X}) runs into "
                         f"MTE_STATE at 0x{R.MTE_STATE:08X}")
    off = R.ram2rom(SITE)
    expect = R.asm("ldrb r0, [r8], #1", SITE)
    if bytes(rom[off:off + 4]) != expect:
        raise SystemExit(f"ARM9 site 0x{SITE:08X} is not the expected fetch "
                         f"(found {bytes(rom[off:off+4]).hex()})")
    rom[R.ram2rom(a):R.ram2rom(a) + len(blob)] = blob
    rom[off:off + 4] = R.asm(f"b 0x{a:08X}", SITE)
    return {"addr": a, "size": len(blob)}


if __name__ == "__main__":
    a = hook_addr()
    b = build(a)
    print(f"menu hook: {len(b)} B at 0x{a:08X} "
          f"(MTE_STATE 0x{R.MTE_STATE:08X}, {R.MTE_STATE - a - len(b)} B spare)")
