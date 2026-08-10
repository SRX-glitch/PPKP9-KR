#!/usr/bin/env python3
import sys, time, os
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR
STORY="/root/ppkp9_story.dss"; KBD="/root/ppkp9_kbd.dss"; OUT2="/root/ppkp9_story2.dss"
e=Emucap()
e.call("bootstrap",{},30)
if not (e.call("status",{},30)["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)
st = STORY if os.path.exists(STORY) else KBD
e.call("load_state",{"path":st},30)
e.call("resume",{},30); time.sleep(0.4); e.call("pause",{},30)
def tap(i,x,y,wait=1.4):
    e.call("touch",{"x":x,"y":y,"frames":8},30)
    e.call("resume",{},30); time.sleep(wait); e.call("pause",{},30)
    e.screenshot(f"{OUTDIR}/cn_{i:02d}.png"); print(f"cn_{i:02d} {x},{y}")
tap(0,28,76)     # OK (confirm name)
for i in range(1,12): tap(i,128,150,1.5)   # advance through opening dialogue
try: print("save story2:", e.call("save_state",{"path":OUT2},30)["text"][:60])
except Exception as ex: print("save fail",ex)
e.close(); print("DONE")
