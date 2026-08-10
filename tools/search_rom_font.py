#!/usr/bin/env python3
"""Search the ROM directly for the confirmed VRAM font glyph tiles (4bpp, from
VRAM 0x06208000 = kbd_subBG.bin[0x8000:0xC000]). If found -> font is uncompressed
in ROM and directly patchable."""
import os, struct
sd=os.path.join(os.path.dirname(__file__),"..","survey")
rom=open("/mnt/c/Users/jngji/Desktop/실험실/rom/Power Pro Kun Pocket 9 (Japan).nds","rb").read()
vram=open(os.path.join(sd,"kbd_subBG.bin"),"rb").read()

# also load NitroFS names to map any hit to a file
def u16(b,o): return struct.unpack_from("<H",b,o)[0]
def u32(b,o): return struct.unpack_from("<I",b,o)[0]
fnt_off=u32(rom,0x40); fat_off=u32(rom,0x48); fat_size=u32(rom,0x4C)
fat=[(u32(rom,fat_off+i*8),u32(rom,fat_off+i*8+4)) for i in range(fat_size//8)]
names={}
def walk(dir_id,prefix):
    idx=dir_id&0xFFF; sub=u32(rom,fnt_off+idx*8); first=u16(rom,fnt_off+idx*8+4)
    p=fnt_off+sub; fid=first
    while True:
        t=rom[p]; p+=1
        if t==0: break
        ln=t&0x7F; isdir=(t&0x80)!=0; nm=rom[p:p+ln].decode("ascii","replace"); p+=ln
        if isdir: s=u16(rom,p); p+=2; walk(s,prefix+"/"+nm)
        else: names[fid]=prefix+"/"+nm; fid+=1
walk(0xF000,"")
def file_of(off):
    for fid,(s,e) in enumerate(fat):
        if s<=off<e: return names.get(fid,f"fid{fid}")
    return "(arm9/ovl/system)"

hits=0; checked=0
locs=[]
for off in range(0x8000,0xC000,32):
    t=vram[off:off+32]
    ink=sum(bin(b).count("1") for b in t)
    if not (60<ink<200): continue   # glyph-like density
    if len(set(t))<6: continue
    checked+=1
    idx=rom.find(t)
    if idx>=0:
        hits+=1; locs.append(idx)
        if hits<=15:
            print(f"VRAM font 0x{off:X} -> ROM 0x{idx:X} [{file_of(idx)}]")
print(f"\nchecked {checked} font glyphs, {hits} found VERBATIM in ROM")
if locs:
    locs.sort()
    print(f"ROM span: 0x{locs[0]:X}..0x{locs[-1]:X}  file: {file_of(locs[0])}")
else:
    print("=> VRAM 4bpp font NOT in ROM verbatim: font is compressed or built at runtime.")
