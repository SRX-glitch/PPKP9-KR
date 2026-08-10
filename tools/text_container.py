#!/usr/bin/env python3
"""Which NitroFS file holds the dialogue, and is there a pointer table in it?"""
import os, sys, struct
sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

ROM = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
rom = open(ROM, "rb").read()
u32 = lambda o: int.from_bytes(rom[o:o + 4], "little")

fat_off, fat_len = u32(0x48), u32(0x4C)
nfiles = fat_len // 8
print(f"FAT @0x{fat_off:X}, {nfiles} files")

TARGETS = [0x4CE3FC, 0x55E18D, 0x54E339, 0x4D2220]
files = [(u32(fat_off + i * 8), u32(fat_off + i * 8 + 4)) for i in range(nfiles)]

for t in TARGETS:
    hit = [(i, s, e) for i, (s, e) in enumerate(files) if s <= t < e]
    if hit:
        i, s, e = hit[0]
        print(f"0x{t:07X} -> file #{i}  0x{s:07X}-0x{e:07X}  ({(e-s)/1024:.0f} KB), "
              f"offset in file 0x{t-s:X}")
    else:
        print(f"0x{t:07X} -> not inside any FAT file (ARM9/overlay/header area?)")

# For the main dialogue file, look for a pointer table at its head.
hit = [(i, s, e) for i, (s, e) in enumerate(files) if s <= TARGETS[1] < e]
if hit:
    i, s, e = hit[0]
    print(f"\n--- head of file #{i} (0x{s:07X}) ---")
    print(rom[s:s + 64].hex(" "))
    n = u32(s)
    print(f"first u32 = {n} (0x{n:X})")
    # test the "count + u32 offsets" layout
    for base_guess, label in ((s, "file-relative"), (0, "absolute")):
        ok = 0
        for k in range(1, min(n + 1, 200)) if 0 < n < 100000 else []:
            v = u32(s + k * 4)
            a = base_guess + v
            if s <= a < e and 1 <= rom[a] <= 247:
                ok += 1
        print(f"  as count+{label} table: {ok}/{min(n,199)} entries land on text")
    # does any u32 in the first 64KB of the file point at our known string?
    want = TARGETS[1] - s
    found = []
    for o in range(s, min(s + 0x20000, e), 4):
        if u32(o) == want:
            found.append(o - s)
    print(f"  u32 == 0x{want:X} (file-relative ptr to the known string): "
          f"{len(found)} hits {[hex(x) for x in found[:5]]}")
    want2 = TARGETS[1]
    found2 = [o - s for o in range(s, min(s + 0x20000, e), 4) if u32(o) == want2]
    print(f"  u32 == 0x{want2:X} (absolute): {len(found2)} hits")
