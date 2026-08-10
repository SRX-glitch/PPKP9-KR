#!/usr/bin/env python3
"""Derive the full script-opcode length table from the VM code in overlay 1.

Engine 0x020BF958: a byte >= 0xF8 is an opcode; the cursor lives at state+0x20.
  0x020C06AC  dispatch: >= 0xFA -> jump table (FA..FF); < 0xFA (F8/F9) ->
  0x020C0858  consume one subcode byte, index an 8-byte-entry table at 0x020C3950,
              and call entry.fn (Itanium ptr-to-member; field+4 bit0 = virtual).

Each handler consumes its own arguments with
    ldr rX,[state,#0x20] / add rY,rX,#1 / str rY,[state,#0x20] / ldrb ..,[rX]
Handlers receive the state in r0 (some copy it to r4), so we track the register
holding it and count the cursor stores until the first return.
"""
import os, sys, struct, json
sys.path.insert(0, os.path.dirname(__file__))
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

BASE = r"C:/Users/jngji/Desktop/실험실"
ROM = open(f"{BASE}/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds", "rb").read()
OV1_RAM, OV1_ROM, OV1_END = 0x020BF5A0, 0xA6A00, 0x020BF5A0 + 0x60000
r2f = lambda a: OV1_ROM + (a - OV1_RAM)
u32 = lambda a: struct.unpack_from("<I", ROM, r2f(a))[0]

TABLE = u32(0x020C08CC)
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)


def arg_bytes(fn, limit=48):
    """Script bytes consumed by this handler before it returns."""
    data = ROM[r2f(fn):r2f(fn) + limit * 4]
    state = {"r0"}            # registers currently holding the state pointer
    n = 0
    for ins in md.disasm(data, fn):
        m, ops = ins.mnemonic, ins.op_str
        # track copies of the state pointer
        if m == "mov" and "," in ops:
            dst, src = [x.strip() for x in ops.split(",")[:2]]
            if src in state:
                state.add(dst)
            elif dst in state and src not in state:
                state.discard(dst)
        if m.startswith("str") and any(f"[{r}, #0x20]" in ops for r in state):
            n += 1
        if m in ("bx", "pop") and ("pc" in ops or "lr" in ops):
            break
    return n


# The table ends at 0x70: that entry is ASCII from a nearby file-path string, not
# a function pointer. So 0x00-0x6F are the only real subcodes, and any F8 subcode
# above 0x6F encountered while walking means the walk has desynced.
NSUB = 0x70
lens = {}
for s in range(NSUB):
    fn, adj = u32(TABLE + s * 8), u32(TABLE + s * 8 + 4)
    if (adj & 1) or not (OV1_RAM <= fn < OV1_END):
        continue                      # virtual - inspect by hand
    lens[s] = 2 + arg_bytes(fn)

BARE = {0xFA: 1, 0xFB: 1, 0xFC: 3, 0xFD: 3, 0xFE: 3, 0xFF: 1}

print(f"dispatch table @ {TABLE:#010x};  {len(lens)} F8/F9 subcodes resolved\n")
print("bare opcodes (from the FA..FF jump table):")
for op, n in BARE.items():
    note = "u16 arg" if n == 3 else "no arg"
    print(f"  {op:02X}      {n} byte(s)   {note}")

print("\nF8/F9 subcode lengths (total opcode size incl. the F8 and subcode bytes):")
by_len = {}
for s, n in sorted(lens.items()):
    by_len.setdefault(n, []).append(s)
for n in sorted(by_len):
    codes = " ".join(f"{s:02X}" for s in by_len[n])
    print(f"  {n} bytes ({len(by_len[n]):3d} subcodes): {codes}")

out = {"table": TABLE, "bare": BARE, "f8": lens}
dst = f"{BASE}/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/ov28/opcode_lengths.json"
json.dump(out, open(dst, "w"), indent=1)
print(f"\nwrote {dst}")
