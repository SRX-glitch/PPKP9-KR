import sys, subprocess, os, shutil, time, struct
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
shutil.rmtree("/root/.local/share/emucap/desmume-nds", ignore_errors=True)
SD="/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey"
ROM="/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
LOG=open("/root/probe.log","w",encoding="utf-8")
def log(*a): print(*a, file=LOG, flush=True)
try:
    from emucap_drv import Emucap
    e=Emucap()
    e.call("bootstrap",{},30)
    if not (e.call("status",{},30)["json"] or {}).get("connected"):
        e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},180)
    e.call("reset",{},30)
    WRAP=0x0200F390
    e.call("set_breakpoint",{"kind":"exec","memory_type":"arm9","start":hex(WRAP),"end":hex(WRAP),"pause_on_hit":True},20)
    def regs():
        st=(e.call("get_state",{},20)["json"] or {}).get("state",{})
        return {k:st.get("cpu."+k) for k in ("r0","r1","r2","r3","lr","sp","pc")}
    def frozen():
        s=e.call("status",{},20)["json"] or {}
        return s.get("state")=="frozen" or (s.get("cpus",{}) or {}).get("arm9")=="frozen"
    import collections
    callers=collections.Counter(); samples={}
    e.call("resume",{},20); dl=time.time()+40; n=0
    while time.time()<dl and n<400:
        time.sleep(0.008)
        if frozen():
            n+=1; r=regs(); dst=r.get("r2"); lr=r.get("lr")
            if isinstance(dst,int) and 0x06000000<=dst<0x07000000 and isinstance(lr,int):
                callers[lr]+=1
                if lr not in samples: samples[lr]=(r["r0"],r["r1"],r["r2"],r["r3"])
            e.call("resume",{},20)
    log(f"scanned {n} copy32 calls")
    log("caller lr histogram (real return addrs):")
    for lr,c in callers.most_common(20):
        s=samples[lr]
        log(f"  lr={lr:#010x} x{c}  src={s[0]:#x} dst={s[1]:#x} r2={s[2]:#x} r3={s[3]}")
    e.close(); log("DONE")
except Exception:
    import traceback; log("ERR", traceback.format_exc())
finally:
    LOG.close()
    subprocess.run(["pkill","-9","-f","[d]esmume-cli"])
    subprocess.run(["pkill","-9","-f","[e]mucap-desmume-nds-bridge"])
    os._exit(0)
