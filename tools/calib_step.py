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
    e.call("load_state",{"path":"/root/ppkp9_anchor.dss"},30)
    A=0x2D3740
    def rd(n=8):
        for _ in range(3):
            j=e.call("read_memory",{"memory_type":"main","address":hex(A),"length":n},20)["json"]
            if j and "hex" in j: return j["hex"]
            e.call("pause",{},10)
        return None
    def wr(data):
        return e.call("write_memory",{"memory_type":"main","address":hex(A),"hex":data.hex()},20)["json"]
    def step(K):
        r=e.call("step_instructions",{"count":K},120)
        e.call("pause",{},10)
        return r["json"]
    for K in (500, 5000, 50000):
        e.call("load_state",{"path":"/root/ppkp9_anchor.dss"},30)
        e.call("pause",{},10)
        wr(b"\xEE"*8); before=rd()
        sj=step(K); after=rd()
        pc=(sj or {}).get("pc")
        log(f"K={K:>6}: before={before} after={after} changed={before!=after} pc={hex(pc) if pc else None}")
    e.close(); log("DONE")
except Exception:
    import traceback; log("ERR", traceback.format_exc())
finally:
    LOG.close()
    subprocess.run(["pkill","-9","-f","[d]esmume-cli"])
    subprocess.run(["pkill","-9","-f","[e]mucap-desmume-nds-bridge"])
    os._exit(0)
