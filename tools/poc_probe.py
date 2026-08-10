#!/usr/bin/env python3
"""Empirically locate the keyboard font tiles in VRAM: overwrite candidate
regions with a solid pattern, screenshot, see which makes the on-screen kana
change. Establishes the font's live VRAM address for the Hangul PoC."""
import sys, time, os
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR
KBD="/root/ppkp9_kbd.dss"

def wr(e, addr, data):
    # write_memory hex; chunk to be safe
    h=data.hex()
    e.call("write_memory",{"memory_type":"arm9","address":hex(addr),"hex":h},60)

e=Emucap()
e.call("bootstrap",{},30)
if not (e.call("status",{},30)["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)
e.call("load_state",{"path":KBD},30)
e.call("resume",{},30); time.sleep(0.5); e.call("pause",{},30)
e.screenshot(f"{OUTDIR}/poc_base.png"); print("base shot")

# candidate font regions to test (subBG then mainBG bands seen in dumps)
cands=[("subBG_8000",0x06208000,0x2000),
       ("subBG_A000",0x0620A000,0x2000),
       ("mainBG_18000",0x06018000,0x2000)]
for tag,addr,ln in cands:
    e.call("load_state",{"path":KBD},30)
    e.call("resume",{},30); time.sleep(0.3); e.call("pause",{},30)
    wr(e, addr, b"\xFF"*ln)         # solid fill
    e.call("resume",{},30); time.sleep(0.25); e.call("pause",{},30)
    n=e.screenshot(f"{OUTDIR}/poc_{tag}.png")
    print(f"{tag}: wrote 0xFF x{ln} @{hex(addr)} -> poc_{tag}.png {n}B")
e.close(); print("DONE")
