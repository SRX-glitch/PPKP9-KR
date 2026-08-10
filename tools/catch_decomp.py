#!/usr/bin/env python3
"""Set exec breakpoints on the BIOS decompression wrappers, then open the keyboard
screen and catch the font decompression: log r0(source)/r1(dest)/r2 at each hit.
The call whose dest is the SUB font VRAM (or a buffer feeding it) = the font."""
import sys, time, json
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR
DLG="/root/ppkp9_dlg.dss"

WRAPPERS={0x2000306:"LZ77UnCompVram",0x20006ac:"BitUnPack",0x20003b4:"HuffUnComp",
          0x20001dc:"RLUnCompVram",0x2042294:"RLUnCompVram2",0x2000786:"LZ77Wram",
          0x2000416:"RLUnCompWram",0x2000000:""}

def regs(e):
    r=e.call("get_state",{},20); j=r["json"]
    return j if j else {}

e=Emucap()
e.call("bootstrap",{},30)
if not (e.call("status",{},30)["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)
e.call("load_state",{"path":DLG},30)
e.call("resume",{},30); time.sleep(0.5); e.call("pause",{},30)

def tap(x,y,w=1.4): e.call("touch",{"x":x,"y":y,"frames":8},30); e.call("resume",{},30); time.sleep(w); e.call("pause",{},30)
def btn(b,w=1.4): e.call("press_buttons",{"buttons":[b],"frames":8},30); e.call("resume",{},30); time.sleep(w); e.call("pause",{},30)

# navigate to just before the keyboard opens (all but final A)
tap(55,98,2.0); tap(55,98,2.0); btn("a",1.5); tap(128,110,1.5); btn("a",1.5); tap(190,160,1.5)

# set exec breakpoints on decompression wrappers
for addr,name in WRAPPERS.items():
    if not name: continue
    e.call("set_breakpoint",{"kind":"exec","memory_type":"arm9","start":hex(addr),"end":hex(addr),"pause_on_hit":True},20)
print("breakpoints set")

# trigger keyboard: press A and resume in a loop, catching hits
e.call("press_buttons",{"buttons":["a"],"frames":8},30)
hits=[]
for step in range(120):
    e.call("resume",{},20)
    time.sleep(0.15)
    st=e.call("status",{},20)["json"] or {}
    state=st.get("state")
    if state=="frozen" or st.get("cpus",{}).get("arm9")=="frozen":
        ev=e.call("poll_events",{},20)["text"][:150]
        rg=regs(e)
        pc=rg.get("pc") or rg.get("r15")
        r0=rg.get("r0"); r1=rg.get("r1"); r2=rg.get("r2")
        name=WRAPPERS.get(pc & ~1 if isinstance(pc,int) else -1,"?")
        hits.append((pc,r0,r1,r2,name))
        print(f"HIT pc={hex(pc) if isinstance(pc,int) else pc} {name} r0={hex(r0) if isinstance(r0,int) else r0} r1={hex(r1) if isinstance(r1,int) else r1} r2={hex(r2) if isinstance(r2,int) else r2}")
    else:
        if step>3: break
e.screenshot(f"{OUTDIR}/catch_state.png")
print(f"\n{len(hits)} decompression hits")
for pc,r0,r1,r2,name in hits:
    print(f"  {name}: src={hex(r0) if isinstance(r0,int) else r0} dst={hex(r1) if isinstance(r1,int) else r1}")
e.close(); print("DONE")
