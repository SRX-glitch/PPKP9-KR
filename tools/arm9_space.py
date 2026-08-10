#!/usr/bin/env python3
"""NDS header + hunt for reusable slack inside the ARM9 static binary."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import fontcodec as F

ROM = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
rom = open(ROM, "rb").read()
u32 = lambda o: int.from_bytes(rom[o:o + 4], "little")

a9_off, a9_entry, a9_ram, a9_size = u32(0x20), u32(0x24), u32(0x28), u32(0x2C)
a7_off, a7_entry, a7_ram, a7_size = u32(0x30), u32(0x34), u32(0x38), u32(0x3C)
print(f"ARM9: rom 0x{a9_off:X} ram 0x{a9_ram:08X} size 0x{a9_size:X} entry 0x{a9_entry:08X}")
print(f"      ram end 0x{a9_ram + a9_size:08X}   rom end 0x{a9_off + a9_size:X}")
print(f"ARM7: rom 0x{a7_off:X} ram 0x{a7_ram:08X} size 0x{a7_size:X}")
print(f"FNT 0x{u32(0x40):X}/{u32(0x44)}  FAT 0x{u32(0x48):X}/{u32(0x4C)}")
print(f"ov9 tbl 0x{u32(0x50):X} size {u32(0x54)}   ov7 tbl 0x{u32(0x58):X} size {u32(0x5C)}")
print(f"rom used size 0x{u32(0x80):X}  header size 0x{u32(0x84):X}  total file 0x{len(rom):X}")

# font data extent
tbl = F.load_table(rom)
ptrs = sorted(set(tbl))
print(f"\nfont glyph data RAM 0x{ptrs[0]:08X}..0x{ptrs[-1] + 0x900:08X}"
      f"  = ROM 0x{F.ram2rom(ptrs[0]):X}..0x{F.ram2rom(ptrs[-1]) + 0x900:X}"
      f"  ({(ptrs[-1] + 0x900 - ptrs[0]):#x} bytes, {len(ptrs)} blocks)")

# slack hunt inside ARM9 static
def slack(buf, base_rom, minlen=0x200):
    runs = []
    i = 0
    n = len(buf)
    while i < n:
        b = buf[i]
        if b not in (0x00, 0xFF):
            i += 1
            continue
        j = i
        while j < n and buf[j] == b:
            j += 1
        if j - i >= minlen:
            runs.append((base_rom + i, j - i, b))
        i = j
    return runs

a9 = rom[a9_off:a9_off + a9_size]
runs = slack(a9, a9_off)
runs.sort(key=lambda r: -r[1])
total = sum(r[1] for r in runs)
print(f"\nARM9 static slack runs >=0x200: {len(runs)}, total {total:#x} bytes")
for o, ln, b in runs[:15]:
    print(f"  ROM 0x{o:06X}  RAM 0x{o - 0x4000 + 0x02000000:08X}  len {ln:#7x}  fill {b:02X}")

need = 10 * 0x900
print(f"\nneed for 10 filler blocks: {need:#x} ({need}) bytes")
usable = [r for r in runs if r[1] >= 0x900]
print(f"runs big enough for >=1 block: {len(usable)}, capacity "
      f"{sum(r[1] // 0x900 for r in usable)} blocks")
