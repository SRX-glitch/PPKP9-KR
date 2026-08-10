#!/usr/bin/env python3
"""Find the font SOURCE in main RAM by searching for known VRAM glyphs in several
plausible source formats (raw 4bpp, and 1bpp reductions), full 4MB scan."""
import sys, time
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR
KBD="/root/ppkp9_kbd.dss"

vram=open(f"{OUTDIR}/kbd_subBG.bin","rb").read()
# pick a few clean glyph tiles (4bpp 8x8 = 32 bytes)
glyphs=[]
for off in range(0x4000,0x14000,32):
    t=vram[off:off+32]
    ink=sum(bin(b).count("1") for b in t)/(256)
    if 0.15<ink<0.5: glyphs.append((off,t))
glyphs=glyphs[::max(1,len(glyphs)//4)][:4]

def to_1bpp_msb(t):
    # 4bpp tile (2px/byte) -> 1bpp (bit set if nibble!=0), MSB-first
    out=bytearray()
    px=[]
    for b in t: px.append(b&0xF); px.append((b>>4)&0xF)
    for row in range(8):
        byte=0
        for col in range(8):
            if px[row*8+col]!=0: byte|=(1<<(7-col))
        out.append(byte)
    return bytes(out)
def to_1bpp_lsb(t):
    px=[]
    for b in t: px.append(b&0xF); px.append((b>>4)&0xF)
    out=bytearray()
    for row in range(8):
        byte=0
        for col in range(8):
            if px[row*8+col]!=0: byte|=(1<<col)
        out.append(byte)
    return bytes(out)

def search(e, mt, hexpat):
    # full scan by iterating start windows
    start=0; total_scanned=0
    while start < 0x400000:
        r=e.call("find_pattern",{"memory_type":mt,"hex":hexpat,"start":start,"length":0x400000-start},40)
        j=r["json"]
        if not j: return None
        if j.get("count",0)>0 and j.get("matches"):
            return j["matches"]
        sc=j.get("scanned",0)
        if not j.get("truncated_scan"): break
        start = (j.get("start",start)+sc)
        total_scanned+=sc
        if sc==0: break
    return []

e=Emucap()
e.call("bootstrap",{},30)
if not (e.call("status",{},30)["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)
e.call("load_state",{"path":KBD},30)
e.call("resume",{},30); time.sleep(0.4); e.call("pause",{},30)

for off,t in glyphs:
    for tag,pat in [("4bpp",t),("1bpp_msb",to_1bpp_msb(t)),("1bpp_lsb",to_1bpp_lsb(t))]:
        m=search(e,"main",pat.hex())
        status = f"MATCH {m[:3]}" if m else "none"
        print(f"glyph@0x{off:X} {tag:9} -> {status}")
e.close(); print("DONE")
