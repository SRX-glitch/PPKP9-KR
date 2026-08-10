#!/usr/bin/env python3
"""Find BIOS decompression SWI call sites in ARM9 + overlays. Reveals the codec
(BitUnPack/LZ77/Huffman/RLE) used for graphics/font, and gives breakpointable
addresses where r0=source, r1=dest can be read live."""
import struct
ROM="/mnt/c/Users/jngji/Desktop/실험실/rom/Power Pro Kun Pocket 9 (Japan).nds"
d=open(ROM,"rb").read()
def u32(b,o): return struct.unpack_from("<I",b,o)[0]
arm9_off=u32(d,0x20); arm9_ram=u32(d,0x28); arm9_size=u32(d,0x2C)
ov9_off=u32(d,0x50); ov9_size=u32(d,0x54); fat_off=u32(d,0x48)
regions=[("arm9",arm9_off,arm9_off+arm9_size,arm9_ram)]
for i in range(ov9_size//32):
    e=ov9_off+i*32; ovid=u32(d,e); ram=u32(d,e+4); fid=u32(d,e+24)
    fs=u32(d,fat_off+fid*8); fe=u32(d,fat_off+fid*8+4)
    regions.append((f"ov{ovid:02d}",fs,fe,ram))

# ARM SWI (ARM9): 0xEF0000NN? NDS BIOS uses comment high byte as func: 0xEFNN0000
swis={0x10:"BitUnPack",0x11:"LZ77UnCompWram",0x12:"LZ77UnCompVram",
      0x13:"HuffUnComp",0x14:"RLUnCompWram",0x15:"RLUnCompVram",0x19:"Diff8bitUnFilterWram"}
# ARM encoding 0xEF<NN>0000 little-endian bytes: 00 00 NN EF
# THUMB SWI: 0xDFNN (byte1=0xDF, byte0=NN)
print("=== ARM decompression SWIs (00 00 NN EF) ===")
for name,s,e,ram in regions:
    blob=d[s:e]
    for nn,label in swis.items():
        pat=bytes([0x00,0x00,nn,0xEF])
        off=0; locs=[]
        while True:
            i=blob.find(pat,off)
            if i<0: break
            if i%4==0: locs.append(ram+i)  # aligned = real instruction
            off=i+1
        if locs:
            print(f"  {label:16} SWI 0x{nn:02X} in {name}: {len(locs)}x  ram={[hex(x) for x in locs[:5]]}")
print("\n=== THUMB decompression SWIs (NN DF) ===")
for name,s,e,ram in regions:
    blob=d[s:e]
    for nn,label in swis.items():
        pat=bytes([nn,0xDF])
        off=0; locs=[]
        while True:
            i=blob.find(pat,off)
            if i<0: break
            if i%2==0: locs.append(ram+i)
            off=i+1
        if len(locs)>=1:
            print(f"  {label:16} SWI 0x{nn:02X} in {name}: {len(locs)}x  ram={[hex(x) for x in locs[:5]]}")
