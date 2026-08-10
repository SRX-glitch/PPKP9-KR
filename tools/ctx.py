#!/usr/bin/env python3
"""Show a corpus run with its neighbours, so an ambiguous fragment can be read in place."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"
rows = []
for ln in open(f"{BASE}/survey/ov28/dialogue_runs.tsv", encoding="utf-8").read().splitlines():
    p = ln.split("\t")
    if len(p) >= 4:
        rows.append((int(p[0], 16), p[3]))
rows.sort()
n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
shown = 0
for i, (off, jp) in enumerate(rows):
    if jp == sys.argv[1]:
        print("=" * 50)
        for j in range(max(0, i - n), min(len(rows), i + n + 1)):
            print(("  >> " if j == i else "     ") + f"{rows[j][0]:06X} {rows[j][1]}")
        shown += 1
        if shown >= 3:
            break
