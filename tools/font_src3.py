#!/usr/bin/env python3
"""Now that the keyboard font is confirmed at VRAM 0x06208000 (SUB BG0 char base),
take those exact glyph tiles and find their SOURCE in main RAM (full scan), then
inject a Hangul glyph at the source and screenshot."""
import sys, time
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR
KBD="/root/ppkp9_kbd.dss"

vram=open(f"{OUTDIR}/kbd_subBG.bin","rb").read()
# font char data at VRAM offset 0x8000..0xC000 ; pick clean glyph tiles
glyphs=[]
for off in range(0x8000,0xC000,32):
    t=vram[off:off+32]; ink=sum(bin(b).count("1") for b in t)/256
    if 0.15<ink<0.6: glyphs.append((off,t))
print("font glyph candidates:",len(glyphs))

def search_full(e,mt,hexpat):
    start=0
    while start<0x400000:
        j=e.call("find_pattern",{"memory_type":mt,"hex":hexpat,"start":start,"length":0x400000-start},40)["json"]
        if not j: return []
        if j.get("count",0)>0 and j.get("matches"): return j["matches"]
        if not j.get("truncated_scan"): break
        start=j.get("start",start)+j.get("scanned",0)
        if j.get("scanned",0)==0: break
    return []

e=Emucap()
e.call("bootstrap",{},30)
if not (e.call("status",{},30)["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)
e.call("load_state",{"path":KBD},30)
e.call("resume",{},30); time.sleep(0.4); e.call("pause",{},30)

src=None
sample=glyphs[::max(1,len(glyphs)//12)][:12]
for off,t in sample:
    m=search_full(e,"main",t.hex())
    if m:
        print(f"VRAM font 0x{off:X} -> main RAM {[hex(x) for x in m[:3]]}")
        if src is None and len(m)<=4: src=(off,t,m)
    else:
        print(f"VRAM font 0x{off:X} -> none")
print("chosen src:", None if not src else (hex(src[0]), [hex(x) for x in src[2][:3]]))
e.close(); print("DONE")
