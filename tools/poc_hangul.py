#!/usr/bin/env python3
"""Hangul visibility PoC: write a Hangul glyph pattern into the live source buffer
region and screenshot to show Hangul rendering through the game's pipeline."""
import sys, time
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR
KBD="/root/ppkp9_kbd.dss"

# 8x8 Hangul '가' (1=ink). ㄱ on left, ㅏ on right.
GA = [
 "01110100",
 "00010100",
 "00010110",
 "00100100",
 "00100100",
 "01000100",
 "01000100",
 "00000100",
]
def tile4bpp(rows, ink=0xF):
    out=bytearray()
    for r in rows:
        for bx in range(4):
            p0=ink if r[bx*2]=="1" else 0
            p1=ink if r[bx*2+1]=="1" else 0
            out.append(p0 | (p1<<4))
    return bytes(out)   # 32 bytes

TILE=tile4bpp(GA)

def wr(e, off, data):
    e.call("write_memory",{"memory_type":"main","address":hex(off),"hex":data.hex()},60)

e=Emucap()
e.call("bootstrap",{},30)
if not (e.call("status",{},30)["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)
e.call("load_state",{"path":KBD},30)
e.call("resume",{},30); time.sleep(0.3); e.call("pause",{},30)
e.screenshot(f"{OUTDIR}/hangul_base.png")

# write the Hangul tile repeatedly across candidate font ranges
for tag,start,end in [("R1",0x2D1000,0x2D3000),("R2",0x2CF000,0x2D1000),("R3",0x2D3000,0x2D6000)]:
    e.call("load_state",{"path":KBD},30)
    e.call("resume",{},30); time.sleep(0.3); e.call("pause",{},30)
    block=TILE*64   # 2KB of repeated glyph
    off=start
    while off<end:
        wr(e, off, block); off+=len(block)
    e.call("resume",{},30); time.sleep(0.25); e.call("pause",{},30)
    e.screenshot(f"{OUTDIR}/hangul_{tag}.png")
    print(f"{tag}: wrote 가-tiles @main+{hex(start)}..{hex(end)}")
e.close(); print("DONE")
