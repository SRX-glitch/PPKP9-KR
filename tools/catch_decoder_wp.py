import sys, subprocess, os, shutil, time
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
shutil.rmtree("/root/.local/share/emucap/desmume-nds", ignore_errors=True)
ROM="/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
LOG=open("/root/probe.log","w",encoding="utf-8")
def log(*a): print(*a, file=LOG, flush=True)
try:
    from emucap_drv import Emucap
    e=Emucap()
    e.call("bootstrap",{},30)
    if not (e.call("status",{},30)["json"] or {}).get("connected"):
        e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},180)
    e.call("load_state",{"path":"/root/ppkp9_kbd.dss"},30)
    e.call("resume",{},30); time.sleep(0.3); e.call("pause",{},30)
    # set WRITE watchpoint on font buffer
    r=e.call("set_breakpoint",{"kind":"write","memory_type":"main","start":hex(0x2D3740),"end":hex(0x2D3744),"pause_on_hit":True},20)
    log("set write-wp:", r["text"][:200])
    def regs():
        st=(e.call("get_state",{},20)["json"] or {}).get("state",{})
        return {k:st.get("cpu."+k) for k in ("r0","r1","r2","r3","r4","r5","r6","r7","r8","r9","r10","r11","r12","pc","lr","sp")}
    def frozen():
        s=e.call("status",{},20)["json"] or {}
        return s.get("state")=="frozen" or (s.get("cpus",{}) or {}).get("arm9")=="frozen"
    e.call("resume",{},20); dl=time.time()+15; hit=None
    while time.time()<dl:
        time.sleep(0.02)
        if frozen():
            hit=regs(); break
    if hit:
        pc=hit["pc"]
        log("WATCHPOINT HIT! pc=%#x"%pc)
        log("regs: "+" ".join("%s=%#x"%(k,hit[k]) for k in ("r0","r1","r2","r3","r4","r5","r6","r7","r8","r9","r10","r11","r12","lr","sp")))
        # disassemble around pc
        d=e.call("disassemble",{"address":hex(pc-0x18),"count":16},20)
        log("disasm:\n"+d["text"][:800])
    else:
        log("no watchpoint hit in 15s")
    e.close(); log("DONE")
except Exception:
    import traceback; log("ERR", traceback.format_exc())
finally:
    LOG.close()
    subprocess.run(["pkill","-9","-f","[d]esmume-cli"])
    subprocess.run(["pkill","-9","-f","[e]mucap-desmume-nds-bridge"])
    os._exit(0)
