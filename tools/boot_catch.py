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
        j=e.call("read_memory",{"memory_type":mt,"address":hex(addr),"length":n},20)["json"]
        return bytes.fromhex(j["hex"]) if j and "hex" in j else b""
    caps=[]; scanned=0
    e.call("resume",{},20); dl=time.time()+45
    while time.time()<dl and len(caps)<40:
        time.sleep(0.015)
        if frozen():
            scanned+=1
            r=regs(); dst=r.get("r2")
            # char-base regions: main 0x06000000-0x06080000, sub 0x06200000-0x06220000, obj
            if isinstance(dst,int) and 0x06000000<=dst<0x07000000:
                sp=r.get("sp"); stk=rd(sp,0x180,"arm9")
                rets=[struct.unpack_from("<I",stk,i)[0] for i in range(0,len(stk)-3,4)]
                code=[v for v in rets if 0x02000000<=v<0x02120000]
                # keep only ones whose src looks like a big RAM font buffer
                caps.append((r,code))
                if len(caps)<=40:
                    log(f"#{len(caps)} src={r['r1']:#x} dst={dst:#x} cnt={r['r3']&0x1fffff if isinstance(r['r3'],int) else 0} callers={[hex(c) for c in code[:6]]}")
            e.call("resume",{},20)
    log(f"scanned {scanned} DMA hits; captured {len(caps)} VRAM DMAs")
    e.screenshot(f"{SD}/boot_now.png")
    # frequency of caller addresses
    import collections
    cc=collections.Counter()
    for r,code in caps:
        for c in code[:4]: cc[c]+=1
    log("top caller addrs:", [(hex(a),n) for a,n in cc.most_common(12)])
    e.close(); log("DONE")
except Exception:
    import traceback; log("ERR", traceback.format_exc())
finally:
    LOG.close()
    subprocess.run(["pkill","-9","-f","[d]esmume-cli"])
    subprocess.run(["pkill","-9","-f","[e]mucap-desmume-nds-bridge"])
    os._exit(0)
