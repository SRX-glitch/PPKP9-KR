#!/usr/bin/env python3
"""Statically disassemble the font routines out of the ROM (ARM9 uncompressed).
RAM addr -> ROM offset = ram - 0x02000000 + 0x4000
"""
import sys
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB

ROM = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
rom = open(ROM, "rb").read()


def r2o(a):
    return a - 0x02000000 + 0x4000


def dis(start, n=120, thumb=False):
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB if thumb else CS_MODE_ARM)
    md.detail = False
    off = r2o(start)
    code = rom[off:off + n * 4]
    out = []
    for i in md.disasm(code, start):
        out.append(f"{i.address:08X}  {i.bytes.hex():<8}  {i.mnemonic:<8} {i.op_str}")
        if len(out) >= n:
            break
    return "\n".join(out)


if __name__ == "__main__":
    targets = [("render_char", 0x0203CCE8, 130), ("render_glyph", 0x0203CECC, 90),
               ("codec", 0x0203CFA4, 70)]
    if len(sys.argv) > 1:
        targets = [("custom", int(sys.argv[1], 16), int(sys.argv[2]) if len(sys.argv) > 2 else 80)]
    for name, addr, n in targets:
        print(f"\n===== {name} @ {addr:08X} (ROM {r2o(addr):06X}) =====")
        print(dis(addr, n))
