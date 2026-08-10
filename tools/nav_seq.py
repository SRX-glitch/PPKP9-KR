#!/usr/bin/env python3
"""Load the saved title state and run a hardcoded touch/button sequence,
screenshotting each step. Edit STEPS to explore. No shell-quoting needed."""
import sys, time, os
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR

MENU_STATE="/root/ppkp9_menu.dss"
TAG=sys.argv[1] if len(sys.argv)>1 else "seq"

# Each step: ("touch",x,y,wait) or ("btn",name,wait) or ("wait",secs)
STEPS=[
    ("touch",128,96,2.0),   # pass title -> mode menu
    ("touch",128,96,1.5),   # settle
    ("touch",60,30,1.5),    # tap top-left button (サクセス) on bottom screen
    ("touch",60,30,1.5),
    ("touch",128,150,1.5),  # confirm/advance
    ("touch",128,150,1.5),  # -> scenario select
    ("touch",50,88,2.0),    # select みすいのアイスガイ scenario box
    ("touch",50,88,2.0),    # confirm
    ("touch",128,150,2.0),  # advance opening
    ("touch",128,150,2.0),  # dialogue
    ("touch",128,150,1.5),
    ("touch",128,150,1.5),
    ("touch",128,150,1.5),
    ("touch",128,150,1.5),
]
SAVE_AT_END="/root/ppkp9_dlg.dss"

e=Emucap()
e.call("bootstrap",{},30)
if not (e.call("status",{},30)["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)
if os.path.exists(MENU_STATE):
    e.call("load_state",{"path":MENU_STATE},30)
    e.call("resume",{},30); time.sleep(0.4); e.call("pause",{},30)
e.screenshot(f"{OUTDIR}/{TAG}_00.png"); print(f"{TAG}_00 (title)")
for i,step in enumerate(STEPS,1):
    if step[0]=="touch":
        e.call("touch",{"x":step[1],"y":step[2],"frames":6},30); w=step[3]
    elif step[0]=="btn":
        e.call("press_buttons",{"buttons":[step[1]],"frames":6},30); w=step[2]
    else:
        w=step[1]
    e.call("resume",{},30); time.sleep(w); e.call("pause",{},30)
    e.screenshot(f"{OUTDIR}/{TAG}_{i:02d}.png")
    print(f"{TAG}_{i:02d} after {step}")
try:
    print("save dialogue state:", e.call("save_state",{"path":SAVE_AT_END},30)["text"][:80])
except Exception as ex: print("save failed", ex)
e.close(); print("DONE")
