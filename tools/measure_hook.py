#!/usr/bin/env python3
"""Teach the ARM9 MEASUREMENT scanner what a redirect escape is really worth.

The problem (session 37, measured live)
---------------------------------------
The caller at 0x0203C8F8 does the same string twice:

    0x0203C978  measure  -> (charcode count, width in cells) on the stack
    0x0203C91C  MOV R2,R2,ASR#1 / BL 01FF995C   <- (width+1)>>1 makes the BOX
    0x0203C934  BL 0203CBC8                     <- the drawing worker

`menu_hook` already taught the *worker* about the escape, so it draws the whole
Korean. Nobody taught the *scanner*, which sees `F7 2E xx xx` as ordinary bytes
and returns a width of about 11 cells for a 25-cell line. The box is built to the
short number and the Korean is clipped inside it -- exactly the P1 choice-option
truncation, and the reason session 37 had to aim padding bytes (`aim_filler`) and
session 38 had to drop the 『』 brackets off the map line to buy one byte.

What this hook does
-------------------
Hooks the scanner's fetch at 0x0203C990, and on our escape lead:

  * WIDTH  (R4): add the region entry's REAL width, measured with the scanner's
    own rules (2-byte charcode +3, 0x00 +1, >=0xF7 +2), and consume the escape so
    the original path never adds the phantom width of the escape bytes.
    Exact, not generous: session 37's v118 made boxes merely WIDER and the extra
    cells showed the previous draw as a ghost, because the tile uploader only
    writes the cells it drew.

  * COUNT  (LR): add the PHANTOM count -- 1 for tiny, 2 for banked, 2 or 3 for
    the long form -- i.e. exactly what the untouched scanner would have counted
    for those bytes. ⚠⚠ THIS IS NOT AN OVERSIGHT. `menu_hook.cnt_done` does
    `sub r12, r12, lr; add r9, r9, r12`: it corrects the worker's loop bound by
    (real charcodes - phantom charcodes), and the phantom half of that only
    balances if the scanner still counted them. Making the count "correct" here
    would silently double-correct R9.

Register discipline (the two traps)
-----------------------------------
⚠⚠ LR IS THE COUNT ACCUMULATOR in this function (`MOV LR,#0` at 0x0203C97C), so
   a `BL` anywhere in the hook destroys it. No subroutine calls.
⚠  The function's prologue saves only {R3-R5,LR}; R6-R11 belong to the caller.
   The only genuinely free register is R12, so the hook pushes {R1,R2,R3,R5} and
   restores them on every exit path.

    python tools/measure_hook.py        # assemble and report size
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import redirect_hook as R

SITE = 0x0203C990                # LDRB R12, [R0], #1   (the scanner's fetch)
CONT = 0x0203C994                # CMP R12, #0xF8       (original next step)
LOOP_TEST = 0x0203C9F4           # CMP R4, R1 / BLT SITE
SITE_BYTES = bytes.fromhex("01c0d0e4")          # ldrb r12, [r0], #1
# Runaway guard for the entry walk. The caller's real limit is ~60 cells and the
# outer loop stops well before this, so hitting it means the entry is malformed
# rather than long -- stop rather than scan the whole region.
WIDTH_GUARD = 0xC0


def hook_addr():
    """Start of the space session 38 reclaimed from the MTE dictionary."""
    return R.CODE_FREE[0]


def _long_body():
    """The long escape, for the MEASUREMENT scanner.

    ⛔ SESSION 39. The long form is five bytes now and carries the entry's region
    offset in base 232, not a u16 table index (redirect_hook.off248). Because
    every base-232 digit is below 0xE8, an unhooked walker counts exactly
    `PHANTOM_LONG` charcodes for the escape -- so the `cmp r1,#0xE8` guess this
    block used to make is gone, and so is the table read.

    r0 was already post-incremented past the `F7` by the fetch, so the payload
    sits at [r0,#1..#3] and four more bytes are consumed. r1, r2, r3 and r5 are
    pushed by the caller; `lr` is the count accumulator and must survive.
    """
    if not R.OFFSET_ESC:
        return "\n        ".join([
            "ldrb  r2, [r0, #1]",
            "ldrb  r1, [r0, #2]",
            "orr   r2, r2, r1, lsl #8",
            "ldrb  r1, [r0, #1]",
            "cmp   r1, #0xE8",
            "movhs r3, #2",
            "movlo r3, #3",
            "add   r0, r0, #3",
        ])
    return "\n        ".join([
        "ldrb  r2, [r0, #3]",            # b2
        "mov   r5, r2, lsl #8",
        "sub   r5, r5, r2, lsl #4",
        "sub   r2, r5, r2, lsl #3",      # r2 = 232*b2
        "ldrb  r5, [r0, #2]",
        "add   r2, r2, r5",
        "mov   r5, r2, lsl #8",
        "sub   r5, r5, r2, lsl #4",
        "sub   r2, r5, r2, lsl #3",      # r2 = 232*(232*b2 + b1)
        "ldrb  r5, [r0, #1]",
        "add   r2, r2, r5",              # r2 = region offset
        f"mov   r3, #{R.PHANTOM_LONG}",
        f"add   r0, r0, #{R.LONG_BUDGET - 1}",
        f"{R.imm_chain('r1', R.RET_BASE)}",
        "add   r1, r1, r2",
        "add   lr, lr, r3",
        "b     walk",
    ])


def build(addr=None):
    addr = addr or hook_addr()
    code = f"""
        ldrb  r12, [r0], #1
        cmp   r12, #0x{R.ESC_B1:X}
        bne   plain
        stmdb sp!, {{r1, r2, r3, r5}}
        ldrb  r12, [r0]
        cmp   r12, #0x{R.RET_B2:X}
        beq   bail
        cmp   r12, #0x{R.ESC_B2:X}
        beq   do_long
        {R.imm_chain('r1', R.TINY_TBL)}
        ldrb  r1, [r1, r12]
        cmp   r1, #0x{R.TINY_NONE:X}
        beq   try_bank
        mov   r2, r1
        mov   r3, #1
        add   r0, r0, #1
        b     lookup
    try_bank:
        sub   r1, r12, #0x{R.BANK0_B2:X}
        cmp   r1, #{R.BANK_COUNT}
        bhs   bail
        ldrb  r2, [r0, #1]
        add   r2, r2, r1, lsl #8
        mov   r3, #2
        add   r0, r0, #2
        b     lookup
    do_long:
        {_long_body()}
    lookup:
        {R.imm_chain('r1', R.REGION_BASE)}
        ldr   r5, [r1, r2, lsl #2]
        add   r1, r1, r5
        add   lr, lr, r3
    walk:
        ldrb  r12, [r1], #1
        cmp   r12, #0x{R.ESC_B1:X}
        bne   wchar
        ldrb  r5, [r1]
        cmp   r5, #0x{R.RET_B2:X}
        beq   done
    wchar:
        cmp   r12, #0xE8
        addhs r1, r1, #1
        cmp   r12, #0
        addeq r4, r4, #1
        beq   wtest
        cmp   r12, #0xF7
        addlo r4, r4, #3
        addhs r4, r4, #2
    wtest:
        cmp   r4, #0x{WIDTH_GUARD:X}
        blo   walk
    done:
        ldmia sp!, {{r1, r2, r3, r5}}
        b     0x{LOOP_TEST:08X}
    bail:
        ldmia sp!, {{r1, r2, r3, r5}}
        mov   r12, #0x{R.ESC_B1:X}
    plain:
        b     0x{CONT:08X}
    """
    return R.asm(code, addr)


def install(rom: bytearray):
    a = hook_addr()
    blob = build(a)
    end = R.CODE_FREE[1]
    if a + len(blob) > end:
        raise SystemExit(f"measure hook ({len(blob)}B at 0x{a:08X}) overruns "
                         f"CODE_FREE end 0x{end:08X}")
    if a < R.TINY_TBL + 256:
        raise SystemExit("measure hook would overlap the tiny table")
    off = R.ram2rom(SITE)
    if bytes(rom[off:off + 4]) != SITE_BYTES:
        raise SystemExit(f"scanner site 0x{SITE:08X} is not the expected fetch "
                         f"(found {bytes(rom[off:off+4]).hex()})")
    rom[R.ram2rom(a):R.ram2rom(a) + len(blob)] = blob
    rom[off:off + 4] = R.asm(f"b 0x{a:08X}", SITE)
    return {"addr": a, "size": len(blob)}


if __name__ == "__main__":
    a = hook_addr()
    b = build(a)
    print(f"measure hook: {len(b)} B at 0x{a:08X} "
          f"(CODE_FREE ends 0x{R.CODE_FREE[1]:08X}, "
          f"{R.CODE_FREE[1] - a - len(b)} B spare)")
