#!/usr/bin/env python3
"""Pin down the F8 subcode lengths using the corpus as an oracle.

Every corpus line is preceded by `F8 6B <box>`, so a correct length table makes a
straight walk of the stream land exactly on all 9,957 recorded text addresses.
That turns "is this length right?" into a number we can maximise.

Start from the disassembly-derived table (tools/opcode_table.py) and do
coordinate ascent: for each subcode that the walk actually meets, try lengths
2..8, keep whichever lands on the most corpus addresses. Where the result agrees
with the disassembly, two independent methods confirm each other; where it does
not, the handler is worth reading by hand.
"""
import os, sys, json, collections
sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

BASE = r"C:/Users/jngji/Desktop/실험실"
OV = f"{BASE}/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/ov28"
ov = open(f"{OV}/ov28.bin", "rb").read()
L = json.load(open(f"{OV}/opcode_lengths.json"))
BARE = {int(k): v for k, v in L["bare"].items()}
DISASM = {int(k): v for k, v in L["f8"].items()}

anchors = set()
for ln in open(f"{OV}/dialogue_lines.tsv", encoding="utf-8").read().splitlines():
    p = ln.split("\t")
    if len(p) >= 4:
        anchors.add(int(p[0], 16))
LO, HI = min(anchors) - 3, max(anchors) + 64

# charcode step: 1 byte, or 2 for the 0xE8-0xF7 lead bytes; 0x00 is a valid blank
STEP = bytearray(248)
for b in range(248):
    STEP[b] = 2 if 232 <= b <= 247 else 1


def walk(lens, start):
    """Walk from start; return (corpus addresses hit, steps, desyncs)."""
    i, hit, steps, bad = start, 0, 0, 0
    n = len(ov)
    while i < HI and i < n - 2:
        b = ov[i]
        if b < 0xF8:
            if i in anchors:
                hit += 1
            i += STEP[b]
        elif b in BARE:
            i += BARE[b]
        elif b in (0xF8, 0xF9):
            s = ov[i + 1]
            m = lens.get(s)
            if m is None:
                bad += 1
                m = 2
            i += m
        else:
            bad += 1
            i += 1
        steps += 1
    return hit, steps, bad


start = min(anchors) - 3
lens = dict(DISASM)
base_hit, _, base_bad = walk(lens, start)
print(f"disassembly table  : {base_hit}/{len(anchors)} anchors hit, {base_bad} desyncs")

# which subcodes does the walk actually meet? (collect with the current table)
def met(lens):
    i, seen = start, collections.Counter()
    n = len(ov)
    while i < HI and i < n - 2:
        b = ov[i]
        if b < 0xF8:
            i += STEP[b]
        elif b in BARE:
            i += BARE[b]
        elif b in (0xF8, 0xF9):
            s = ov[i + 1]
            seen[s] += 1
            i += lens.get(s, 2)
        else:
            i += 1
    return seen

best = base_hit
for rnd in range(6):
    order = [s for s, _ in met(lens).most_common() if s <= 0x6F]
    improved = False
    for s in order:
        cur = lens.get(s, 2)
        cand = cur
        for m in range(2, 9):
            if m == cur:
                continue
            trial = dict(lens)
            trial[s] = m
            h, _, _ = walk(trial, start)
            if h > best:
                best, cand = h, m
        if cand != cur:
            lens[s] = cand
            improved = True
            print(f"  round {rnd}: subcode {s:02X}  {cur} -> {cand}  ({best}/{len(anchors)})")
    if not improved:
        break

hit, steps, bad = walk(lens, start)
print(f"\nsolved table       : {hit}/{len(anchors)} anchors hit "
      f"({hit/len(anchors):.1%}), {bad} desyncs, {steps} steps")

diff = {s: (DISASM.get(s), lens[s]) for s in lens if DISASM.get(s) != lens[s]}
print(f"\nsubcodes where the solver disagrees with the disassembly: {len(diff)}")
for s, (d, v) in sorted(diff.items()):
    print(f"  {s:02X}: disasm={d}  solved={v}")

json.dump({"bare": BARE, "f8": lens}, open(f"{OV}/opcode_lengths_solved.json", "w"), indent=1)
print(f"\nwrote {OV}/opcode_lengths_solved.json")
