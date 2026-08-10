#!/usr/bin/env python3
"""Test whether the main-RAM 4bpp buffer near 0x2D1740 is a live VRAM source:
overwrite a slice and see if the keyboard changes. If yes -> place Hangul."""
import sys, time
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR
KBD="/root/ppkp9_kbd.dss"

def wr(e, off, data):
    e.call("write_memory",{"memory_type":"main","address":hex(off),"hex":data.hex()},60)

e=Emucap()
e.call("bootstrap",{},30)
if not (e.call("status",{},30)["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)

# test several slices around the 4bpp match to find a live source buffer
tests=[("A",0x2D0000,0x4000),("B",0x2D1000,0x2000),("C",0x2CE000,0x8000)]
for tag,off,ln in tests:
    e.call("load_state",{"path":KBD},30)
    e.call("resume",{},30); time.sleep(0.3); e.call("pause",{},30)
    if tag=="A": e.screenshot(f"{OUTDIR}/poc2_base.png")
    wr(e, off, b"\xFF"*ln)
    e.call("resume",{},30); time.sleep(0.25); e.call("pause",{},30)
    e.screenshot(f"{OUTDIR}/poc2_{tag}.png")
    print(f"{tag}: 0xFF x{ln} @main+{hex(off)} -> poc2_{tag}.png")
e.close(); print("DONE")
