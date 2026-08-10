#!/usr/bin/env python3
"""Exact text inventory from the script stream, plus the two levers we have
left now that repacking is off the table:

  L1. per-string trailing slack (padding bytes after the terminator we may absorb)
  L2. which 1-byte charcodes (0..230) are rare enough to reassign to Hangul

Parses the real command stream, so this census is trustworthy -- unlike scanning
raw ROM bytes, which decodes compressed graphics into kana soup.
"""
import os, sys, collections, json
sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

OUT = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/ov28"
ov = open(os.path.join(OUT, "ov28.bin"), "rb").read()
N = len(ov)
RAM = 0x021C0DC0

lines = []          # (text_start, text_len, slack, decoded)
i = 0
while i < N - 3:
    if ov[i] == 0xF8 and ov[i + 1] == 0x6B:
        st = i + 3
        j = st
        while j < N and ov[j] != 0 and ov[j] < 0xF8:
            j += 1
        ln = j - st
        if ln > 0:
            k = j
            while k < N and ov[k] == 0:
                k += 1
            slack = k - j
            s = []
            p = st
            ok = True
            while p < j:
                cc, p2 = P.bytes_to_cc(ov, p)
                if cc is None or cc not in P.CC2CH:
                    ok = False
                    break
                s.append(P.CC2CH[cc])
                p = p2
            if ok:
                lines.append((st, ln, slack, "".join(s)))
        i = j
        continue
    i += 1

print(f"parsed text lines: {len(lines)}")
tot = sum(l for _, l, _, _ in lines)
print(f"total text bytes: {tot} ({tot/1024:.0f} KB)")
L = [l for _, l, _, _ in lines]
L.sort()
print(f"line length bytes: min {L[0]}, median {L[len(L)//2]}, "
      f"mean {tot/len(L):.1f}, max {L[-1]}")

print("\n--- L1: trailing slack after the terminator ---")
sl = collections.Counter(s for _, _, s, _ in lines)
print(f"slack distribution: {sorted(sl.items())[:12]}")
tots = sum(s for _, _, s, _ in lines)
print(f"total slack bytes: {tots} ({tots/len(lines):.2f} per line avg)")
print(f"lines with >=1 slack byte: {sum(1 for _,_,s,_ in lines if s>=1)}"
      f" ({sum(1 for _,_,s,_ in lines if s>=1)*100//len(lines)}%)")
print(f"lines with >=4 slack bytes: {sum(1 for _,_,s,_ in lines if s>=4)}")

print("\n--- L2: 1-byte charcode usage in real text ---")
one = collections.Counter()
two = collections.Counter()
for st, ln, _, _ in lines:
    p = st
    while p < st + ln:
        cc, p2 = P.bytes_to_cc(ov, p)
        if cc is None:
            break
        (one if cc < 231 else two)[cc] += 1
        p = p2
print(f"distinct 1-byte charcodes used: {len(one)} / 231")
print(f"distinct 2-byte charcodes used: {len(two)}")
unused1 = [c for c in range(231) if c not in one]
print(f"1-byte charcodes NEVER used in dialogue: {len(unused1)}")
for thr in (0, 5, 20, 50, 200, 1000):
    n = len([c for c in range(231) if one.get(c, 0) <= thr])
    print(f"  <= {thr:4d} uses: {n:3d} charcodes")
rare = sorted(range(231), key=lambda c: one.get(c, 0))
print("\nrarest 1-byte charcodes (char, uses):")
print("  " + ", ".join(f"{P.CC2CH.get(c,'?')}:{one.get(c,0)}" for c in rare[:40]))

json.dump({"unused1": unused1,
           "one_counts": {str(k): v for k, v in one.items()},
           "rare_order": rare},
          open(os.path.join(OUT, "byte1_census.json"), "w"))
with open(os.path.join(OUT, "dialogue_lines.tsv"), "w", encoding="utf-8") as f:
    for st, ln, sk, s in lines:
        f.write(f"0x{st:06X}\t{ln}\t{sk}\t{s}\n")
print(f"\nwrote dialogue_lines.tsv ({len(lines)} lines) + byte1_census.json")
