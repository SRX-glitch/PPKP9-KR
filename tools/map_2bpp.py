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
    def frozen():
        s=e.call("status",{},20)["json"] or {}
        return s.get("state")=="frozen" or (s.get("cpus",{}) or {}).get("arm9")=="frozen"
    def regs():
        st=(e.call("get_state",{},20)["json"] or {}).get("state",{})
        return {k:st.get("cpu."+k) for k in ("r4","r5","r6","pc")}
    def rd(addr,n,mt="arm9"):
        j=e.call("read_memory",{"memory_type":mt,"address":hex(addr),"length":n},20)["json"]
        return bytes.fromhex(j["hex"]) if j and "hex" in j else b""
    def wr(addr,data,mt="arm9"):
        return e.call("write_memory",{"memory_type":mt,"address":hex(addr),"hex":data.hex()},20)["json"]
    # catch decoder to learn exact src/dst for FONT_TABLE[0][0]
    e.call("set_breakpoint",{"kind":"write","memory_type":"main","start":hex(0x2D3740),"end":hex(0x2D3744),"pause_on_hit":True},20)
    e.call("resume",{},20); dl=time.time()+15; r=None
    while time.time()<dl:
        time.sleep(0.02)
        if frozen(): r=regs(); break
    if not r: log("no catch"); raise SystemExit
    SRC=0x0208435C  # FONT_TABLE[0][0]
    DST_BASE=0x022D3700
    log("caught: r4(dst)=%#x r5(src)=%#x r6=%#x"%(r["r4"],r["r5"],r["r6"]))
    e.call("clear_all_breakpoints",{},20)
    # baseline: read source + output
    src0=rd(SRC,36,"arm9"); log("SRC(36B): "+src0.hex())
    def snap_output():
        # step exactly enough frames for a full redecode; resume 1 frame
        e.call("resume",{},20); time.sleep(0.05); e.call("pause",{},20)
        return rd(DST_BASE,0x120,"arm9")
    base=snap_output(); open(f"{SD}/map_base.bin","wb").write(base)
    # all 0xFF
    wr(SRC, b"\xFF"*36,"arm9"); ff=snap_output(); open(f"{SD}/map_ff.bin","wb").write(ff)
    # all 0x00
    wr(SRC, b"\x00"*36,"arm9"); zz=snap_output(); open(f"{SD}/map_00.bin","wb").write(zz)
    # single-byte probe: source[0]=0xFF only
    p=bytearray(36); p[0]=0xFF; wr(SRC,bytes(p),"arm9"); b0=snap_output(); open(f"{SD}/map_b0.bin","wb").write(b0)
    p=bytearray(36); p[2]=0xFF; wr(SRC,bytes(p),"arm9"); b2=snap_output(); open(f"{SD}/map_b2.bin","wb").write(b2)
    # diff offsets where FF differs from 00
    diff=[i for i in range(len(ff)) if ff[i]!=zz[i]]
    log("FF vs 00: %d differing bytes; offsets(abs): %s"%(len(diff), [hex(DST_BASE+i) for i in diff[:40]]))
    log("done capture")
    e.close(); log("DONE")
except Exception:
    import traceback; log("ERR", traceback.format_exc())
finally:
    LOG.close()
    subprocess.run(["pkill","-9","-f","[d]esmume-cli"])
    subprocess.run(["pkill","-9","-f","[e]mucap-desmume-nds-bridge"])
    os._exit(0)
