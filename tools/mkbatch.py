#!/usr/bin/env python3
"""Join `index<TAB>korean` lines onto the worksheet's jp column by row index.

Translating against a row number instead of retyping the Japanese removes the
one failure mode that has bitten this project before: an invented/mistyped jp
key silently matches nothing in the corpus (session 20, batch42).
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"

ws, ko_src, out = sys.argv[1], sys.argv[2], sys.argv[3]
rows = [l.split("\t") for l in
        open(f"{BASE}/translation/{ws}", encoding="utf-8").read().splitlines()[1:]]

pairs, bad = [], []
for ln in open(ko_src, encoding="utf-8").read().splitlines():
    if not ln.strip() or "\t" not in ln:
        continue
    i, ko = ln.split("\t", 1)
    i, ko = int(i), ko.strip()
    if not ko:
        continue
    jp, cap = rows[i][3], int(rows[i][2])
    if len(ko) > cap:
        bad.append((i, cap, len(ko), jp, ko))
    pairs.append((jp, ko))

with open(f"{BASE}/translation/{out}", "w", encoding="utf-8") as f:
    f.write("jp\tko\n")
    for jp, ko in pairs:
        f.write(f"{jp}\t{ko}\n")
print(f"{out}: {len(pairs)} lines")
for i, cap, n, jp, ko in bad:
    print(f"  OVER row {i}: cap {cap} got {n} | {jp} -> {ko}")
