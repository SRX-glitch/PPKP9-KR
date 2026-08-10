#!/usr/bin/env python3
"""Can dictionary compression (MTE) fit Korean into the original byte budget?

Levers available under the "no repack, no ROM growth" policy:
  A. 1-byte charcodes  -> assign to the most frequent single syllables
  B. 2-byte charcodes  -> assign whole frequent SUBSTRINGS ("습니다", "그래서")
     We have 2058 free 2-byte slots; each costs 2 bytes regardless of length,
     so a 3-syllable ending drops from 6 bytes to 2.

Simulated on the existing 60-line translation against each line's real JP budget.
"""
import os, sys, csv, collections
sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

TRANS = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/translation/dialogue_ko.tsv"
rows = [r for r in csv.reader(open(TRANS, encoding="utf-8"), delimiter="\t")[1:]
        if len(r) >= 3] if False else None
rows = [r for r in list(csv.reader(open(TRANS, encoding="utf-8"), delimiter="\t"))[1:]
        if len(r) >= 3]

pairs = []
for r in rows:
    jp, kr = r[1], r[2]
    try:
        jb = sum(len(P.cc_to_bytes(P.CH2CC[ch])) for ch in jp)
    except KeyError:
        continue
    pairs.append((jp, kr, jb))
print(f"lines: {len(pairs)}   avg JP budget {sum(p[2] for p in pairs)/len(pairs):.1f} bytes")

corpus = [kr for _, kr, _ in pairs]
allko = "".join(corpus)


def build_dict(n_one, n_two):
    freq = collections.Counter(c for c in allko if 0xAC00 <= ord(c) <= 0xD7A3)
    one = {s for s, _ in freq.most_common(n_one)}
    # candidate substrings, scored by bytes saved
    cand = collections.Counter()
    for line in corpus:
        for L in range(2, 6):
            for i in range(len(line) - L + 1):
                sub = line[i:i + L]
                if all(0xAC00 <= ord(c) <= 0xD7A3 or c == " " for c in sub):
                    cand[sub] += 1
    def saving(sub, cnt):
        cost = sum(1 if c in one else 2 for c in sub)
        return (cost - 2) * cnt
    ranked = sorted(cand.items(), key=lambda kv: -saving(kv[0], kv[1]))
    two = [s for s, c in ranked if saving(s, c) > 0][:n_two]
    return one, two


def encode_len(text, one, two):
    """greedy longest-match dictionary encoding -> byte length"""
    i = 0
    n = 0
    tw = sorted(two, key=len, reverse=True)
    while i < len(text):
        for sub in tw:
            if text.startswith(sub, i):
                n += 2
                i += len(sub)
                break
        else:
            c = text[i]
            if 0xAC00 <= ord(c) <= 0xD7A3:
                n += 1 if c in one else 2
            else:
                n += 1 if (c in P.CH2CC and P.CH2CC[c] < 231) else 2
            i += 1
    return n


print("\nfit rate against each line's original JP byte budget:")
print(f"{'1-byte':>7} {'2-byte dict':>12} {'lines fit':>12} {'avg overflow':>14}")
for n_one, n_two in [(0, 0), (100, 0), (150, 0), (0, 500), (100, 500),
                     (150, 800), (150, 1500), (150, 2000)]:
    one, two = build_dict(n_one, n_two)
    fit = 0
    over = []
    for jp, kr, jb in pairs:
        kb = encode_len(kr, one, two)
        if kb <= jb:
            fit += 1
        else:
            over.append(kb - jb)
    avg = sum(over) / len(over) if over else 0
    print(f"{n_one:>7} {len(two):>12} {fit:>6}/{len(pairs):<5} "
          f"({fit*100//len(pairs):>3}%) {avg:>10.1f} B")

print("\nNOTE: the dictionary is built from this same 60-line sample, so these "
      "numbers are optimistic; a real dictionary trained on the full 9,957-line "
      "corpus generalises worse per line but covers far more text.")
