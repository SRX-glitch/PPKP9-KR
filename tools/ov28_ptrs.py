#!/usr/bin/env python3
"""Overlay 28: how position-dependent is it?

Repacking strings is only safe if we can account for every reference into the
text area. Measure:
  1. density of u32 values that land inside the overlay's own RAM range
  2. where those pointers point (code area vs text area)
  3. whether text-area pointers cluster into a table
"""
import os, sys, collections, json
sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

ROM = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
OUT = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/ov28"
rom = open(ROM, "rb").read()
u32 = lambda o: int.from_bytes(rom[o:o + 4], "little")

FS, FE = 0x04CC000, 0x055EE40
RAM = 0x021C0DC0
SIZE = FE - FS
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, "ov28.bin"), "wb").write(rom[FS:FE])
print(f"overlay 28: file 0x{FS:07X}-0x{FE:07X}  size 0x{SIZE:X} ({SIZE/1024:.0f} KB)  RAM 0x{RAM:08X}-0x{RAM+SIZE:08X}")

# --- 1. self-pointer census (4-byte aligned) ---
selfptr = []
for o in range(FS, FE - 3, 4):
    v = u32(o)
    if RAM <= v < RAM + SIZE:
        selfptr.append((o - FS, v - RAM))
print(f"\naligned u32 landing inside the overlay: {len(selfptr)}")

# --- 2. find the text area: first & last confident string ---
def is_text_at(off, minlen=6):
    seq = []
    i = off
    while i < FE - 1:
        if rom[i] == 0:
            return len(seq) >= minlen, i
        cc, j = P.bytes_to_cc(rom, i)
        if cc is None or cc not in P.CC2CH or j > FE - 1:
            return False, i
        seq.append(cc)
        i = j
        if len(seq) > 200:
            return False, i
    return False, i

# map which bytes belong to confident strings
import re
KANA = re.compile(r'[぀-ヿ]')
covered = bytearray(SIZE)
strings = []
i = FS
while i < FE - 1:
    if not (1 <= rom[i] <= 247):
        i += 1
        continue
    seq = []
    j = i
    term = False
    while j < FE - 1:
        if rom[j] == 0:
            term = True
            break
        cc, j2 = P.bytes_to_cc(rom, j)
        if cc is None or cc not in P.CC2CH:
            break
        seq.append(cc)
        j = j2
        if len(seq) > 250:
            break
    if term and len(seq) >= 6:
        s = "".join(P.CC2CH[c] for c in seq)
        if len(KANA.findall(s)) >= max(2, len(s) * 0.3):
            strings.append((i - FS, j - FS, s))
            for k in range(i - FS, j - FS + 1):
                covered[k] = 1
            i = j + 1
            continue
    i += 1

tstart = min(s for s, _, _ in strings)
tend = max(e for _, e, _ in strings)
print(f"confident strings: {len(strings)}")
print(f"text span: 0x{tstart:X}-0x{tend:X}  ({(tend-tstart)/1024:.0f} KB, "
      f"{sum(covered)*100/(tend-tstart):.1f}% of that span is string bytes)")

# --- 3. where do self-pointers point? ---
into_text = [(src, dst) for src, dst in selfptr if tstart <= dst <= tend]
print(f"\nself-pointers targeting the text span: {len(into_text)} / {len(selfptr)}")
onstr = sum(1 for _, dst in into_text if covered[dst])
print(f"  ...of which land ON a string byte: {onstr}")

# where do the *sources* live?
if into_text:
    srcs = sorted(src for src, _ in into_text)
    buckets = collections.Counter(s // 0x1000 for s in srcs)
    print(f"  source locations span 0x{srcs[0]:X}-0x{srcs[-1]:X} in "
          f"{len(buckets)} 4KB buckets; densest: {buckets.most_common(5)}")

# --- 4. code vs data: where does the ARM code end? ---
code_end = max((src for src, _ in selfptr if src < tstart), default=0)
print(f"\nhighest self-pointer before the text span: 0x{code_end:X}")
json.dump({"file": [FS, FE], "ram": RAM, "text_span": [tstart, tend],
           "n_strings": len(strings), "selfptr": len(selfptr),
           "into_text": len(into_text)},
          open(os.path.join(OUT, "ov28_info.json"), "w"))
with open(os.path.join(OUT, "ov28_strings.tsv"), "w", encoding="utf-8") as f:
    for s, e, t in strings:
        f.write(f"0x{s:06X}\t0x{RAM+s:08X}\t{e-s}\t{t}\n")
print("wrote ov28.bin, ov28_strings.tsv, ov28_info.json")
