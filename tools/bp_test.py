#!/usr/bin/env python3
"""Decisively test whether exec breakpoints actually fire: read the live PC at the
keyboard screen, set an exec BP there, resume, and check if it re-hits."""
import sys, time
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM
KBD="/root/ppkp9_kbd.dss"

e=Emucap()
e.call("bootstrap",{},30)
if not (e.call("status",{},30)["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)
e.call("load_state",{"path":KBD},30)

def pc():
    j=e.call("get_state",{},20)["json"] or {}; s=j.get("state",j)
    return s.get("cpu.pc")

# sample a few PCs while running
pcs=[]
for _ in range(5):
    e.call("resume",{},20); time.sleep(0.15); e.call("pause",{},20)
    p=pc(); pcs.append(p)
print("sampled PCs while running:", [hex(x) if isinstance(x,int) else x for x in pcs])

# pick a PC in main RAM code region (0x0200xxxx-0x021Fxxxx)
target=None
for p in pcs:
    if isinstance(p,int) and 0x02000000<=(p&~1)<0x02400000:
        target=p&~1; break
if target is None: target=(pcs[0]&~1) if isinstance(pcs[0],int) else 0x2000000
print("setting exec BP at", hex(target))
r=e.call("set_breakpoint",{"kind":"exec","memory_type":"arm9","start":hex(target),"end":hex(target),"pause_on_hit":True},20)
print("set_breakpoint reply:", r["text"][:150])
print("list:", e.call("list_breakpoints",{},20)["text"][:200])

# resume and see if it freezes on the BP
e.call("resume",{},20)
hit=False
for i in range(20):
    time.sleep(0.1)
    st=e.call("status",{},20)["json"] or {}
    if st.get("state")=="frozen" or (st.get("cpus",{}) or {}).get("arm9")=="frozen":
        hit=True
        print(f"FROZEN after {i} polls -> exec BP FIRED. pc now={hex(pc()) if isinstance(pc(),int) else pc()}")
        print("poll_events:", e.call("poll_events",{},20)["text"][:200])
        break
if not hit:
    print("NOT frozen after 2s -> exec BP did NOT fire (breakpoints non-functional here)")
    st=e.call("status",{},20)["json"] or {}
    print("state:", st.get("state"), st.get("cpus"))
e.close(); print("DONE")
