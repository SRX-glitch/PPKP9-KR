#!/usr/bin/env python3
"""Which table/variant holds a given kanji, and does it match the ROM font order?"""
import re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

lines = open(P.CS, encoding="utf-8").read().splitlines()
in3 = False
tables = {}
pat = re.compile(r'array4\[(\d+)\]\s*=\s*"(.*)";\s*$')
for ln in lines:
    if "ポケ3以降の文字コード変換処理" in ln:
        in3 = True
    m = pat.search(ln)
    if m and in3:
        s = re.sub(r'\\u([0-9a-fA-F]{4})', lambda x: chr(int(x.group(1), 16)), m.group(2))
        tables.setdefault(int(m.group(1)), []).append(s)

print("variants per table:", {k: len(v) for k, v in sorted(tables.items())})
for k in sorted(tables):
    for i, s in enumerate(tables[k]):
        print(f"  t{k:2d} v{i}  len={len(s):4d}  head={s[:24]!r}")

print()
for ch in "何練習気起良待事上手":
    loc = [(k, i, s.index(ch)) for k in tables for i, s in enumerate(tables[k]) if ch in s]
    print(f"  {ch}: {loc}")
