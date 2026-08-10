#!/usr/bin/env python3
"""Extract the game's character-code table(s) embedded in PokeTEXT.exe (.NET),
stored as UTF-16LE string literals. These map the game's byte encoding -> JP text."""
import sys, re
data=open(sys.argv[1],"rb").read()
print("size:",len(data))
text=data.decode("utf-16-le","ignore")
JP=re.compile(r'[぀-ヿ㐀-鿿＀-￯　-〄ｦ-ﾟ]')
runs=[]; cur=[]; start=0
for i,ch in enumerate(text):
    if JP.match(ch) or ch in "　・ー―":
        if not cur: start=i
        cur.append(ch)
    else:
        if len(cur)>=16: runs.append((start*2, "".join(cur)))
        cur=[]
if len(cur)>=16: runs.append((start*2,"".join(cur)))
runs.sort(key=lambda x:-len(x[1]))
print(f"=== {len(runs)} Japanese runs; lengths of top 12: {[len(r) for _,r in runs[:12]]}")
with open(sys.argv[2],"w",encoding="utf-8") as f:
    for off,r in runs:
        f.write(f"[0x{off:X}] ({len(r)}) {r}\n")
print(f"wrote all runs to {sys.argv[2]}")
