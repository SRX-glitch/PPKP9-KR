#!/usr/bin/env python3
"""Map file #25 to its overlay, then hunt for RAM pointers to known strings."""
import sys, os
ROM = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
rom = open(ROM, "rb").read()
u32 = lambda o: int.from_bytes(rom[o:o + 4], "little")

ov_off, ov_len = u32(0x50), u32(0x54)
fat_off = u32(0x48)
n = ov_len // 32
print(f"overlay table @0x{ov_off:X}: {n} overlays")
target_file = 25
ent = None
for i in range(n):
    o = ov_off + i * 32
    oid, ram, size, bss, sinit_s, sinit_e, fid, _ = [u32(o + k * 4) for k in range(8)]
    fs, fe = u32(fat_off + fid * 8), u32(fat_off + fid * 8 + 4)
    if i < 8 or fid == target_file:
        print(f"  ov{oid:<3} ram 0x{ram:08X} size 0x{size:<6X} bss 0x{bss:<5X} "
              f"file#{fid} 0x{fs:07X}-0x{fe:07X}")
    if fid == target_file:
        ent = (oid, ram, size, fs, fe)

if not ent:
    sys.exit("file #25 is not an overlay")
oid, ram, size, fs, fe = ent
print(f"\n=> overlay {oid} loads at RAM 0x{ram:08X}, file 0x{fs:07X}-0x{fe:07X}")

STRINGS = {0x055E18D: "よくわからないけど…", 0x054E339: "だから諦めるしかない…",
           0x04CE3FC: "何もする気に…", 0x04D2220: "良くない事が…"}
for off, label in STRINGS.items():
    want = ram + (off - fs)
    hits = [o - fs for o in range(fs, fe, 4) if u32(o) == want]
    print(f"  0x{off:07X} -> RAM 0x{want:08X}  pointers found in overlay: {len(hits)}"
          f"  {[hex(h) for h in hits[:6]]}")

# also scan ARM9 static for those pointers
a9_off, a9_ram, a9_size = u32(0x20), u32(0x28), u32(0x2C)
for off in list(STRINGS)[:2]:
    want = ram + (off - fs)
    hits = [o - a9_off for o in range(a9_off, a9_off + a9_size, 4) if u32(o) == want]
    print(f"  in ARM9 static: 0x{want:08X} -> {len(hits)} hits")
