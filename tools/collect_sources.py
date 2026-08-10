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
    def frozen():
        s=e.call("status",{},20)["json"] or {}
        return s.get("state")=="frozen" or (s.get("cpus",{}) or {}).get("arm9")=="frozen"
    def regs():
        st=(e.call("get_state",{},20)["json"] or {}).get("state",{})
        return {k:st.get("cpu."+k) for k in ("r4","r5","r6","pc")}
    # watch a wide buffer range to catch many glyph decodes
    e.call("set_breakpoint",{"kind":"write","memory_type":"main","start":hex(0x2D3720),"end":hex(0x2D3900),"pause_on_hit":True},20)
    seen={}
    e.call("resume",{},20); dl=time.time()+20
    while time.time()<dl and len(seen)<30:
        time.sleep(0.01)
        if frozen():
            r=regs(); s=r["r5"]
            if s not in seen: seen[s]=(r["r4"],r["r6"])
            e.call("resume",{},20)
    log("distinct decode sources (R5) -> (R4 dest, R6):")
    for s in sorted(seen):
        d,r6=seen[s]
        # which FONT_TABLE block? source in glyph-data region
        log("  src=%#010x  dst=%#x r6=%#x"%(s,d,r6))
    log("count=%d"%len(seen))
    e.close(); log("DONE")
except Exception:
    import traceback; log("ERR", traceback.format_exc())
finally:
    LOG.close()
    subprocess.run(["pkill","-9","-f","[d]esmume-cli"])
    subprocess.run(["pkill","-9","-f","[e]mucap-desmume-nds-bridge"])
    os._exit(0)
