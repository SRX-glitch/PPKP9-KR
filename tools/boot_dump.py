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
    DMASET=0x01FF8098
    e.call("set_breakpoint",{"kind":"exec","memory_type":"arm9","start":hex(DMASET),"end":hex(DMASET),"pause_on_hit":True},20)
    def regs():
        st=(e.call("get_state",{},20)["json"] or {}).get("state",{})
        return {k:st.get("cpu."+k) for k in ("r0","r1","r2","r3","pc","lr","sp")}
    def frozen():
        s=e.call("status",{},20)["json"] or {}
        return s.get("state")=="frozen" or (s.get("cpus",{}) or {}).get("arm9")=="frozen"
    def rd(addr,n,mt="arm9"):
        out=bytearray(); a=addr
        while n>0:
            k=min(0x8000,n)
            j=e.call("read_memory",{"memory_type":mt,"address":hex(a),"length":k},40)["json"]
            if not j or "hex" not in j: break
            out+=bytes.fromhex(j["hex"]); a+=k; n-=k
        return bytes(out)
    # find a stable sub-BG char upload (caller 0x20b0a44)
    e.call("resume",{},20); dl=time.time()+40; found=None
    while time.time()<dl:
        time.sleep(0.015)
        if frozen():
            r=regs(); dst=r.get("r2")
            if isinstance(dst,int) and 0x06200000<=dst<0x06220000 and r.get("r3") and (r["r3"]&0x1fffff)==512:
                found=r; break
            e.call("resume",{},20)
    if found:
        log("caught font upload: src=%#x dst=%#x cnt=%d"%(found["r1"],found["r2"],found["r3"]&0x1fffff))
        # dump overlay code region + src buffer
        code=rd(0x02080000,0x40000,"arm9")   # 0x02080000-0x020C0000
        open(f"{SD}/boot_code_80000.bin","wb").write(code); log("code dump",len(code))
        srcbuf=rd(0x022C0000,0x20000,"arm9")
        open(f"{SD}/boot_srcbuf.bin","wb").write(srcbuf); log("srcbuf dump",len(srcbuf))
    else:
        log("no font upload caught")
    e.close(); log("DONE")
except Exception:
    import traceback; log("ERR", traceback.format_exc())
finally:
    LOG.close()
    subprocess.run(["pkill","-9","-f","[d]esmume-cli"])
    subprocess.run(["pkill","-9","-f","[e]mucap-desmume-nds-bridge"])
    os._exit(0)
