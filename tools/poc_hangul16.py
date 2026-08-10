#!/usr/bin/env python3
"""Clean 16x16 Hangul PoC: write a legible '가' as 4-tile metatiles into the live
source buffer, trying tile arrangements, and screenshot each."""
import sys, time
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR
KBD="/root/ppkp9_kbd.dss"

GA16 = [
 "0000000000000000",
 "0000000000011000",
 "0011111111011000",
 "0000000011011000",
 "0000000011011000",
 "0000000011011000",
 "0000000011011000",
 "0000000011011110",
 "0000000011011110",
 "0000000011011000",
 "0000000000011000",
 "0000000000011000",
 "0000000000011000",
 "0000000000011000",
 "0000000000011000",
 "0000000000000000",
]
def tile(rows, r0, c0, ink=0xF):
    out=bytearray()
    for ry in range(8):
        row=rows[r0+ry]
        for bx in range(4):
            c=c0+bx*2
            p0=ink if row[c]=="1" else 0
            p1=ink if row[c+1]=="1" else 0
            out.append(p0 | (p1<<4))
    return bytes(out)
TL=tile(GA16,0,0); TR=tile(GA16,0,8); BL=tile(GA16,8,0); BR=tile(GA16,8,8)
arrangements={
 "TLTRBLBR": TL+TR+BL+BR,
 "TLBLTRBR": TL+BL+TR+BR,
}

def wr(e, off, data):
    e.call("write_memory",{"memory_type":"main","address":hex(off),"hex":data.hex()},60)

e=Emucap()
e.call("bootstrap",{},30)
if not (e.call("status",{},30)["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)

for tag,meta in arrangements.items():
    e.call("load_state",{"path":KBD},30)
    e.call("resume",{},30); time.sleep(0.3); e.call("pause",{},30)
    block=meta*16   # 16 glyphs = 2KB
    off=0x2D1000; end=0x2D4000
    while off<end:
        wr(e, off, block); off+=len(block)
    e.call("resume",{},30); time.sleep(0.25); e.call("pause",{},30)
    e.screenshot(f"{OUTDIR}/hangul16_{tag}.png")
    print(f"{tag}: wrote 16x16 가 metatiles")
e.close(); print("DONE")
