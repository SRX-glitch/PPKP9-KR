#!/usr/bin/env python3
"""Audit every F8 subcode handler and say WHICH declared widths are trustworthy.

survey/ov28/opcode_lengths.json was produced by counting `str [state,#0x20]`
stores in each handler and stopping at the first return.  That estimate is only
valid for handlers that consume a fixed number of immediate bytes on a straight
line.  It is silently wrong when a handler

    * loops (backward branch)          -> the cursor moves a variable distance
    * stores the cursor conditionally  -> width depends on runtime state
    * calls out (bl/blx)               -> the callee may consume more
    * writes an absolute cursor value  -> it is a JUMP, not a width

A wrong width desyncs every linear walker: the byte after the opcode gets read
as text, the extracted run starts one byte early, and re-inserting it overwrites
opcode bytes -- i.e. control-flow damage that no string-level gate can see.

This does not guess a corrected width; it classifies each handler so the ones
that need runtime measurement (0x020C0858 -> 0x020C0894) are known.

Usage:
    python3 opcode_audit.py <ram.bin>            # RAM image from dst_ram.py
"""
import sys, os, json, struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = 0x02000000
TABLE_PTR = 0x020C08CC
NSUB = 0x70
OV1_LO, OV1_HI = 0x020BF5A0, 0x020BF5A0 + 0x60000

md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
md.detail = False


CONDS = ("eq", "ne", "lt", "ge", "gt", "le", "hi", "ls", "cs", "cc", "mi", "pl", "vs", "vc")


def analyse(ram, fn, limit=64, depth=0, seen=None):
    """Classify one handler, following calls. Returns (stores, flags, ninsn).

    `stores` counts writes to state+0x20 (the script cursor).  Following BL/BLX
    matters because the original estimator stopped at the handler boundary, so
    any argument consumed inside a callee was invisible to it.
    """
    seen = seen if seen is not None else set()
    if fn in seen or depth > 3 or not (OV1_LO <= fn < OV1_HI):
        return 0, ({"deep-call"} if depth > 3 else set()), 0
    seen.add(fn)
    off = fn - BASE
    data = ram[off:off + limit * 4]
    state = {"r0"}
    stores = 0
    flags = set()
    n = 0
    for ins in md.disasm(data, fn):
        n += 1
        m, ops = ins.mnemonic, ins.op_str
        if m.startswith("mov") and "," in ops:
            dst, src = [x.strip() for x in ops.split(",")[:2]]
            if src in state:
                state.add(dst)
            elif dst in state:
                state.discard(dst)
        if m.startswith("str") and any(f"[{r}, #0x20]" in ops for r in state):
            stores += 1
            if m[3:5] in CONDS:
                flags.add("cond-store")
        if m.startswith("bl"):
            flags.add("call")
            try:
                tgt = int(ops.strip(), 16)
            except ValueError:
                flags.add("indirect-call")
            else:
                # only the state pointer in r0 lets a callee touch the cursor
                s2, f2, _ = analyse(ram, tgt, limit, depth + 1, seen)
                stores += s2
                flags |= {f for f in f2 if f != "call"}
        if m.startswith("b") and not m.startswith("bl") and not m.startswith("bx"):
            try:
                tgt = int(ops.strip(), 16)
            except ValueError:
                pass
            else:
                if tgt <= ins.address:
                    flags.add("loop")
        if m.startswith("bx") or (m.startswith("pop") and "pc" in ops) or \
           (m.startswith("ldm") and "pc" in ops):
            break
    return stores, flags, n


def main():
    ram = open(sys.argv[1], "rb").read()
    u32 = lambda a: struct.unpack_from("<I", ram, a - BASE)[0]
    table = u32(TABLE_PTR)
    lens = json.load(open(os.path.join(HERE, "..", "survey", "ov28", "opcode_lengths.json")))
    declared = {int(k): v for k, v in lens["f8"].items()}

    print(f"subcode table @ 0x{table:08x}\n")
    print(f"{'sub':>4} {'handler':>10} {'decl':>4} {'stores':>6}  flags")
    suspect = []
    for s in range(NSUB):
        fn, adj = u32(table + s * 8), u32(table + s * 8 + 4)
        if adj & 1:
            print(f" {s:02X}  {'(virtual)':>10} {declared.get(s, '-'):>4}")
            suspect.append((s, "virtual"))
            continue
        if not (OV1_LO <= fn < OV1_HI):
            print(f" {s:02X}  0x{fn:08x} {declared.get(s, '-'):>4}   OUT-OF-RANGE")
            suspect.append((s, "out-of-range"))
            continue
        stores, flags, n = analyse(ram, fn)
        derived = 2 + stores
        note = []
        if flags:
            note.append("+".join(sorted(flags)))
        if declared.get(s) != derived:
            note.append(f"decl!={derived}")
        print(f" {s:02X}  0x{fn:08x} {declared.get(s, '-'):>4} {stores:>6}  {' '.join(note)}")
        if flags & {"loop", "call", "cond-store"} or declared.get(s) != derived:
            suspect.append((s, " ".join(note)))

    print(f"\n=== {len(suspect)} subcode(s) whose declared width is NOT trustworthy")
    for s, why in suspect:
        print(f"  F8 {s:02X}  {why}")


if __name__ == "__main__":
    main()
