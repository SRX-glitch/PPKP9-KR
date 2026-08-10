#!/usr/bin/env python3
"""Validate the opcode length table by walking overlay 28's script end to end.

If the lengths are right the walk stays in sync: every step lands on either a
decodable charcode or a known opcode. Desync shows up immediately as an unknown
F8 subcode or as an unmapped charcode in the middle of a text run.

Also re-extracts dialogue the right way -- following inline control codes instead
of stopping at them -- and diffs the result against the old corpus.
"""
import os, sys, json, collections
sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

BASE = r"C:/Users/jngji/Desktop/실험실"
OV = f"{BASE}/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/ov28"
ov = open(f"{OV}/ov28.bin", "rb").read()
L = json.load(open(f"{OV}/opcode_lengths.json"))
BARE = {int(k): v for k, v in L["bare"].items()}
F8LEN = {int(k): v for k, v in L["f8"].items()}

# Corpus addresses run 0x2317..0x92dba, so the script starts well before the
# 0x8000 quoted in session 7b.
SCRIPT = (0x2000, 0x93000)


def oplen(i):
    """Length of the opcode at i, or None if unknown."""
    b = ov[i]
    if b in BARE:
        return BARE[b]
    if b in (0xF8, 0xF9):
        return F8LEN.get(ov[i + 1])
    return None


# ---- 1. sync walk -------------------------------------------------------
start = ov.find(b"\xf8\x6b", *SCRIPT)
i = start
steps = unknown = 0
bad = []
text_starts = {}
while i < SCRIPT[1]:
    b = ov[i]
    if b >= 0xF8:
        n = oplen(i)
        if n is None:
            unknown += 1
            bad.append((i, ov[i], ov[i + 1]))
            if len(bad) > 40:
                break
            n = 2
        i += n
    elif b == 0:
        # Not a terminator: the engine (0x020BFA20 cmp r4,#0 / beq) still advances
        # the cursor and carries 0 through as a blank glyph code.
        i += 1
    else:
        cc, nxt = P.bytes_to_cc(ov, i)
        if P.CC2CH.get(cc) is None:
            bad.append((i, b, None))
            if len(bad) > 40:
                break
            i = nxt
        else:
            st = i
            run = []
            while i < SCRIPT[1] and ov[i] < 0xF8:
                cc, nxt = P.bytes_to_cc(ov, i)
                ch = P.CC2CH.get(cc)
                if ch is None:
                    break
                run.append(ch)
                i = nxt
            text_starts[st] = "".join(run)
    steps += 1

print(f"walk from {start:#x} to {i:#x}  ({i - start} bytes, {steps} steps)")
print(f"  unknown opcodes : {unknown}")
print(f"  desync points   : {len(bad)}")
for a, b1, b2 in bad[:10]:
    print(f"    {a:#08x}  {b1:02X} {b2 if b2 is None else format(b2, '02X')}")

# ---- 2. compare with the old corpus ------------------------------------
old = {}
for ln in open(f"{OV}/dialogue_lines.tsv", encoding="utf-8").read().splitlines():
    p = ln.split("\t")
    if len(p) >= 4:
        old[int(p[0], 16)] = p[3]

hit = sum(1 for a in old if a in text_starts)
exact = sum(1 for a, t in old.items() if text_starts.get(a) == t)
print(f"\nold corpus lines           : {len(old)}")
print(f"  found at same address    : {hit}")
print(f"  byte-identical text      : {exact}")
print(f"  found but LONGER now     : {sum(1 for a, t in old.items() if a in text_starts and text_starts[a] != t and text_starts[a].startswith(t))}")

jp_chars = sum(len(t) for t in text_starts.values())
old_chars = sum(len(t) for t in old.values())
print(f"\ntext runs found by the walk : {len(text_starts)}  ({jp_chars} chars)")
print(f"old corpus                  : {len(old)}  ({old_chars} chars)")
