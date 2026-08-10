#!/usr/bin/env python3
"""Standard NDS decompressors (LZ10/LZ11/Huff/RLE) applied to every NitroFS file;
look for NFTR/NCGR/NCLR magics or a match with the known decoded font tiles."""
import struct, os
ROM=open("/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds","rb").read()
def u16(b,o): return struct.unpack_from("<H",b,o)[0]
def u32(b,o): return struct.unpack_from("<I",b,o)[0]

# ---- NitroFS parse ----
fnt_off=u32(ROM,0x40); fat_off=u32(ROM,0x48); fat_size=u32(ROM,0x4C)
nfiles=fat_size//8
fat=[(u32(ROM,fat_off+i*8),u32(ROM,fat_off+i*8+4)) for i in range(nfiles)]

# ---- decompressors ----
def lz10(d):
    if not d or d[0]!=0x10: return None
    size=d[1]|(d[2]<<8)|(d[3]<<16); out=bytearray(); p=4
    try:
        while len(out)<size and p<len(d):
            fl=d[p]; p+=1
            for b in range(8):
                if len(out)>=size: break
                if fl&(0x80>>b):
                    if p+1>=len(d): return None
                    v=(d[p]<<8)|d[p+1]; p+=2
                    ln=(v>>12)+3; disp=(v&0xFFF)+1
                    if disp>len(out): return None
                    for _ in range(ln): out.append(out[-disp])
                else:
                    if p>=len(d): return None
                    out.append(d[p]); p+=1
    except: return None
    return bytes(out)
def lz11(d):
    if not d or d[0]!=0x11: return None
    size=d[1]|(d[2]<<8)|(d[3]<<16); out=bytearray(); p=4
    try:
        while len(out)<size and p<len(d):
            fl=d[p]; p+=1
            for b in range(8):
                if len(out)>=size or p>=len(d): break
                if fl&(0x80>>b):
                    a=d[p]; p+=1; ind=a>>4
                    if ind==0:
                        cnt=(a&0xF)<<4|(d[p]>>4); cnt+=0x11
                        disp=((d[p]&0xF)<<8|d[p+1])+1; p+=2
                    elif ind==1:
                        cnt=((a&0xF)<<12|d[p]<<4|d[p+1]>>4)+0x111; disp=((d[p+1]&0xF)<<8|d[p+2])+1; p+=3
                    else:
                        cnt=ind+1; disp=((a&0xF)<<8|d[p])+1; p+=1
                    if disp>len(out): return None
                    for _ in range(cnt): out.append(out[-disp])
                else:
                    out.append(d[p]); p+=1
    except: return None
    return bytes(out)
def huff(d):
    if not d or (d[0]&0xF0)!=0x20: return None  # 0x24/0x28
    return None  # skip full huff for now (rare for fonts)

MAGICS={b"RTFN":"NFTR",b"RGCN":"NCGR",b"RLCN":"NCLR",b"RCSN":"NSCR",b"RECN":"NCER",b"NFTR":"NFTR-fwd"}
# known decoded font tiles (from RAM buffer)
buf=open("/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/main_kbd_full.bin","rb").read()
ref=buf[0x2D3740-0x0:0x2D3740+0x400]  # wait, buf is main dump from 0x02000000, offset = 0x2D3740
ref=buf[0x2D3740:0x2D3740+0x800]  # 64 tiles of decoded font
needles=[ref[o:o+32] for o in range(0,len(ref),32) if 40<sum(bin(x).count("1") for x in ref[o:o+32])<180 and len(set(ref[o:o+32]))>6][:6]

hits=[]
for fid,(s,eoff) in enumerate(fat):
    if s>=len(ROM) or eoff<=s or eoff-s<256 or eoff>len(ROM): continue
    data=ROM[s:eoff]
    for name,fn in (("lz10",lz10),("lz11",lz11)):
        out=fn(data)
        if not out or len(out)<64: continue
        # magic check
        mg=out[:4]
        magic=MAGICS.get(mg) or MAGICS.get(bytes(reversed(mg)))
        # font-tile match
        matched=any(n in out for n in needles)
        if magic or matched:
            hits.append((fid,name,len(data),len(out),magic,matched))
            print(f"FID {fid} {name}: {len(data)}B -> {len(out)}B magic={magic} font_match={matched}")
# also raw magic scan (uncompressed NFTR/NCGR)
print("--- raw uncompressed magic scan across NitroFS files ---")
for fid,(s,eoff) in enumerate(fat):
    if s>=len(ROM) or eoff<=s or eoff>len(ROM): continue
    mg=ROM[s:s+4]
    m=MAGICS.get(mg) or MAGICS.get(bytes(reversed(mg)))
    if m: print(f"  FID {fid} raw magic {m} ({eoff-s}B)")
print("total compressed hits:", len(hits))
print("needles used:", len(needles))
