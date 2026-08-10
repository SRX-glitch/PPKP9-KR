#!/usr/bin/env python3
"""Find who calls render_char (0x0203CCE8) -- i.e. the string printing loop.

We need to know whether the printer already has any expansion / substitution
mechanism (name insertion, macro codes). If it does, MTE is nearly free.
If not, MTE needs an ASM hook.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

ROM = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
rom = open(ROM, "rb").read()
u32 = lambda o: int.from_bytes(rom[o:o + 4], "little")
A9_OFF, A9_RAM, A9_SIZE = u32(0x20), u32(0x28), u32(0x2C)
RENDER_CHAR = 0x0203CCE8


def r2o(a):
    return a - A9_RAM + A9_OFF


def find_bl(target):
    """scan ARM9 static for BL instructions branching to target"""
    hits = []
    for o in range(A9_OFF, A9_OFF + A9_SIZE - 3, 4):
        w = u32(o)
        if (w >> 24) & 0x0F != 0x0B:          # BL (cond any, bits27-24 = 1011)
            continue
        imm = w & 0xFFFFFF
        if imm & 0x800000:
            imm -= 0x1000000
        pc = A9_RAM + (o - A9_OFF)
        tgt = pc + 8 + imm * 4
        if tgt == target:
            hits.append(pc)
    return hits


callers = find_bl(RENDER_CHAR)
print(f"BL -> render_char(0x{RENDER_CHAR:08X}) in ARM9 static: {len(callers)}")
for c in callers:
    print(f"  0x{c:08X}")

md = Cs(CS_ARCH_ARM, CS_MODE_ARM)


def dis(start, n):
    o = r2o(start)
    out = []
    for i in md.disasm(rom[o:o + n * 4], start):
        out.append(f"  {i.address:08X}  {i.mnemonic:<8} {i.op_str}")
    return "\n".join(out)


# find the enclosing function: walk back to a push
for c in callers[:3]:
    a = c
    for _ in range(400):
        a -= 4
        w = u32(r2o(a))
        if (w & 0x0FFF0000) == 0x092D0000:    # push {..}
            break
    print(f"\n===== printer function containing 0x{c:08X} -> starts 0x{a:08X} =====")
    print(dis(a, min((c - a) // 4 + 30, 110)))
