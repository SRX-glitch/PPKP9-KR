#!/usr/bin/env python3
"""Fresh launch, set decompression breakpoints while halted, then boot + navigate
to the charamake keyboard, catching EVERY decompression (codec/src/dst/size).
The font's decompression is in this log."""
import sys, time
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR

WRAP={0x2000306:"LZ77Vram",0x20006ac:"BitUnPack",0x20003b4:"HuffUnComp",
      0x20001dc:"RLVram",0x2042294:"RLVram2",0x2000786:"LZ77Wram",0x2000416:"RLWram"}

e=Emucap()
e.call("bootstrap",{},30)
print("launch:", e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)["text"][:50])
# stub starts halted; set BPs now (before boot)
st=e.call("status",{},20)["json"] or {}
print("initial state:", st.get("state"))
for a in WRAP: e.call("set_breakpoint",{"kind":"exec","memory_type":"arm9","start":hex(a),"end":hex(a),"pause_on_hit":True},20)
print("breakpoints set:", e.call("list_breakpoints",{},20)["text"][:120])

hits=[]; seen=set()
def regs():
    j=e.call("get_state",{},20)["json"] or {}; s=j.get("state",j)
    return {k:s.get("cpu."+k) for k in ("r0","r1","r2","r3","pc")}
def frozen(st): return st.get("state")=="frozen" or (st.get("cpus",{}) or {}).get("arm9")=="frozen"

def run(wait, inject=None):
    if inject: inject()
    e.call("resume",{},20)
    deadline=time.time()+wait
    while time.time()<deadline:
        time.sleep(0.06)
        st=e.call("status",{},20)["json"] or {}
        if frozen(st):
            r=regs(); pc=r.get("pc"); pcv=(pc&~1) if isinstance(pc,int) else None
            name=WRAP.get(pcv,f"?{hex(pcv) if isinstance(pcv,int) else pcv}")
            key=(name,r.get("r0"),r.get("r1"))
            if key not in seen:
                seen.add(key); hits.append((name,r.get("r0"),r.get("r1"),r.get("r2")))
                hx=lambda v: hex(v) if isinstance(v,int) else v
                print(f"HIT {name} src={hx(r.get('r0'))} dst={hx(r.get('r1'))} size={hx(r.get('r2'))}")
            e.call("resume",{},20)
            if len(hits)>250: break
    e.call("pause",{},20)

def tap(x,y,w=1.6): run(w, lambda: e.call("touch",{"x":x,"y":y,"frames":8},20))
def btn(b,w=1.6): run(w, lambda: e.call("press_buttons",{"buttons":[b],"frames":8},20))

# boot
for i in range(7):
    run(1.3, (lambda: e.call("press_buttons",{"buttons":["start"],"frames":4},20)) if i%2==0 else None)
tap(128,96,2.0); tap(128,96,1.5)
tap(60,30,1.5); tap(60,30,1.5)
tap(128,150,1.5); tap(128,150,1.5)
tap(55,98,2.0); tap(55,98,2.0)
btn("a"); tap(128,110); btn("a"); tap(190,160,2.0); btn("a",2.5)
run(2.5)
e.screenshot(f"{OUTDIR}/boot_cap_state.png")
print(f"\n=== {len(hits)} unique decompressions ===")
for name,r0,r1,r2 in hits:
    hx=lambda v: hex(v) if isinstance(v,int) else v
    print(f"  {name:12} src={hx(r0):>11} dst={hx(r1):>11} size={hx(r2)}")
e.close(); print("DONE")
