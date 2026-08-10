#!/usr/bin/env python3
"""Re-extract overlay 28's dialogue with the validated opcode length table.

The old scanner (text_budget.py) stopped a line at the first byte >= 0xF8 or 0x00
and then skipped to the next `F8 6B`, so everything after an inline control code
was lost. Walking the stream properly recovers those remainders.

Emits every contiguous charcode run with its address and byte budget -- the same
unit the patcher already works in, so each run can be translated and reinserted
independently.
"""
import os, sys, json, collections
sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

BASE = r"C:/Users/jngji/Desktop/실험실"
OV = f"{BASE}/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/ov28"
ov = open(f"{OV}/ov28.bin", "rb").read()
L = json.load(open(f"{OV}/opcode_lengths.json"))
BARE = {int(k): v for k, v in L["bare"].items()}
F8 = {int(k): v for k, v in L["f8"].items()}

old = {}
for ln in open(f"{OV}/dialogue_lines.tsv", encoding="utf-8").read().splitlines():
    p = ln.split("\t")
    if len(p) >= 4:
        old[int(p[0], 16)] = p[3]
LO, HI = min(old) - 3, min(max(old) + 256, len(ov) - 2)

JP = lambda c: ("぀" <= c <= "ヿ" or "一" <= c <= "鿿" or c in "。、！？・～「」（）ー")

runs = []
i, box, desync = LO, None, 0
# in_dialogue gate: a text run counts as dialogue only if an `F8 6B` (message
# start) has been seen since the last data gap. This keeps the recovered
# post-control-code tails (誰かとケンカ...) while dropping the binary data tables
# between messages, whose byte runs decode to kana-ish noise (「さいＵあ」 etc.).
in_dialogue = False
zeros = 0
while i < HI and i < len(ov) - 2:
    b = ov[i]
    if b == 0:
        # A valid blank glyph mid-message, but also the padding that separates
        # script from data. Three-plus zeros in a row = a gap: leave dialogue.
        zeros += 1
        if zeros >= 3:
            in_dialogue = False
        i += 1
        continue
    zeros = 0
    if b < 0xF8:
        st, chars = i, []
        while i < HI and 0 < ov[i] < 0xF8:
            cc, nxt = P.bytes_to_cc(ov, i)
            ch = P.CC2CH.get(cc)
            if ch is None:
                break
            chars.append(ch)
            i = nxt
        if chars and in_dialogue:
            runs.append((st, i - st, box, "".join(chars)))
        if i == st:
            i += 1
    elif b in BARE:
        if b == 0xFF:              # clear box -> message ended
            in_dialogue = False
        i += BARE[b]
    elif b in (0xF8, 0xF9):
        s = ov[i + 1]
        if s == 0x6B:
            box = ov[i + 2] if i + 2 < len(ov) else None
            in_dialogue = True     # message start
        # A choice list is player-facing text too, but it never follows an
        # `F8 6B`, so the in_dialogue gate dropped it: 386 of the 512 distinct
        # options never reached the worklist and shipped in Japanese. `F8 15`
        # opens the list (its operand is the option count) and `F8 F8` separates
        # the options, so both have to keep the gate open.
        elif s == 0x15:
            in_dialogue = True     # choice list start
        elif s == 0xF8:
            i += 2                 # option separator
            continue
        n = F8.get(s)
        if n is None:              # unknown subcode = desync into data
            desync += 1
            in_dialogue = False
            n = 2
        i += n
    else:
        desync += 1
        i += 1

jp_runs = [r for r in runs if sum(1 for c in r[3] if JP(c)) / len(r[3]) >= 0.5]

print(f"text runs walked        : {len(runs)}   ({sum(len(r[3]) for r in runs)} chars)")
print(f"  Japanese-looking      : {len(jp_runs)} ({sum(len(r[3]) for r in jp_runs)} chars)")
print(f"old corpus              : {len(old)} ({sum(len(t) for t in old.values())} chars)")
print(f"unknown opcodes on walk : {desync}")

at_old = {a for a, _, _, _ in runs} & set(old)
print(f"\nold addresses reproduced: {len(at_old)}/{len(old)}")
same = sum(1 for a, _, _, t in runs if a in old and old[a] == t)
longer = sum(1 for a, _, _, t in runs if a in old and t != old[a] and t.startswith(old[a]))
print(f"  identical text        : {same}")
print(f"  same start, now longer: {longer}")

new_only = [r for r in jp_runs if r[0] not in old]
print(f"\nruns the old corpus never had: {len(new_only)}"
      f"  ({sum(len(r[3]) for r in new_only)} chars)")
print("\nsamples of newly recovered text:")
for a, n, bx, t in new_only[:15]:
    if len(t) >= 6:
        print(f"  {a:#08x} ({n:2d}B)  {t}")

with open(f"{OV}/dialogue_runs.tsv", "w", encoding="utf-8", newline="\n") as f:
    for a, n, bx, t in jp_runs:
        f.write(f"{a:#08x}\t{n}\t{bx if bx is not None else ''}\t{t}\n")
print(f"\nwrote {OV}/dialogue_runs.tsv")
