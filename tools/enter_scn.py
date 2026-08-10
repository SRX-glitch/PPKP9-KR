#!/usr/bin/env python3
"""Load the saved scenario-select state and probe entry into 放浪のナイスガイ,
screenshotting after each distinct interaction so we can see the transition."""
import sys, time, os
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR

DLG="/root/ppkp9_dlg.dss"; MENU="/root/ppkp9_menu.dss"
TAG="scn"

e=Emucap()
e.call("bootstrap",{},30)
if not (e.call("status",{},30)["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)
state = DLG if os.path.exists(DLG) else MENU
print("loading", state, ":", e.call("load_state",{"path":state},30)["text"][:60])
e.call("resume",{},30); time.sleep(0.6); e.call("pause",{},30)
e.screenshot(f"{OUTDIR}/{TAG}_00.png"); print("00 base")

def act(i, kind, *a, wait=1.6):
    if kind=="touch": e.call("touch",{"x":a[0],"y":a[1],"frames":8},30)
    elif kind=="btn": e.call("press_buttons",{"buttons":[a[0]],"frames":8},30)
    e.call("resume",{},30); time.sleep(wait); e.call("pause",{},30)
    e.screenshot(f"{OUTDIR}/{TAG}_{i:02d}.png"); print(f"{i:02d} {kind} {a}")

# probe scenario entry: tap the scenario box, then likely confirm spots + A
act(1,"touch",55,98)     # scenario box
act(2,"touch",55,98)     # again (confirm?)
act(3,"btn","a")         # A to confirm
act(4,"touch",128,110)   # center (yes button?)
act(5,"btn","a")
act(6,"touch",190,160)   # bottom-right OK
act(7,"btn","a")
e.close(); print("DONE")
