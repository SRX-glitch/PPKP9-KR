#!/usr/bin/env python3
"""Fast interactive navigation using save-states. First run boots to the menu and
saves a state; subsequent runs load it and apply an action list, screenshotting.
Usage: nav.py <tag> <actions-json>
  actions: [{"touch":[x,y]} | {"btn":"a"} | {"wait":1.5}] applied in order."""
import sys, time, json, os
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR

MENU_STATE="/root/ppkp9_menu.dss"
tag=sys.argv[1] if len(sys.argv)>1 else "nav"
actions=json.loads(sys.argv[2]) if len(sys.argv)>2 else []

e=Emucap()
e.call("bootstrap",{},30)
if not (e.call("status",{},30)["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)

if os.path.exists(MENU_STATE):
    print("load menu state:", e.call("load_state",{"path":MENU_STATE},30)["text"][:100])
    e.call("resume",{},30); time.sleep(0.4); e.call("pause",{},30)
else:
    print("booting to menu...")
    for i in range(8):
        e.call("resume",{},30); time.sleep(1.3); e.call("pause",{},30)
        if i%2==0: e.call("press_buttons",{"buttons":["start"],"frames":4},30)
    print("save menu state:", e.call("save_state",{"path":MENU_STATE},30)["text"][:100])

e.screenshot(f"{OUTDIR}/{tag}_00.png")
i=1
for act in actions:
    if "touch" in act:
        x,y=act["touch"]; e.call("touch",{"x":x,"y":y,"frames":6},30)
    elif "btn" in act:
        e.call("press_buttons",{"buttons":[act["btn"]],"frames":6},30)
    w=act.get("wait",1.2)
    e.call("resume",{},30); time.sleep(w); e.call("pause",{},30)
    e.screenshot(f"{OUTDIR}/{tag}_{i:02d}.png")
    print(f"{tag}_{i:02d}.png after {act}")
    i+=1
e.close()
print("DONE")
