#!/usr/bin/env python3
"""Locate code that references the font VRAM address: search ARM9 + overlays for
the 32-bit LE constants 0x06208000 / 0x06200000 (ARM literal pools). Those sites
are near the font upload/blit routine (the next RE target)."""
import struct
ROM="/mnt/c/Users/jngji/Desktop/실험실/rom/Power Pro Kun Pocket 9 (Japan).nds"
d=open(ROM,"rb").read()
def u32(b,o): return struct.unpack_from("<I",b,o)[0]

# build map of code regions: arm9 + overlays (ROM extent -> ram base)
arm9_off=u32(d,0x20); arm9_ram=u32(d,0x28); arm9_size=u32(d,0x2C)
ov9_off=u32(d,0x50); ov9_size=u32(d,0x54); fat_off=u32(d,0x48)
regions=[("arm9",arm9_off,arm9_off+arm9_size,arm9_ram)]
for i in range(ov9_size//32):
    e=ov9_off+i*32; ovid=u32(d,e); ram=u32(d,e+4); fid=u32(d,e+24)
    fs=u32(d,fat_off+fid*8); fe=u32(d,fat_off+fid*8+4)
    regions.append((f"ov{ovid:02d}",fs,fe,ram))

targets={0x06208000:"font(SUB BG0 char)",0x06200000:"SUB BG base",0x06000000:"MAIN BG base",
         0x040000B0:"DMA0",0x040000BC:"DMA1",0x040000C8:"DMA2",0x040000D4:"DMA3"}
for tval,label in targets.items():
    pat=struct.pack("<I",tval)
    total=0
    for name,s,e,ram in regions:
        blob=d[s:e]; off=0; local=[]
        while True:
            i=blob.find(pat,off)
            if i<0: break
            local.append(i); off=i+1
        if local:
            total+=len(local)
            ramlocs=[f"0x{ram+i:X}" for i in local[:4]]
            print(f"  0x{tval:08X} {label:18} in {name}: {len(local)}x  ram~{ramlocs}")
    if total==0:
        print(f"  0x{tval:08X} {label:18} : not found as literal")
