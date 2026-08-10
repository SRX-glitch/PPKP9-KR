#!/usr/bin/env python3
"""Go/no-go numbers for the two ways out of the byte-budget problem.

PLAN A - repack the script and fix up pointers.
  Needs: every reference into the script is findable. Count candidate pointers
  at ALL byte alignments; if unaligned candidates swamp aligned ones, fixup is
  unsafe (false positives corrupt data).

PLAN B - give the most frequent Korean syllables 1-BYTE charcodes by taking over
  rarely-used kana/symbol slots. Korean syllable frequency is very skewed, so a
  small number of 1-byte codes cuts the average cost a lot.
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

OUT = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/ov28"
TRANS = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/translation/dialogue_ko.tsv"
ov = open(os.path.join(OUT, "ov28.bin"), "rb").read()
RAM = 0x021C0DC0
N = len(ov)

print("=" * 70)
print("PLAN A — repack + pointer fixup")
print("=" * 70)
cand = collections.Counter()
for a in range(4):
    c = 0
    for o in range(a, N - 3, 4):
        v = int.from_bytes(ov[o:o + 4], "little")
        if RAM <= v < RAM + N:
            c += 1
    cand[a] = c
print(f"u32 values inside the overlay's own RAM range, by byte alignment:")
for a in range(4):
    print(f"  align {a}: {cand[a]}")
tot = sum(cand.values())
print(f"  total candidates at any alignment: {tot}")
print(f"  aligned(0) share: {cand[0]*100/tot:.1f}%")
print(f"  -> {'aligned pointers dominate: fixup is tractable' if cand[0] > 2*max(cand[1],cand[2],cand[3]) else 'unaligned noise is comparable: fixup is RISKY'}")

# how much do we even need to move? total text bytes in the script
tx = [i for i in range(N - 2) if ov[i] == 0xF8 and ov[i + 1] == 0x6B]
tot_text = 0
for i in tx:
    j = i + 3
    while j < N and ov[j] != 0 and ov[j] < 0xF8:
        j += 1
    tot_text += j - (i + 3)
print(f"\ntext commands: {len(tx)}, total inline text bytes: {tot_text} "
      f"({tot_text/1024:.0f} KB of the 560 KB script)")

print()
print("=" * 70)
print("PLAN B — 1-byte charcodes for frequent Korean syllables")
print("=" * 70)
ko = []
for ln in open(TRANS, encoding="utf-8").read().splitlines()[1:]:
    p = ln.split("\t")
    if len(p) >= 3:
        ko.append(p[2])
text = "".join(ko)
syl = [c for c in text if 0xAC00 <= ord(c) <= 0xD7A3]
freq = collections.Counter(syl)
print(f"corpus: {len(ko)} lines, {len(syl)} syllables, {len(freq)} distinct")
cum = 0
tots = len(syl)
print("\ncoverage by the top-N most frequent syllables:")
for topn in (32, 64, 100, 128, 192, 231):
    cov = sum(c for _, c in freq.most_common(topn))
    print(f"  top {topn:3d}: {cov*100/tots:5.1f}% of all syllable occurrences")

# average bytes per syllable if top-N get 1-byte codes
print("\naverage bytes per Hangul syllable:")
for topn in (0, 64, 100, 128, 192, 231):
    one = sum(c for _, c in freq.most_common(topn))
    avg = (one * 1 + (tots - one) * 2) / tots
    print(f"  {topn:3d} one-byte codes -> {avg:.2f} bytes/syllable")

# per-line budget check against the ORIGINAL japanese byte length
print("\nper-line fit against the original JP byte budget:")
import csv
rows = list(csv.reader(open(TRANS, encoding="utf-8"), delimiter="\t"))[1:]
for topn in (0, 100, 192, 231):
    onebyte = {s for s, _ in freq.most_common(topn)}
    fit = 0
    tested = 0
    over = []
    for r in rows:
        if len(r) < 3:
            continue
        jp, kr = r[1], r[2]
        try:
            jb = sum(len(P.cc_to_bytes(P.CH2CC[ch])) for ch in jp)
        except KeyError:
            continue
        kb = 0
        for ch in kr:
            if 0xAC00 <= ord(ch) <= 0xD7A3:
                kb += 1 if ch in onebyte else 2
            else:
                kb += 1 if ch in P.CH2CC and P.CH2CC[ch] < 231 else 2
        tested += 1
        if kb <= jb:
            fit += 1
        else:
            over.append(kb - jb)
    avg_over = sum(over) / len(over) if over else 0
    print(f"  {topn:3d} one-byte codes -> {fit}/{tested} lines fit "
          f"({fit*100//max(tested,1)}%), avg overflow {avg_over:.1f} bytes")
