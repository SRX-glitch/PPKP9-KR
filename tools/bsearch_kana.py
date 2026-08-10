#!/usr/bin/env python3
"""Binary-search which sub-slice of the source buffer holds the kana keyboard
glyphs: zero each 0x1000 slice, screenshot, see which removes the あいうえお grid."""
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
e.call("load_state",{"path":KBD},30)
e.call("resume",{},30); time.sleep(0.3); e.call("pause",{},30)
e.screenshot(f"{OUTDIR}/bs_base.png")

start=0x2CC000; end=0x2D8000; step=0x1000
i=0
for off in range(start,end,step):
    e.call("load_state",{"path":KBD},30)
    e.call("resume",{},30); time.sleep(0.25); e.call("pause",{},30)
    wr(e, off, b"\x00"*step)
    e.call("resume",{},30); time.sleep(0.22); e.call("pause",{},30)
    e.screenshot(f"{OUTDIR}/bs_{i:02d}_{off:X}.png")
    print(f"bs_{i:02d}: zeroed {hex(off)}..{hex(off+step)}")
    i+=1
e.close(); print("DONE")
