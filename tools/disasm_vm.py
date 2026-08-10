#!/usr/bin/env python3
"""Disassemble the gameplay text engine in overlay 1 to read the opcode dispatch.

Overlay 1: RAM 0x020BF5A0, ROM 0xA6A00, uncompressed (per session 19).
Engine entry 0x020BF958. Bytes >= 0xF8 in the script stream are opcodes; we want
the code that decides how far the cursor advances for each one.
"""
import sys
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB

BASE = r"C:/Users/jngji/Desktop/실험실"
ROM = open(f"{BASE}/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds", "rb").read()

OV1_RAM, OV1_ROM = 0x020BF5A0, 0xA6A00
r2f = lambda a: OV1_ROM + (a - OV1_RAM)

start = int(sys.argv[1], 16) if len(sys.argv) > 1 else 0x020BF958
count = int(sys.argv[2]) if len(sys.argv) > 2 else 120
mode = CS_MODE_THUMB if (len(sys.argv) > 3 and sys.argv[3] == "t") else CS_MODE_ARM

md = Cs(CS_ARCH_ARM, mode)
off = r2f(start)
data = ROM[off:off + count * 4]
for ins in md.disasm(data, start):
    print(f"{ins.address:#010x}  {ins.bytes.hex():<8}  {ins.mnemonic:<8} {ins.op_str}")
