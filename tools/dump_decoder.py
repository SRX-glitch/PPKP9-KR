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
    e.call("load_state",{"path":"/root/ppkp9_kbd.dss"},30)
    e.call("resume",{},30); time.sleep(0.3); e.call("pause",{},30)
    e.call("set_breakpoint",{"kind":"write","memory_type":"main","start":hex(0x2D3740),"end":hex(0x2D3744),"pause_on_hit":True},20)
    def frozen():
        s=e.call("status",{},20)["json"] or {}
        return s.get("state")=="frozen" or (s.get("cpus",{}) or {}).get("arm9")=="frozen"
    def regs():
        st=(e.call("get_state",{},20)["json"] or {}).get("state",{})
        return {k:st.get("cpu."+k) for k in ("r0","r1","r2","r3","r4","r5","r6","r7","r8","r9","r10","r11","pc","lr","sp")}
    def rd(addr,n,mt="arm9"):
        out=bytearray(); a=addr
        while n>0:
            k=min(0x8000,n)
            j=e.call("read_memory",{"memory_type":mt,"address":hex(a),"length":k},40)["json"]
            if not j or "hex" not in j: break
            out+=bytes.fromhex(j["hex"]); a+=k; n-=k
        return bytes(out)
    e.call("resume",{},20); dl=time.time()+15; hit=None
    while time.time()<dl:
        time.sleep(0.02)
        if frozen(): hit=regs(); break
    if hit:
        log("HIT pc=%#x r4(dst)=%#x r5(src)=%#x r6=%#x r7=%#x r8=%#x r9=%#x r10=%#x lr=%#x"%(hit["pc"],hit["r4"],hit["r5"],hit["r6"],hit["r7"],hit["r8"],hit["r9"],hit["r10"],hit["lr"]))
        # dump decoder+codec code region and source data
        code=rd(0x0203C000,0x2000,"arm9"); open(f"{SD}/decoder_code.bin","wb").write(code); log("code dump 0x0203C000 len",len(code))
        src=rd(0x02084000,0x2000,"arm9"); open(f"{SD}/font_src_083.bin","wb").write(src); log("src dump 0x02084000 len",len(src))
        # r5 exact source content
        srcexact=rd(hit["r5"]-0x40,0x100,"arm9"); log("src@r5-0x40..+0xc0: "+srcexact.hex())
    else:
        log("no hit")
    e.close(); log("DONE")
except Exception:
    import traceback; log("ERR", traceback.format_exc())
finally:
    LOG.close()
    subprocess.run(["pkill","-9","-f","[d]esmume-cli"])
    subprocess.run(["pkill","-9","-f","[e]mucap-desmume-nds-bridge"])
    os._exit(0)
