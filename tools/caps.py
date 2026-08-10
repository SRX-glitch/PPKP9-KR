#!/usr/bin/env python3
import sys, time, json
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM
e=Emucap()
e.call("bootstrap",{},30)
if not (e.call("status",{},30)["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)
st=e.call("status",{},30)["json"] or {}
print("methods:", json.dumps(st.get("methods"), ensure_ascii=False))
print("memory_types:", st.get("memory_types"))
print("capability_notes:", json.dumps(st.get("capability_notes"), ensure_ascii=False)[:1500])
print("input_buttons:", st.get("input_buttons"))
# test a write watchpoint support probe: try set_breakpoint write on main
r=e.call("set_breakpoint",{"kind":"write","memory_type":"main","start":"0x1000","end":"0x1004","pause_on_hit":True},20)
print("write BP test:", r["text"][:200])
r=e.call("set_breakpoint",{"kind":"read","memory_type":"arm9","start":"0x02000000","end":"0x02000004","pause_on_hit":True},20)
print("read BP test:", r["text"][:200])
e.close()
