#!/usr/bin/env python3
"""Overlay 28 script format.

Established from windows: text is inline, introduced by `F8 6B <box>` and ended
by the next byte >= 0xF8 (or 0x00). F8/FD/FE/FF are command prefixes.

Goal: decide whether strings can be repacked, i.e. does anything encode an
absolute or relative POSITION in the stream?
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

OUT = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/ov28"
ov = open(os.path.join(OUT, "ov28.bin"), "rb").read()
RAM = 0x021C0DC0
N = len(ov)
u32 = lambda o: int.from_bytes(ov[o:o + 4], "little")
u16 = lambda o: int.from_bytes(ov[o:o + 2], "little")

# ---- 1. where are the script regions? use F8 6B density ----
tx = [i for i in range(N - 2) if ov[i] == 0xF8 and ov[i + 1] == 0x6B]
print(f"`F8 6B` text commands: {len(tx)}")
chunks = collections.Counter(i // 0x4000 for i in tx)
hot = sorted(c for c, n in chunks.items() if n >= 10)
print(f"16KB chunks with >=10 text cmds: {len(hot)}")


def merge(bs, gap=1):
    out = []
    s = p = bs[0]
    for x in bs[1:]:
        if x - p <= gap:
            p = x; continue
        out.append((s, p)); s = p = x
    out.append((s, p))
    return out


regions = [(s * 0x4000, (e + 1) * 0x4000) for s, e in merge(hot)]
print("script regions:")
for s, e in regions:
    print(f"  0x{s:06X}-0x{e:06X}  {(e-s)/1024:5.0f} KB  "
          f"{sum(1 for i in tx if s <= i < e):5d} text cmds")
first_script = regions[0][0]
last_script = regions[-1][1]

# ---- 2. operand histograms for the command prefixes ----
print("\ncommand byte following each prefix (top 12):")
for pre in (0xF8, 0xFD, 0xFE, 0xFF, 0xD0, 0xD7):
    nxt = collections.Counter(ov[i + 1] for i in range(N - 1) if ov[i] == pre)
    top = ", ".join(f"{b:02X}:{c}" for b, c in nxt.most_common(12))
    print(f"  {pre:02X} -> {top}")

# ---- 3. do FD/FE operands look like positions? ----
print("\nFD/FE 16-bit operand distribution:")
for pre in (0xFD, 0xFE):
    vals_le = collections.Counter()
    for i in range(N - 3):
        if ov[i] == pre:
            vals_le[u16(i + 1)] += 1
    mx = max(vals_le) if vals_le else 0
    print(f"  {pre:02X}: {len(vals_le)} distinct 16-bit operands, max 0x{mx:04X} "
          f"({'too small to address 588KB' if mx < N else 'could be an offset'})")
    print(f"      most common: {[(f'{v:04X}', c) for v, c in vals_le.most_common(6)]}")

# ---- 4. the 4085 self-pointers: what do they target? ----
sp = []
for o in range(0, N - 3, 4):
    v = u32(o)
    if RAM <= v < RAM + N:
        sp.append((o, v - RAM))
tgt = collections.Counter(d for _, d in sp)
in_script = [(s, d) for s, d in sp if first_script <= d < last_script]
print(f"\nself-pointers: {len(sp)}; targeting the script regions: {len(in_script)}")
if in_script:
    # do they point at a command boundary?
    at_cmd = sum(1 for _, d in in_script if ov[d] in (0xF8, 0xFD, 0xFE, 0xFF, 0xD0))
    print(f"  landing on a command prefix byte: {at_cmd}/{len(in_script)}")
    srcs = sorted(s for s, _ in in_script)
    print(f"  their sources span 0x{srcs[0]:06X}-0x{srcs[-1]:06X}")
    sb = collections.Counter(s // 0x4000 for s in srcs)
    print(f"  source chunks: {[(f'{c*0x4000:#x}', n) for c, n in sb.most_common(6)]}")

# ---- 5. is the pointer set an ordered table? ----
if in_script:
    runs = 0
    best = 0
    prev = None
    cur = 0
    for s, d in sorted(in_script):
        if prev is not None and s == prev + 4:
            cur += 1
            best = max(best, cur)
        else:
            cur = 1
        prev = s
    print(f"  longest run of consecutive 4-byte-spaced pointers: {best}")
