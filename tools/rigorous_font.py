#!/usr/bin/env python3
"""Rigorously find the compressed font: try LZ77(0x10) AND LZ11(0x11) on every
NitroFS file (and every overlay), and count how many DISTINCTIVE VRAM font glyphs
appear in each decompressed output. High count = the font file + its codec."""
import sys, os, struct
ROM=sys.argv[1]; VRAM=sys.argv[2]
rom=open(ROM,"rb").read(); vram=open(VRAM,"rb").read()
def u16(b,o): return struct.unpack_from("<H",b,o)[0]
def u32(b,o): return struct.unpack_from("<I",b,o)[0]

# distinctive reference glyphs: high unique-byte count, mid density (avoid common tiles)
refs=[]
for o in range(0x8000,0xC000,32):
    t=vram[o:o+32]; ink=sum(bin(x).count("1") for x in t)
    if 90<ink<170 and len(set(t))>=10:
        refs.append(bytes(t))
refset=set(refs)
print(f"{len(refset)} distinctive reference font glyphs")

def lz10(data):
    if not data or data[0]!=0x10: return None
    size=data[1]|(data[2]<<8)|(data[3]<<16)
    if not (0x800<size<0x200000): return None
    out=bytearray(); p=4
    try:
        while len(out)<size and p<len(data):
            fl=data[p]; p+=1
            for b in range(8):
                if len(out)>=size: break
                if fl&(0x80>>b):
                    b0=data[p]; b1=data[p+1]; p+=2
                    ln=(b0>>4)+3; disp=(((b0&0xF)<<8)|b1)+1
                    if disp>len(out): return None
                    for _ in range(ln):
                        out.append(out[-disp])
                        if len(out)>=size: break
                else: out.append(data[p]); p+=1
        return bytes(out)
    except: return None

def lz11(data):
    if not data or data[0]!=0x11: return None
    size=data[1]|(data[2]<<8)|(data[3]<<16)
    if not (0x800<size<0x200000): return None
    out=bytearray(); p=4
    try:
        while len(out)<size and p<len(data):
            fl=data[p]; p+=1
            for b in range(8):
                if len(out)>=size: break
                if fl&(0x80>>b):
                    b0=data[p]; b1=data[p+1]
                    ind=b0>>4
                    if ind==0:
                        b2=data[p+2]; p+=3
                        ln=(((b0&0xF)<<4)|(b1>>4))+0x11
                        disp=(((b1&0xF)<<8)|b2)+1
                    elif ind==1:
                        b2=data[p+2]; b3=data[p+3]; p+=4
                        ln=(((b0&0xF)<<12)|(b1<<4)|(b2>>4))+0x111
                        disp=(((b2&0xF)<<8)|b3)+1
                    else:
                        p+=2
                        ln=ind+1
                        disp=(((b0&0xF)<<8)|b1)+1
                    if disp>len(out): return None
                    for _ in range(ln):
                        out.append(out[-disp])
                        if len(out)>=size: break
                else: out.append(data[p]); p+=1
        return bytes(out)
    except: return None

def count_font(dec):
    if not dec or len(dec)<0x800: return 0
    c=0
    for o in range(0,len(dec)-32,32):
        if dec[o:o+32] in refset: c+=1
    return c

# enumerate files + overlays
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

results=[]
for fid,(s,e) in enumerate(fat):
    if e-s<0x200: continue
    blob=rom[s:e]
    for codec,fn in (("LZ10",lz10),("LZ11",lz11)):
        dec=fn(blob)
        c=count_font(dec)
        if c>=8:
            results.append((c,names.get(fid,f"fid{fid}"),hex(s),codec,len(dec)))
results.sort(reverse=True)
print(f"\n=== candidate compressed-font files (>=8 distinctive glyphs) ===")
for c,nm,s,codec,dl in results[:15]:
    print(f"  {c:4} glyphs  {codec}  {nm} @{s} -> {dl}B")
if not results:
    print("  none — font not a whole-file LZ10/LZ11; may be embedded/other codec.")
