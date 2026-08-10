import sys, subprocess, os, shutil, time
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
shutil.rmtree("/root/.local/share/emucap/desmume-nds", ignore_errors=True)
LOG=open("/root/probe.log","w",encoding="utf-8")
def log(*a): print(*a, file=LOG, flush=True)
try:
    from emucap_drv import Emucap, ROM
    e=Emucap()
    e.call("bootstrap",{},30)
    if not (e.call("status",{},30)["json"] or {}).get("connected"):
        e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},180)
    e.call("load_state",{"path":"/root/ppkp9_kbd.dss"},30)
    e.call("resume",{},30); time.sleep(0.6); e.call("pause",{},30)
    def rd(a,n=32,mt="main"):
        j=e.call("read_memory",{"memory_type":mt,"address":hex(a),"length":n},30)["json"]
        return j.get("hex") if j else None
    def wr(a,data,mt="main"):
        return e.call("write_memory",{"memory_type":mt,"address":hex(a),"hex":data.hex()},30)["json"]
    A=0x2D3740
    log("orig   :", rd(A))
    log("write  :", wr(A, b"\xEE"*32))
    log("read@0f:", rd(A), "(no resume)")
    for k in range(1,5):
        e.call("resume",{},30); time.sleep(0.05); e.call("pause",{},30)
        log(f"read@{k}step:", rd(A))
    e.close(); log("DONE")
except Exception:
    import traceback; log("ERR", traceback.format_exc())
finally:
    LOG.close()
    subprocess.run(["pkill","-9","-f","[d]esmume-cli"])
    subprocess.run(["pkill","-9","-f","[e]mucap-desmume-nds-bridge"])
    os._exit(0)
