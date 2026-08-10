#!/usr/bin/env python3
"""Static font hunt across the whole ROM: known DS font magics + NitroFS font
files + fixed-cell glyph-region heuristic on ARM9/overlays/.bin files."""
import struct, sys, os
d=open(sys.argv[1],"rb").read()
def u32(b,o): return struct.unpack_from("<I",b,o)[0]
def u16(b,o): return struct.unpack_from("<H",b,o)[0]

# --- enumerate files (reuse survey logic) ---
fnt_off=u32(d,0x40); fat_off=u32(d,0x48); fat_size=u32(d,0x4C)
fat=[(u32(d,fat_off+i*8),u32(d,fat_off+i*8+4)) for i in range(fat_size//8)]
names={}
def walk(dir_id,prefix):
    idx=dir_id&0xFFF; sub=u32(d,fnt_off+idx*8); first=u16(d,fnt_off+idx*8+4)
    p=fnt_off+sub; fid=first
    while True:
        t=d[p]; p+=1
        if t==0: break
        ln=t&0x7F; isdir=(t&0x80)!=0
        nm=d[p:p+ln].decode("ascii","replace"); p+=ln
        if isdir:
            s=u16(d,p); p+=2; walk(s,prefix+"/"+nm)
        else:
            names[fid]=prefix+"/"+nm; fid+=1
walk(0xF000,"")

# --- 1. known font magics anywhere in ROM ---
magics=[b"RTFN",b"NFTR",b"NFGR",b"RGCN",b"NCGR",b"RLCN",b"NCLR",b"RCSN",b"NSCR"]
print("=== font/graphics magics in whole ROM ===")
for m in magics:
    idxs=[]; start=0
    while True:
        i=d.find(m,start)
        if i<0: break
        idxs.append(i); start=i+1
        if len(idxs)>=6: break
    if idxs:
        # map offset to file if possible
        locs=[]
        for i in idxs[:6]:
            f=next((names[fid] for fid,(s,e) in enumerate(fat) if fid in names and s<=i<e), "?")
            locs.append(f"0x{i:X}({f})")
        print(f"  {m.decode()}: {len(idxs)}+  {locs}")

# --- 2. NitroFS files whose name suggests font ---
print("\n=== files with font-ish names ===")
for fid,path in sorted(names.items()):
    low=path.lower()
    if any(k in low for k in ("font","fnt","nftr","glyph","moji","font","kanji",".nbfc",".nbfp","char")):
        if fid<len(fat):
            s,e=fat[fid]; print(f"  {path}  size={e-s}")

# --- 3. fixed-cell glyph heuristic: scan ARM9+overlays+big files for regions
#        that look like 1bpp/2bpp bitmap font (regular ink density per cell) ---
ov9_off=u32(d,0x50); ov9_size=u32(d,0x54)
blobs=[("arm9",d[u32(d,0x20):u32(d,0x20)+u32(d,0x2C)])]
for i in range(ov9_size//32):
    e=ov9_off+i*32; ovid=u32(d,e); fid=u32(d,e+24)
    s2=u32(d,fat_off+fid*8); e2=u32(d,fat_off+fid*8+4)
    blobs.append((f"ov{ovid:02d}",d[s2:e2]))
# add large .bin files
for fid,path in names.items():
    if fid<len(fat):
        s,e=fat[fid]
        if e-s>8000 and path.endswith(".bin"):
            blobs.append((path,d[s:e]))

def looks_fontish(b, cell=18):
    # 12x12 1bpp = 18 bytes; check windows for consistent mid-range ink density
    if len(b)<cell*64: return None
    best=None
    step=cell*32
    for base in range(0, len(b)-cell*64, step):
        dens=[]
        for g in range(64):
            chunk=b[base+g*cell:base+(g+1)*cell]
            bits=sum(bin(x).count("1") for x in chunk)
            dens.append(bits/(cell*8))
        mid=sum(1 for x in dens if 0.12<x<0.6)
        if mid>=48:  # most cells have font-like density
            return base
    return None

print("\n=== fixed-cell (12x12 1bpp) font-region candidates ===")
found=0
for name,b in blobs:
    for cell in (18,32,24):  # 12x12 1bpp, 16x16 1bpp, 16x12
        r=looks_fontish(b,cell)
        if r is not None:
            print(f"  {name}: candidate @0x{r:X} (cell={cell}B) size={len(b)}")
            found+=1; break
if not found:
    print("  (none — font likely compressed or non-1bpp)")
