import sys, subprocess, os, shutil, time
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
    def rd(addr,n,mt="arm9"):
        j=e.call("read_memory",{"memory_type":mt,"address":hex(addr),"length":n},20)["json"]
        return bytes.fromhex(j["hex"]) if j and "hex" in j else b""
    e.call("resume",{},20); dl=time.time()+40; got=0
    while time.time()<dl and got<3:
        time.sleep(0.008)
        if frozen():
            r=regs(); dst=r.get("r2")
            if isinstance(dst,int) and 0x06200000<=dst<0x06220000:
                sp=r["sp"]; stk=rd(sp,0x300,"arm9")
                open(f"{SD}/stack_{got}.bin","wb").write(stk)
                log(f"call#{got}: src={r['r1']:#x} dst={dst:#x} r3={r['r3']} lr={r['lr']:#x} sp={sp:#x}")
                got+=1
            e.call("resume",{},20)
    log(f"captured {got} stacks")
    e.close(); log("DONE")
except Exception:
    import traceback; log("ERR", traceback.format_exc())
finally:
    LOG.close()
    subprocess.run(["pkill","-9","-f","[d]esmume-cli"])
    subprocess.run(["pkill","-9","-f","[e]mucap-desmume-nds-bridge"])
    os._exit(0)
