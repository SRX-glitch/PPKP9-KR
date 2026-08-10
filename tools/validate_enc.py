import sys, subprocess, os, shutil, time
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
shutil.rmtree("/root/.local/share/emucap/desmume-nds", ignore_errors=True)
SD="/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey"
ROM="/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
from fontenc import encode_glyph
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
    SRC=0x0208435C; DST=0x022D3700
    def rd(addr,n,mt="arm9"):
        j=e.call("read_memory",{"memory_type":mt,"address":hex(addr),"length":n},20)["json"]
        return bytes.fromhex(j["hex"]) if j and "hex" in j else b""
    def wr(addr,data,mt="arm9"):
        e.call("write_memory",{"memory_type":mt,"address":hex(addr),"hex":data.hex()},20)
    # F pattern
    F=[[0]*12 for _ in range(8)]
    for c in range(12): F[0][c]=1
    for r in range(8): F[r][0]=1
    for c in range(8): F[3][c]=1
    src=encode_glyph(F)
    wr(SRC,src)
    e.call("resume",{},20); time.sleep(0.05); e.call("pause",{},20)
    out=rd(DST,0x120)
    # reconstruct 12x8 from output
    def px(r,c):
        if c<4: base=0x28+4*r; off=c
        elif c<8: base=0x2a+4*r; off=c-4
        else: base=0x68+4*r; off=c-8
        b=out[base+off//2]; return (b>>(4*(off%2)))&0xF
    log("reconstructed 12x8 from decoded output:")
    ok=True
    for r in range(8):
        line=""
        for c in range(12):
            v=px(r,c); line+= ("#" if v>=8 else ("." if v>0 else " "))
            intended = F[r][c]
            if (v>=8)!=(intended==1): ok=False
        log("  |"+line+"|")
    log("MATCHES intended F: %s"%ok)
    e.close(); log("DONE")
except Exception:
    import traceback; log("ERR", traceback.format_exc())
finally:
    LOG.close()
    subprocess.run(["pkill","-9","-f","[d]esmume-cli"])
    subprocess.run(["pkill","-9","-f","[e]mucap-desmume-nds-bridge"])
    os._exit(0)
