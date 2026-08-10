#!/usr/bin/env python3
"""Look for offset/index tables addressing the overlay-28 strings.

Tries u32 and u16, absolute-RAM / file-relative / relative-to-an-arbitrary-base,
by requiring a run of consecutive entries that all land on real string starts.
"""
import os, sys, re, collections
sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

OUT = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/ov28"
ov = open(os.path.join(OUT, "ov28.bin"), "rb").read()
RAM = 0x021C0DC0
N = len(ov)
u32 = lambda o: int.from_bytes(ov[o:o + 4], "little")
u16 = lambda o: int.from_bytes(ov[o:o + 2], "little")

KANA = re.compile(r'[぀-ヿ]')


def all_string_starts():
    """Loose scan: anything null-terminated that decodes and has kana."""
    starts = set()
    i = 0
    while i < N - 1:
        if not (1 <= ov[i] <= 247) or (i > 0 and ov[i - 1] != 0):
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
        if term and len(seq) >= 3:
            s = "".join(P.CC2CH[c] for c in seq)
            if len(KANA.findall(s)) >= 1:
                starts.add(i)
        i += 1
    return starts


starts = all_string_starts()
print(f"loose string starts: {len(starts)}")

MINRUN = 6


def find_tables(width, base_desc, base_fn):
    """base_fn(value, table_offset) -> candidate string offset"""
    read = u32 if width == 4 else u16
    hits = []
    run = 0
    o = 0
    while o < N - width:
        v = read(o)
        tgt = base_fn(v, o)
        if tgt is not None and tgt in starts:
            run += 1
        else:
            if run >= MINRUN:
                hits.append((o - run * width, run))
            run = 0
        o += width
    if run >= MINRUN:
        hits.append((o - run * width, run))
    tot = sum(r for _, r in hits)
    print(f"  {base_desc:<28s} width {width}: {len(hits)} runs, {tot} entries"
          + (f"  biggest: {sorted(hits, key=lambda h: -h[1])[:4]}" if hits else ""))
    return hits


print("\nsearching for index tables (runs of >=6 consecutive valid entries):")
find_tables(4, "absolute RAM", lambda v, o: v - RAM if RAM <= v < RAM + N else None)
find_tables(4, "overlay-relative", lambda v, o: v if 0 < v < N else None)
find_tables(2, "u16 overlay-relative", lambda v, o: v if 0 < v < N else None)
# relative to the table's own start is common
find_tables(4, "relative to table start", lambda v, o: None)

# self-relative: value + its own address
find_tables(4, "self-relative (v+addr)", lambda v, o: (v + o) if 0 < v + o < N else None)
find_tables(2, "u16 self-relative", lambda v, o: (v + o) if 0 < v + o < N else None)


# --- table-start-relative needs a two-pass approach ---
def find_rel_tables(width):
    read = u32 if width == 4 else u16
    best = []
    o = 0
    while o < N - width * MINRUN:
        v0 = read(o)
        for base in (o, o - v0):
            pass
        o += width
    return best


# --- what does the head of the dense text area look like? ---
print("\n--- hex around the first strings (0x100-0x200) ---")
for row in range(0x100, 0x200, 16):
    print(f"  {row:05X}  {ov[row:row+16].hex(' ')}")

# --- distribution: how are the 0x88000 chunk strings addressed? ---
print("\n--- hex at 0x88000 (dense text chunk) ---")
for row in range(0x88000, 0x88060, 16):
    print(f"  {row:05X}  {ov[row:row+16].hex(' ')}")
