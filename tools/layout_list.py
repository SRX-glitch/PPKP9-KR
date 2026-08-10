#!/usr/bin/env python3
"""List every translated line that costs an extra display line, with the batch
file it lives in, so it can be tightened. Writes UTF-8 (the console here is
cp949 and chokes on the Japanese source)."""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from layout_audit import rows, BASE, BATCHES

trans, origin = {}, {}
for name in BATCHES:
    p = f"{BASE}/translation/{name}.tsv"
    if not os.path.exists(p):
        continue
    for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
        if "\t" in ln:
            jp, ko = ln.split("\t")[:2]
            if jp.strip() and ko.strip():
                trans[jp.strip()] = ko.strip()
                origin[jp.strip()] = name

occ = collections.Counter()
for ln in open(f"{BASE}/survey/ov28/dialogue_runs.tsv", encoding="utf-8").read().splitlines():
    p = ln.split("\t")
    if len(p) >= 4:
        occ[p[3]] += 1

out = ["batch\tocc\tjp_rows\tkr_rows\tkr_len\tbudget\tjp\tko"]
n = 0
for jp, ko in trans.items():
    if jp not in occ:
        continue
    rj, rk = rows(jp), rows(ko, korean=True)
    if rk > rj:
        n += 1
        out.append(f"{origin[jp]}\t{occ[jp]}\t{rj}\t{rk}\t{len(ko)}\t{rj*19}\t{jp}\t{ko}")

dst = f"{BASE}/survey/layout_overflow.tsv"
open(dst, "w", encoding="utf-8").write("\n".join(out) + "\n")
print(f"{n} overflowing lines -> {dst}")
