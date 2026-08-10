import sys, subprocess, os, shutil, time
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
shutil.rmtree("/root/.local/share/emucap/desmume-nds", ignore_errors=True)
LOG=open("/root/probe.log","w",encoding="utf-8")
def log(*a): print(*a, file=LOG, flush=True)
try:
    from emucap_drv import Emucap, ROM
    e=Emucap()
    e.call("bootstrap",{},30)
    if not (e.call("status",{},30)["json"] or {}).get("connected"):
        e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},180)
    e.call("load_state",{"path":"/root/ppkp9_kbd.dss"},30)
    e.call("resume",{},30); time.sleep(0.4); e.call("pause",{},30)
    e.screenshot("/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/kbd_now.png")
    DMASET=0x01FF8098
    e.call("set_breakpoint",{"kind":"exec","memory_type":"arm9","start":hex(DMASET),"end":hex(DMASET),"pause_on_hit":True},20)
    def regs():
        st=(e.call("get_state",{},20)["json"] or {}).get("state",{})
        return {k:st.get("cpu."+k) for k in ("r0","r1","r2","r3","pc","lr","sp")}
    def frozen():
        s=e.call("status",{},20)["json"] or {}
        return s.get("state")=="frozen" or (s.get("cpus",{}) or {}).get("arm9")=="frozen"
    def inrange(v): return isinstance(v,int) and 0x06000000<=v<0x07000000
    alld=[]; got=[]
    # type a key: tap first hiragana 'あ' cell approx (from name_05: grid starts ~x18,y196)
    e.call("touch",{"x":22,"y":210,"frames":6},20)
    e.call("resume",{},20); dl=time.time()+15
    while time.time()<dl:
        time.sleep(0.02)
        if frozen():
            r=regs(); alld.append(r)
            if any(inrange(r[k]) for k in ("r0","r1","r2")):
                cs=e.call("call_stack",{},20)["text"][:500]
                got.append((r,cs))
                log(f"VRAM DMA: r0={r['r0']:#x} r1={r['r1']:#x} r2={r['r2']:#x} r3={r['r3']} lr={r['lr']:#x}")
                log("  stack:", cs.replace(chr(10)," | "))
            e.call("resume",{},20)
    log(f"total DMA hits during type: {len(alld)}; VRAM-touching: {len(got)}")
    # show a sample of dst values to understand landscape
    import collections
    dsts=collections.Counter()
    for r in alld:
        d=r['r1']; dsts[(d>>24)&0xff if isinstance(d,int) else -1]+=1
    log("r1 high-byte histogram:", dict(dsts))
    e.close(); log("DONE")
except Exception:
    import traceback; log("ERR", traceback.format_exc())
finally:
    LOG.close()
    subprocess.run(["pkill","-9","-f","[d]esmume-cli"])
    subprocess.run(["pkill","-9","-f","[e]mucap-desmume-nds-bridge"])
    os._exit(0)
