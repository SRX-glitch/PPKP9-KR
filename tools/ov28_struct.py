#!/usr/bin/env python3
"""Overlay 28 structure: where is the text block, and what frames each string?"""
import os, sys, re, collections
sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

OUT = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/ov28"
ov = open(os.path.join(OUT, "ov28.bin"), "rb").read()
RAM = 0x021C0DC0
N = len(ov)
u32 = lambda o: int.from_bytes(ov[o:o + 4], "little")

KANA = re.compile(r'[぀-ヿ]')
JPOK = re.compile(r'[぀-ヿ一-鿿０-９Ａ-Ｚａ-ｚ、。！？「」（）・…ー～]')


def scan(minlen, kana_ratio):
    out = []
    i = 0
    while i < N - 1:
        if not (1 <= ov[i] <= 247):
            i += 1
            continue
        seq = []
        j = i
        term = False
        while j < N - 1:
            if ov[j] == 0:
                term = True
                break
            cc, j2 = P.bytes_to_cc(ov, j)
            if cc is None or cc not in P.CC2CH:
                break
            seq.append(cc)
            j = j2
            if len(seq) > 250:
                break
        if term and len(seq) >= minlen:
            s = "".join(P.CC2CH[c] for c in seq)
            if (len(KANA.findall(s)) >= len(s) * kana_ratio
                    and len(JPOK.findall(s)) >= len(s) * 0.95):
                out.append((i, j, s))
                i = j + 1
                continue
        i += 1
    return out


strings = scan(8, 0.35)
print(f"strict strings: {len(strings)}")
starts = {s for s, _, _ in strings}
lo, hi = min(starts), max(e for _, e, _ in strings)
print(f"span 0x{lo:X}-0x{hi:X}  ({(hi-lo)/1024:.0f} KB)")

# density profile in 16KB chunks -> find the real text block
prof = collections.Counter(s // 0x4000 for s, _, _ in strings)
print("\nstrings per 16KB chunk (chunk: count), only chunks with >=5:")
rows = [(c, n) for c, n in sorted(prof.items()) if n >= 5]
print("  " + ", ".join(f"{c*0x4000:#x}:{n}" for c, n in rows))

# --- pointers that hit an exact string start ---
ptrs = collections.Counter()
exact = []
for o in range(0, N - 3, 4):
    v = u32(o)
    if RAM <= v < RAM + N:
        d = v - RAM
        ptrs[d] += 1
        if d in starts:
            exact.append((o, d))
print(f"\naligned self-pointers: {sum(ptrs.values())}, distinct targets {len(ptrs)}")
print(f"pointers hitting an EXACT strict-string start: {len(exact)}"
      f"  ({len(exact)*100//max(len(strings),1)}% of strings covered)")
covered = {d for _, d in exact}
print(f"distinct strings referenced by a pointer: {len(covered)} / {len(strings)}")

# --- what frames a string? bytes immediately before each start ---
pre = collections.Counter(ov[s - 1] for s, _, _ in strings if s > 0)
pre2 = collections.Counter(ov[s - 2:s].hex() for s, _, _ in strings if s > 1)
print(f"\nbyte immediately BEFORE a string: {pre.most_common(8)}")
print(f"two bytes before: {pre2.most_common(8)}")
post = collections.Counter(ov[e + 1] for _, e, _ in strings if e + 1 < N)
print(f"byte AFTER the 0x00 terminator: {post.most_common(8)}")

# --- gaps between consecutive strings ---
ss = sorted(strings)
gaps = collections.Counter()
for (s1, e1, _), (s2, _, _) in zip(ss, ss[1:]):
    gaps[min(s2 - e1 - 1, 40)] += 1
print(f"\ngap (bytes) between end-of-string and next string: {gaps.most_common(12)}")
