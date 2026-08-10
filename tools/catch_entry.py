import sys, subprocess, os, shutil, time, struct
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
shutil.rmtree("/root/.local/share/emucap/desmume-nds", ignore_errors=True)
SD="/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey"
LOG=open("/root/probe.log","w",encoding="utf-8")
def log(*a): print(*a, file=LOG, flush=True)
try:
    from emucap_drv import Emucap, ROM
    e=Emucap()
    e.call("bootstrap",{},30)
    if not (e.call("status",{},30)["json"] or {}).get("connected"):
        e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},180)
    e.call("load_state",{"path":"/root/ppkp9_dlg.dss"},30)
    e.call("resume",{},30); time.sleep(0.6); e.call("pause",{},30)
    DMASET=0x01FF8098
    e.call("set_breakpoint",{"kind":"exec","memory_type":"arm9","start":hex(DMASET),"end":hex(DMASET),"pause_on_hit":True},20)
    def regs():
        st=(e.call("get_state",{},20)["json"] or {}).get("state",{})
        return {k:st.get("cpu."+k) for k in ("r0","r1","r2","r3","pc","lr","sp")}
    def frozen():
        s=e.call("status",{},20)["json"] or {}
        return s.get("state")=="frozen" or (s.get("cpus",{}) or {}).get("arm9")=="frozen"
    def rd(addr,n,mt="arm9"):
        j=e.call("read_memory",{"memory_type":mt,"address":hex(addr),"length":n},20)["json"]
        return bytes.fromhex(j["hex"]) if j and "hex" in j else b""
    caught=[]; allchar=[]
    def pump(secs):
        e.call("resume",{},20); dl=time.time()+secs
        while time.time()<dl and len(caught)<8:
            time.sleep(0.02)
            if frozen():
                r=regs(); dst=r.get("r2")
                if isinstance(dst,int) and 0x06208000<=dst<0x06220000:
                    sp=r.get("sp"); stk=rd(sp,0x140,"arm9")
                    rets=[struct.unpack_from("<I",stk,i)[0] for i in range(0,len(stk)-3,4)]
                    code=[hex(v) for v in rets if 0x02000000<=v<0x02120000]
                    log(f"CHAR-DMA src={r['r1']:#x} dst={dst:#x} cnt={r['r3']:#x}")
                    log(f"   caller-candidates: {code[:20]}")
                    caught.append((r,code))
                e.call("resume",{},20)
    seq=[("t",55,98),("t",55,98),("b","a"),("t",128,110),("b","a"),("t",190,160),("b","a"),("b","a"),("b","a")]
    for i,s in enumerate(seq):
        if frozen(): e.call("resume",{},20)
        e.call("pause",{},20)
        if s[0]=="t": e.call("touch",{"x":s[1],"y":s[2],"frames":8},20)
        else: e.call("press_buttons",{"buttons":[s[1]],"frames":8},20)
        pump(3.5)
        e.screenshot(f"{SD}/entry_{i}.png")
        if len(caught)>=3: break
    log(f"caught {len(caught)} char-base DMAs")
    e.close(); log("DONE")
except Exception:
    import traceback; log("ERR", traceback.format_exc())
finally:
    LOG.close()
    subprocess.run(["pkill","-9","-f","[d]esmume-cli"])
    subprocess.run(["pkill","-9","-f","[e]mucap-desmume-nds-bridge"])
    os._exit(0)
