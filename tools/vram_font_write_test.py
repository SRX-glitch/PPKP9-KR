#!/usr/bin/env python3
"""Re-test whether writing the font char-data in VRAM (0x06208000, SUB BG0 char
base) changes the on-screen keyboard. If it sticks, live Hangul PoC is possible."""
import sys, time
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR
KBD="/root/ppkp9_kbd.dss"

def wr(e,addr,data): e.call("write_memory",{"memory_type":"arm9","address":hex(addr),"hex":data.hex()},60)

e=Emucap()
e.call("bootstrap",{},30)
if not (e.call("status",{},30)["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)
e.call("load_state",{"path":KBD},30)
e.call("resume",{},30); time.sleep(0.4); e.call("pause",{},30)
e.screenshot(f"{OUTDIR}/vfw_base.png")

# overwrite a chunk of the font char data with solid 0xFF and screenshot
for tag,addr,ln,wait in [("A",0x06208000,0x1000,0.05),("B",0x06208000,0x1000,0.3),
                          ("C",0x06209000,0x1000,0.3)]:
    e.call("load_state",{"path":KBD},30)
    e.call("resume",{},30); time.sleep(0.3); e.call("pause",{},30)
    wr(e,addr,b"\xFF"*ln)
    # screenshot BOTH without resume (just render current) and after a tiny resume
    e.call("resume",{},30); time.sleep(wait); e.call("pause",{},30)
    n=e.screenshot(f"{OUTDIR}/vfw_{tag}.png")
    print(f"{tag}: wrote 0xFF x{ln} @{hex(addr)} wait={wait} -> vfw_{tag}.png")
e.close(); print("DONE")
