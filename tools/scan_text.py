#!/usr/bin/env python3
"""Scan every NitroFS file for Japanese-text density under several encodings.
Read-only. Reports files whose bytes decode to a high ratio of Japanese chars,
which flags script/message archives vs. graphics/binary blobs."""
import struct, sys, os

def u32(b, o): return struct.unpack_from("<I", b, o)[0]

def read_fat(d, off, size):
    return [(u32(d, off+i*8), u32(d, off+i*8+4)) for i in range(size//8)]

def read_fnt(d, fnt_off):
    names = {}
    def walk(dir_id, prefix):
        idx = dir_id & 0x0FFF
        sub_off = u32(d, fnt_off + idx*8)
        first_file = struct.unpack_from("<H", d, fnt_off+idx*8+4)[0]
        p = fnt_off + sub_off; fid = first_file
        while True:
            t = d[p]; p += 1
            if t == 0: break
            length = t & 0x7F; is_dir = (t & 0x80) != 0
            nm = d[p:p+length].decode("ascii","replace"); p += length
            if is_dir:
                sub = struct.unpack_from("<H", d, p)[0]; p += 2
                walk(sub, prefix+"/"+nm)
            else:
                names[fid] = prefix+"/"+nm; fid += 1
    walk(0xF000, "")
    return names

def jp_ratio_sjis(b):
    """fraction of bytes that form valid Shift-JIS double-byte kana/kanji"""
    n = len(b); i = 0; jp = 0; total_chars = 0
    while i < n:
        c = b[i]
        if (0x81 <= c <= 0x9F) or (0xE0 <= c <= 0xFC):
            if i+1 < n:
                c2 = b[i+1]
                if (0x40 <= c2 <= 0x7E) or (0x80 <= c2 <= 0xFC):
                    jp += 1; total_chars += 1; i += 2; continue
            i += 1; total_chars += 1
        else:
            i += 1; total_chars += 1
    return (jp*2)/n if n else 0, jp

def jp_ratio_utf16(b):
    """fraction of code units in Hiragana/Katakana/CJK ranges under UTF-16LE"""
    n = len(b)//2; jp = 0
    for i in range(n):
        cp = b[i*2] | (b[i*2+1]<<8)
        if (0x3040<=cp<=0x30FF) or (0x4E00<=cp<=0x9FFF) or (0xFF00<=cp<=0xFFEF):
            jp += 1
    return jp/n if n else 0, jp

def main():
    rom = sys.argv[1]
    d = open(rom,"rb").read()
    fnt_off=u32(d,0x40); fat_off=u32(d,0x48); fat_size=u32(d,0x4C)
    fat=read_fat(d,fat_off,fat_size); names=read_fnt(d,fnt_off)
    results=[]
    for fid,path in names.items():
        if fid>=len(fat): continue
        s,e=fat[fid]; b=d[s:e]
        if len(b)<32: continue
        sr,sjp=jp_ratio_sjis(b)
        ur,ujp=jp_ratio_utf16(b)
        results.append((path,len(b),sr,sjp,ur,ujp,s,e))
    print("=== TOP Shift-JIS density files (ratio, #jp-pairs) ===")
    for r in sorted(results,key=lambda x:-x[2])[:25]:
        print(f"  sjis={r[2]:.2f} pairs={r[3]:6}  size={r[1]:8}  {r[0]}")
    print("\n=== TOP UTF-16LE density files (ratio, #jp-units) ===")
    for r in sorted(results,key=lambda x:-x[4])[:25]:
        print(f"  u16={r[4]:.2f} units={r[5]:6}  size={r[1]:8}  {r[0]}")
    print("\n=== files whose NAME suggests text ===")
    kw=("msg","mes","text","txt","str","script","scr","word","name","dic","talk","serif","story","event","help","tuto","menu","lang")
    for r in sorted(results,key=lambda x:-x[1]):
        low=r[0].lower()
        if any(k in low for k in kw):
            print(f"  size={r[1]:8} sjis={r[2]:.2f} u16={r[4]:.2f}  {r[0]}")

if __name__=="__main__":
    main()
