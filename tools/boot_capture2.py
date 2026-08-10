#!/usr/bin/env python3
"""Set exec BPs on ALL decompression SWI sites (ARM9 + overlays), boot + navigate
to charamake, and log every decompression (codec/src/dst/size). The charamake font
decomp lives in an overlay's SWI site."""
import sys, time
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR

# swi sites from swi_scan.py (addr -> codec)
SITES={
 0x20006ac:"BitUnPack",0x2000786:"LZ77Wram",0x2000306:"LZ77Vram",0x20003b4:"HuffUnComp",
 0x2000416:"RLWram",0x20001dc:"RLVram",0x2042294:"RLVram",
 0x20ca5a0:"RLWram",0x20ca830:"RLWram",0x20cacd4:"RLWram",0x20cb2b0:"RLWram",0x20cb734:"RLWram",
 0x20f5de8:"BitUnPack",0x20e7a7c:"HuffUnComp",0x21753dc:"BitUnPack",0x2177800:"RLWram",
 0x2170d5c:"RLWram",0x21ba514:"Diff8",0x219cb64:"LZ77Wram",0x219cc4c:"LZ77Wram",
 0x219d244:"LZ77Wram",0x219d35c:"LZ77Wram",0x2218f44:"BitUnPack",
}

e=Emucap()
e.call("bootstrap",{},30)
e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)
for a in SITES: e.call("set_breakpoint",{"kind":"exec","memory_type":"arm9","start":hex(a),"end":hex(a),"pause_on_hit":True},20)
print(f"{len(SITES)} breakpoints set")

hits=[]; seen=set()
def regs():
    j=e.call("get_state",{},20)["json"] or {}; s=j.get("state",j)
    return {k:s.get("cpu."+k) for k in ("r0","r1","r2","pc")}
def frozen(st): return st.get("state")=="frozen" or (st.get("cpus",{}) or {}).get("arm9")=="frozen"
def run(wait, inject=None):
    if inject: inject()
    e.call("resume",{},20)
    dl=time.time()+wait
    while time.time()<dl:
        time.sleep(0.05)
        st=e.call("status",{},20)["json"] or {}
        if frozen(st):
            r=regs(); pc=r.get("pc"); pcv=(pc&~1) if isinstance(pc,int) else None
            name=SITES.get(pcv,f"?{hex(pcv) if isinstance(pcv,int) else pcv}")
            key=(pcv,r.get("r0"),r.get("r1"))
            if key not in seen:
                seen.add(key); hits.append((name,r.get("r0"),r.get("r1"),r.get("r2")))
                hx=lambda v: hex(v) if isinstance(v,int) else v
                print(f"HIT {name} pc={hx(pcv)} src={hx(r.get('r0'))} dst={hx(r.get('r1'))} size={hx(r.get('r2'))}")
            e.call("resume",{},20)
            if len(hits)>300: break
    e.call("pause",{},20)
def tap(x,y,w=1.5): run(w, lambda: e.call("touch",{"x":x,"y":y,"frames":8},20))
def btn(b,w=1.5): run(w, lambda: e.call("press_buttons",{"buttons":[b],"frames":8},20))

for i in range(7): run(1.3,(lambda: e.call("press_buttons",{"buttons":["start"],"frames":4},20)) if i%2==0 else None)
tap(128,96,2.0); tap(128,96,1.5); tap(60,30,1.5); tap(60,30,1.5)
tap(128,150,1.5); tap(128,150,1.5); tap(55,98,2.0); tap(55,98,2.0)
btn("a"); tap(128,110); btn("a"); tap(190,160,2.0); btn("a",2.5); run(2.5)
print(f"\n=== {len(hits)} unique decompressions (VRAM/0x22d-region dst = font candidates) ===")
for name,r0,r1,r2 in hits:
    hx=lambda v: hex(v) if isinstance(v,int) else v
    tag=""
    if isinstance(r1,int) and (0x06000000<=r1<0x07000000): tag=" <== VRAM"
    print(f"  {name:12} src={hx(r0):>11} dst={hx(r1):>11} size={hx(r2)}{tag}")
e.close(); print("DONE")
