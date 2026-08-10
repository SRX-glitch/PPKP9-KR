#!/usr/bin/env python3
"""Trustworthy charcode frequency census.

Noise decodes to ~uniform kanji soup; real text is heavily skewed. Filter hard:
  - run must be >= MINLEN chars and terminated by 0x00
  - kana fraction in a sane band for real JP prose
  - reject runs whose kanji are mostly JIS level-2 (noise signature)
Then report the frequency distribution so we can see the noise floor.
"""
import os, sys, re, collections, json
sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

ROM = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
OUTDIR = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font"
rom = open(ROM, "rb").read()
n = len(rom)

KANA = re.compile(r'[぀-ヿ]')
MINLEN = int(sys.argv[1]) if len(sys.argv) > 1 else 12

used = collections.Counter()
samples = []
kept = 0
i = 0
while i < n - 1:
    if not (1 <= rom[i] <= 247):
        i += 1
        continue
    seq = []
    j = i
    ok = False
    while j < n - 1:
        if rom[j] == 0:
            ok = True
            break
        cc, j2 = P.bytes_to_cc(rom, j)
        if cc is None or cc not in P.CC2CH:
            break
        seq.append(cc)
        j = j2
        if len(seq) > 300:
            break
    if ok and len(seq) >= MINLEN:
        s = "".join(P.CC2CH[c] for c in seq)
        kana = len(KANA.findall(s)) / len(s)
        # real JP prose: 40%+ kana. Noise is kanji-soup (low kana) or pure-kana runs.
        if 0.40 <= kana <= 0.98:
            used.update(seq)
            kept += 1
            if len(samples) < 12 and len(s) > 14:
                samples.append((i, s))
            i = j + 1
            continue
    i += 1

print(f"MINLEN={MINLEN}  kept runs: {kept}   distinct charcodes: {len(used)}")
print("\nsamples:")
for off, s in samples:
    print(f"  0x{off:06X}  {s[:60]}")

freq = collections.Counter(used)
print(f"\ntop 20: {[(P.CC2CH[c], k) for c, k in freq.most_common(20)]}")
hist = collections.Counter()
for c, k in freq.items():
    hist[min(k, 50)] += 1
print("\ncount histogram (count -> #charcodes):")
for k in sorted(hist)[:20]:
    print(f"  {k:3d} -> {hist[k]}")

unused = [c for c in range(4352) if c not in used]
print(f"\ncharcodes with ZERO hits: {len(unused)}")
for thr in (1, 2, 3, 5, 10):
    print(f"  <= {thr:2d} hits: {len([c for c in range(4352) if used.get(c,0) <= thr])}")

json.dump({"minlen": MINLEN, "counts": {str(k): v for k, v in used.items()}},
          open(os.path.join(OUTDIR, f"census_min{MINLEN}.json"), "w"))
print("wrote census json")
