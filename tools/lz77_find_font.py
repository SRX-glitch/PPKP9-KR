#!/usr/bin/env python3
"""Find the compressed font: LZ77(0x10)-decompress ROM files/overlays and check
whether the output contains the confirmed VRAM font glyphs (kbd_subBG 0x8000+)."""
import os, struct
sd=os.path.join(os.path.dirname(__file__),"..","survey")
rom=open("/mnt/c/Users/jngji/Desktop/실험실/rom/Power Pro Kun Pocket 9 (Japan).nds","rb").read()
vram=open(os.path.join(sd,"kbd_subBG.bin"),"rb").read()
def u16(b,o): return struct.unpack_from("<H",b,o)[0]
def u32(b,o): return struct.unpack_from("<I",b,o)[0]

# reference font glyphs to detect
refs=[vram[o:o+32] for o in range(0x8000,0xC000,32)
      if 60<sum(bin(x).count("1") for x in vram[o:o+32])<200 and len(set(vram[o:o+32]))>=6]
refset=set(bytes(r) for r in refs)

def lz77(data, off):
    if off>=len(data) or data[off]!=0x10: return None
    size=data[off+1]|(data[off+2]<<8)|(data[off+3]<<16)
    if size==0 or size>0x200000: return None
    out=bytearray(); p=off+4
    try:
        while len(out)<size and p<len(data):
            flags=data[p]; p+=1
            for b in range(8):
                if len(out)>=size: break
                if flags&(0x80>>b):
                    if p+1>=len(data): return None
                    b0=data[p]; b1=data[p+1]; p+=2
                    ln=(b0>>4)+3; disp=(((b0&0xF)<<8)|b1)+1
                    if disp>len(out): return None
                    for _ in range(ln):
                        out.append(out[len(out)-disp])
                        if len(out)>=size: break
                else:
                    out.append(data[p]); p+=1
        return bytes(out)
    except: return None

def contains_font(dec):
    if not dec or len(dec)<0x1000: return 0
    c=0
    for o in range(0,len(dec)-32,32):
        if dec[o:o+32] in refset:
            c+=1
            if c>=3: return c
    return c

# enumerate files
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

print(f"{len(refset)} reference font glyphs")
found=[]
for fid,(s,e) in enumerate(fat):
    if e<=s or e-s<0x400: continue
    # try LZ77 at file start
    if rom[s]==0x10:
        dec=lz77(rom,s)
        c=contains_font(dec)
        if c>=3:
            found.append((names.get(fid,f"fid{fid}"),s,e,c,len(dec) if dec else 0))
            print(f"  MATCH file '{names.get(fid,fid)}' @0x{s:X} size={e-s} -> decomp {len(dec)}B, {c}+ font glyphs")
print(f"\n{len(found)} compressed-font file(s) found")
if not found:
    print("no LZ77-at-start file decompresses to the VRAM font; font may use a different codec/offset.")
