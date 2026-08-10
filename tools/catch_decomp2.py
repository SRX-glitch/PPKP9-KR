#!/usr/bin/env python3
"""Set decompression breakpoints from the scenario-select state, then navigate to
the keyboard while catching EVERY decompression hit. Log codec + r0(src)/r1(dst);
the hit whose dst is SUB font VRAM (0x0620xxxx) or its buffer = the font."""
import sys, time
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR
DLG="/root/ppkp9_dlg.dss"

WRAPPERS={0x2000306:"LZ77UnCompVram",0x20006ac:"BitUnPack",0x20003b4:"HuffUnComp",
          0x20001dc:"RLUnCompVram",0x2042294:"RLUnCompVram2",0x2000786:"LZ77Wram",
          0x2000416:"RLUnCompWram"}

e=Emucap()
e.call("bootstrap",{},30)
if not (e.call("status",{},30)["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)
e.call("load_state",{"path":DLG},30)
e.call("resume",{},30); time.sleep(0.4); e.call("pause",{},30)

# raw get_state once to learn field names
raw=e.call("get_state",{},20)["text"][:300]
print("get_state sample:", raw)

for addr,name in WRAPPERS.items():
    e.call("set_breakpoint",{"kind":"exec","memory_type":"arm9","start":hex(addr),"end":hex(addr),"pause_on_hit":True},20)
print("breakpoints set")

hits=[]
def regs():
    j=e.call("get_state",{},20)["json"] or {}
    st=j.get("state",j)
    def g(n):
        return st.get("cpu."+n, st.get(n))
    return {k:g(k) for k in ("r0","r1","r2","r3","pc","r15","lr","sp")}

def bp_frozen(st):
    return st.get("state")=="frozen" or (st.get("cpus",{}) or {}).get("arm9")=="frozen"

def step(input_fn, wait):
    if input_fn: input_fn()   # set input while paused
    e.call("resume",{},20)
    deadline=time.time()+wait
    while time.time()<deadline:
        time.sleep(0.08)
        st=e.call("status",{},20)["json"] or {}
        if bp_frozen(st):            # frozen w/o us pausing => real BP hit
            r=regs(); pc=r.get("pc") or r.get("r15")
            pcv=(pc & ~1) if isinstance(pc,int) else None
            name=WRAPPERS.get(pcv,"?")
            hits.append((pcv,r.get("r0"),r.get("r1"),r.get("r2"),name))
            hx=lambda v: hex(v) if isinstance(v,int) else v
            print(f"HIT {name} pc={hx(pcv)} src={hx(r.get('r0'))} dst={hx(r.get('r1'))} r2={hx(r.get('r2'))}")
            e.call("resume",{},20)   # continue past the BP
    e.call("pause",{},20)

def tap(x,y,w=1.6): step(lambda: e.call("touch",{"x":x,"y":y,"frames":8},20), w)
def btn(b,w=1.6): step(lambda: e.call("press_buttons",{"buttons":[b],"frames":8},20), w)

tap(55,98,2.0); tap(55,98,2.0); btn("a"); tap(128,110); btn("a"); tap(190,160,2.0); btn("a",2.5)
step(None,2.0)
e.screenshot(f"{OUTDIR}/catch2_state.png")

print(f"\n=== ALL {len(hits)} decompression hits (name src dst r2) ===")
hx=lambda v: hex(v) if isinstance(v,int) else str(v)
for pc,r0,r1,r2,name in hits:
    tag=""
    if isinstance(r1,int) and 0x06000000<=r1<0x07000000: tag=" <-- VRAM dst"
    print(f"  {name:16} src={hx(r0):>10} dst={hx(r1):>10} r2={hx(r2)}{tag}")
e.close(); print("DONE")
