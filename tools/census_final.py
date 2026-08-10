#!/usr/bin/env python3
"""Final charcode census — restricted to the real text regions."""
import os, sys, re, json, collections
sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

ROM = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
OUTDIR = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font"
rom = open(ROM, "rb").read()
regions = json.load(open(os.path.join(OUTDIR, "text_regions.json")))

KANA = re.compile(r'[぀-ヿ]')
used = collections.Counter()
strings = []

for rs, re_ in regions:
    i = rs
    while i < re_ - 1:
        if not (1 <= rom[i] <= 247):
            i += 1
            continue
        seq = []
        j = i
        term = False
        while j < re_ - 1:
            if rom[j] == 0:
                term = True
                break
            cc, j2 = P.bytes_to_cc(rom, j)
            if cc is None or cc not in P.CC2CH:
                break
            seq.append(cc)
            j = j2
            if len(seq) > 300:
                break
        if term and len(seq) >= 4:
            s = "".join(P.CC2CH[c] for c in seq)
            if len(KANA.findall(s)) >= max(2, len(s) * 0.3):
                used.update(seq)
                strings.append((i, s))
                i = j + 1
                continue
        i += 1

print(f"strings: {len(strings)}   distinct charcodes: {len(used)}")
print("samples:")
for off, s in strings[len(strings)//2: len(strings)//2 + 8]:
    print(f"  0x{off:06X}  {s[:70]}")

print(f"\ntop 15: {[(P.CC2CH[c], k) for c, k in used.most_common(15)]}")
for thr in (0, 1, 2, 3, 5, 10, 20):
    n = len([c for c in range(4352) if used.get(c, 0) <= thr])
    print(f"  charcodes with <= {thr:2d} hits: {n}")

# Slots we can safely repurpose, best-first (never used, then rarest).
order = sorted(range(4352), key=lambda c: (used.get(c, 0), -c))
free = [c for c in order if used.get(c, 0) == 0]
print(f"\nZERO-hit charcodes: {len(free)}")
json.dump({"counts": {str(k): v for k, v in used.items()},
           "free": free, "order": order},
          open(os.path.join(OUTDIR, "census_final.json"), "w"))
with open(os.path.join(OUTDIR, "game_strings.tsv"), "w", encoding="utf-8") as f:
    for off, s in strings:
        f.write(f"0x{off:06X}\t{len(s)}\t{s}\n")
print("wrote census_final.json + game_strings.tsv")
