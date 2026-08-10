#!/usr/bin/env python3
"""From the kana keyboard, enter a name and confirm (命名), then advance to reach
the actual scenario dialogue. Save a dialogue state and screenshot each step."""
import sys, time, os
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR
KBD="/root/ppkp9_kbd.dss"; STORY="/root/ppkp9_story.dss"

e=Emucap()
e.call("bootstrap",{},30)
if not (e.call("status",{},30)["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)
e.call("load_state",{"path":KBD},30)
e.call("resume",{},30); time.sleep(0.4); e.call("pause",{},30)
e.screenshot(f"{OUTDIR}/name_00.png")

def tap(i,x,y,wait=1.2):
    e.call("touch",{"x":x,"y":y,"frames":8},30)
    e.call("resume",{},30); time.sleep(wait); e.call("pause",{},30)
    e.screenshot(f"{OUTDIR}/name_{i:02d}.png"); print(f"name_{i:02d} touch {x},{y}")

# enter a few kana (あ area repeatedly), then 命名, then advance
tap(1,30,128)     # tap a kana in grid
tap(2,52,128)     # another kana
tap(3,74,128)     # another
tap(4,55,76)      # 命名 (confirm name) button
tap(5,128,150)    # advance
tap(6,128,150)
tap(7,128,150)
tap(8,128,150)
tap(9,128,150,1.6)
tap(10,128,150,1.6)
try: print("save story state:", e.call("save_state",{"path":STORY},30)["text"][:60])
except Exception as ex: print("save fail",ex)
e.close(); print("DONE")
