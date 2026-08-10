#!/usr/bin/env python3
"""Strict census: which charcodes appear in REAL game text.

Two passes:
  A) permissive scan but keep only runs that look like genuine JP text
  B) report per-block usage so we can find blocks that are entirely dead
"""
import os, sys, re, collections, json
sys.path.insert(0, os.path.dirname(__file__))
import fontcodec as F
import poketbl as P

ROM = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
OUTDIR = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font"
rom = open(ROM, "rb").read()

KANA = re.compile(r'[぀-ヿ]')
JP = re.compile(r'[぀-ヿ一-鿿＀-￯0-9A-Za-z]')

n = len(rom)
used = collections.Counter()
kept = 0
i = 0
while i < n - 1:
    b = rom[i]
    if not (1 <= b <= 247):
        i += 1
        continue
    seq = []
    j = i
    while j < n - 1:
        cc, j2 = P.bytes_to_cc(rom, j)
        if cc is None or cc not in P.CC2CH:
            break
        seq.append(cc)
        j = j2
        if len(seq) > 400:
            break
    if len(seq) >= 5:
        s = "".join(P.CC2CH[c] for c in seq)
        if len(KANA.findall(s)) >= 2 and len(JP.findall(s)) >= len(s) * 0.85:
            used.update(seq)
            kept += 1
            i = j
            continue
    i += 1

print(f"kept text runs: {kept}")
print(f"distinct charcodes used: {len(used)} / 4327")

allcc = set(range(4352))
unused = sorted(allcc - set(used))
print(f"unused charcodes: {len(unused)}")

# rare = used but only once or twice (risky but nearly free)
rare = sorted(c for c, k in used.items() if k <= 2)
print(f"charcodes used <=2 times: {len(rare)}")

# per block
perblock = collections.Counter(cc // 64 for cc in used)
dead_blocks = [b for b in range(F.NBLOCK) if perblock.get(b, 0) == 0]
lite_blocks = [(b, perblock.get(b, 0)) for b in range(F.NBLOCK) if 0 < perblock.get(b, 0) <= 6]
print(f"\nfully dead blocks ({len(dead_blocks)}): {dead_blocks}")
print(f"  = {len(dead_blocks)*64} free charcodes")
print(f"near-dead blocks (<=6 used): {lite_blocks}")

def runs_of(lst):
    out = []
    s = p = lst[0]
    for x in lst[1:]:
        if x == p + 1:
            p = x; continue
        out.append((s, p)); s = p = x
    out.append((s, p))
    return out

r = sorted(runs_of(unused), key=lambda t: -(t[1] - t[0]))
print("\nlargest contiguous unused ranges:")
for s, e in r[:20]:
    print(f"  0x{s:04X}-0x{e:04X}  ({e-s+1})")

json.dump({"unused": unused, "dead_blocks": dead_blocks,
           "counts": {str(k): v for k, v in used.items()}},
          open(os.path.join(OUTDIR, "census.json"), "w"))
print("\nwrote census.json")
