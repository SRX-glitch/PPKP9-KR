#!/usr/bin/env python3
"""Inject Hangul into the located 4bpp font buffer in main RAM (~0x2D3320, the
source for VRAM font 0x06208000) and screenshot: keyboard glyphs -> Hangul."""
import sys, time
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR
KBD="/root/ppkp9_kbd.dss"

# 8x8 Hangul '가' (bold). 1=ink -> 4bpp nibble 0xF
GA=["01110010","00010010","00010011","00100010","00100010","01000010","01000010","00000010"]
def tile8(rows,ink=0xF):
    out=bytearray()
    for r in rows:
        for bx in range(4):
            p0=ink if r[bx*2]=="1" else 0; p1=ink if r[bx*2+1]=="1" else 0
            out.append(p0|(p1<<4))
    return bytes(out)
TILE=tile8(GA)

def wr(e,off,data): e.call("write_memory",{"memory_type":"main","address":hex(off),"hex":data.hex()},60)

e=Emucap()
e.call("bootstrap",{},30)
if not (e.call("status",{},30)["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)

# Try the linear-mapped font block; VRAM 0x84E0 -> main 0x2D3800 => VRAM 0x8000 -> main 0x2D3320
for tag,start,end in [("F1",0x2D3320,0x2D5320),("F2",0x2D3000,0x2D4000),("F3",0x2D2000,0x2D6000)]:
    e.call("load_state",{"path":KBD},30)
    e.call("resume",{},30); time.sleep(0.3); e.call("pause",{},30)
    block=TILE*64
    off=start
    while off<end: wr(e,off,block); off+=len(block)
    e.call("resume",{},30); time.sleep(0.25); e.call("pause",{},30)
    e.screenshot(f"{OUTDIR}/pocfinal_{tag}.png")
    print(f"{tag}: 가 into main {hex(start)}..{hex(end)}")
e.close(); print("DONE")
