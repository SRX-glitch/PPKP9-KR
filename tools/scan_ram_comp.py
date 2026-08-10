#!/usr/bin/env python3
"""Scan the full RAM dump for LZ10/LZ11 compressed blocks that decompress to
contain the VRAM font glyphs. Finds the compressed font's live location + codec.
Also reports where the decompressed 4bpp font appears verbatim in RAM (if any)."""
import sys, os, struct
sd=os.path.join(os.path.dirname(__file__),"..","survey")
ram=open(os.path.join(sd,"main_full.bin"),"rb").read()
vram=open(os.path.join(sd,"kbd_subBG.bin"),"rb").read()

# reference glyphs (loosened but distinctive)
refs=set()
for o in range(0x8000,0xC000,32):
    t=vram[o:o+32]; ink=sum(bin(x).count("1") for x in t)
    if 40<ink<210 and len(set(t))>=8: refs.add(bytes(t))
print(f"{len(refs)} reference font glyphs")

def lz10(data):
    if len(data)<4 or data[0]!=0x10: return None
    size=data[1]|(data[2]<<8)|(data[3]<<16)
    if not (0x400<size<0x100000): return None
    out=bytearray(); p=4
    try:
        while len(out)<size and p<len(data):
            fl=data[p]; p+=1
            for b in range(8):
                if len(out)>=size: break
                if fl&(0x80>>b):
                    b0=data[p]; b1=data[p+1]; p+=2
                    ln=(b0>>4)+3; disp=(((b0&0xF)<<8)|b1)+1
                    if disp>len(out) or disp==0: return None
                    for _ in range(ln):
                        out.append(out[-disp])
                        if len(out)>=size: break
                else: out.append(data[p]); p+=1
        return bytes(out)
    except: return None

def lz11(data):
    if len(data)<4 or data[0]!=0x11: return None
    size=data[1]|(data[2]<<8)|(data[3]<<16)
    if not (0x400<size<0x100000): return None
    out=bytearray(); p=4
    try:
        while len(out)<size and p<len(data):
            fl=data[p]; p+=1
            for b in range(8):
                if len(out)>=size: break
                if fl&(0x80>>b):
                    b0=data[p]; b1=data[p+1]; ind=b0>>4
                    if ind==0:
                        b2=data[p+2]; p+=3; ln=(((b0&0xF)<<4)|(b1>>4))+0x11; disp=(((b1&0xF)<<8)|b2)+1
                    elif ind==1:
                        b2=data[p+2]; b3=data[p+3]; p+=4; ln=(((b0&0xF)<<12)|(b1<<4)|(b2>>4))+0x111; disp=(((b2&0xF)<<8)|b3)+1
                    else:
                        p+=2; ln=ind+1; disp=(((b0&0xF)<<8)|b1)+1
                    if disp>len(out) or disp==0: return None
                    for _ in range(ln):
                        out.append(out[-disp])
                        if len(out)>=size: break
                else: out.append(data[p]); p+=1
        return bytes(out)
    except: return None

def count_font(dec):
    if not dec: return 0
    c=0
    for o in range(0,len(dec)-32,4):   # step 4 (glyphs may not be 32-aligned in output)
        if dec[o:o+32] in refs: c+=1
    return c

# 1) is the decompressed 4bpp font present verbatim in RAM?
print("\n=== verbatim 4bpp font in RAM? ===")
sample=list(refs)[:8]; vb=0
for r in sample:
    if ram.find(r)>=0: vb+=1
print(f"  {vb}/{len(sample)} sample glyphs present verbatim in RAM")

# 2) scan RAM for compressed blocks decompressing to the font
print("\n=== scanning RAM for LZ10/LZ11 blocks -> font ===")
hits=[]
i=0
while i < len(ram)-8:
    b=ram[i]
    if b in (0x10,0x11):
        sz=ram[i+1]|(ram[i+2]<<8)|(ram[i+3]<<16)
        if 0x400<sz<0x100000:
            dec = lz10(ram[i:i+0x40000]) if b==0x10 else lz11(ram[i:i+0x40000])
            c=count_font(dec)
            if c>=6:
                hits.append((i,b,len(dec) if dec else 0,c))
                print(f"  RAM 0x{i:X} codec={'LZ10' if b==0x10 else 'LZ11'} decomp={len(dec)}B font_glyphs={c}")
                i+= max(0x100,(len(dec) or 0)//8)
                continue
    i+=4
print(f"\n{len(hits)} compressed-font block(s) in RAM")
