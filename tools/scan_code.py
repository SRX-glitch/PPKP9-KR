#!/usr/bin/env python3
"""Extract ARM9 + overlays (unnamed FAT entries) and scan for Japanese text and
readable strings, to locate the text engine / script tables. Read-only."""
import struct, sys, os

def u16(b,o): return struct.unpack_from("<H",b,o)[0]
def u32(b,o): return struct.unpack_from("<I",b,o)[0]

def jp_sjis_pairs(b):
    n=len(b); i=0; jp=0
    while i<n-1:
        c=b[i]
        if (0x81<=c<=0x9F) or (0xE0<=c<=0xEF):
            c2=b[i+1]
            if (0x40<=c2<=0x7E) or (0x80<=c2<=0xFC):
                jp+=1; i+=2; continue
        i+=1
    return jp

def ascii_strings(b, minlen=4):
    out=[]; cur=[]
    for c in b:
        if 0x20<=c<0x7F:
            cur.append(chr(c))
        else:
            if len(cur)>=minlen: out.append("".join(cur))
            cur=[]
    if len(cur)>=minlen: out.append("".join(cur))
    return out

def main():
    rom=sys.argv[1]; outdir=sys.argv[2]
    os.makedirs(outdir,exist_ok=True)
    d=open(rom,"rb").read()
    arm9_off=u32(d,0x20); arm9_size=u32(d,0x2C)
    ov9_off=u32(d,0x50); ov9_size=u32(d,0x54)
    fat_off=u32(d,0x48)
    arm9=d[arm9_off:arm9_off+arm9_size]
    open(os.path.join(outdir,"arm9.bin"),"wb").write(arm9)
    print(f"ARM9 size={len(arm9)} jp_sjis_pairs={jp_sjis_pairs(arm9)}")

    # overlay table: each entry 32 bytes: id, ram_addr, ram_size, bss, sinit_start, sinit_end, file_id, reserved
    ncount=ov9_size//32
    print(f"\n=== ARM9 overlays: {ncount} ===")
    rows=[]
    for i in range(ncount):
        e=ov9_off+i*32
        ovid=u32(d,e); ram=u32(d,e+4); ramsz=u32(d,e+8)
        fileid=u32(d,e+24)
        fs=u32(d,fat_off+fileid*8); fe=u32(d,fat_off+fileid*8+4)
        b=d[fs:fe]
        jp=jp_sjis_pairs(b)
        rows.append((ovid,fileid,ram,ramsz,len(b),jp,fs,fe))
    for r in sorted(rows,key=lambda x:-x[5])[:40]:
        print(f"  ov{r[0]:<3} file={r[1]:<4} ram=0x{r[2]:08X} size={r[4]:8} jp_pairs={r[5]:6}")
    # dump the top-jp overlay for inspection
    top=sorted(rows,key=lambda x:-x[5])[0]
    b=d[top[6]:top[7]]
    open(os.path.join(outdir,f"ov{top[0]:02d}.bin"),"wb").write(b)
    print(f"\nDumped highest-jp overlay ov{top[0]} -> {outdir}/ov{top[0]:02d}.bin")

    # ascii strings in arm9 that look like filenames/paths/format tokens
    ss=ascii_strings(arm9,5)
    interesting=[s for s in ss if any(k in s.lower() for k in
        (".bin",".narc","msg","font","fnt","text",".dat","/","%d","%s","str","load","file"))]
    print(f"\n=== ARM9 interesting ASCII strings (sample of {len(interesting)}) ===")
    for s in interesting[:60]:
        print("   ", s)

if __name__=="__main__":
    main()
