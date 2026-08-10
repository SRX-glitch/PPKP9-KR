import sys, json, subprocess, os, shutil
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
shutil.rmtree("/root/.local/share/emucap/desmume-nds", ignore_errors=True)
LOG=open("/root/probe.log","w",encoding="utf-8")
def log(*a): print(*a, file=LOG, flush=True)
try:
    from emucap_drv import Emucap, ROM
    e=Emucap()
    e.call("bootstrap",{},30)
    st=e.call("status",{},30)
    if not (st["json"] or {}).get("connected"):
        r=e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},180)
        log("launch connected=", (r["json"] or {}).get("connected"))
    log("load kbd:", e.call("load_state",{"path":"/root/ppkp9_kbd.dss"},30)["text"][:100])
    st=e.call("status",{},30)["json"] or {}
    log("METHODS:", json.dumps(st.get("methods"), ensure_ascii=False))
    log("MEMTYPES:", json.dumps(st.get("memory_types"), ensure_ascii=False))
    for k in ("debugger","backend","capability_notes","contracts"):
        if k in st: log(k.upper()+":", json.dumps(st[k], ensure_ascii=False)[:600])
    e.close(); log("DONE")
except Exception:
    import traceback; log("ERR", traceback.format_exc())
finally:
    LOG.close()
    subprocess.run(["pkill","-9","-f","[d]esmume-cli"])
    subprocess.run(["pkill","-9","-f","[e]mucap-desmume-nds-bridge"])
    os._exit(0)
