import sys, subprocess, os, shutil, time
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
shutil.rmtree("/root/.local/share/emucap/desmume-nds", ignore_errors=True)
SD="/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey"
ROM="/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
LOG=open("/root/probe.log","w",encoding="utf-8")
def log(*a): print(*a, file=LOG, flush=True)
try:
    from emucap_drv import Emucap
    g=open(f"{SD}/han_glyphs.bin","rb").read(); han=g[:36]; geul=g[36:72]
    e=Emucap()
    e.call("bootstrap",{},30)
    if not (e.call("status",{},30)["json"] or {}).get("connected"):
        e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},180)
    e.call("load_state",{"path":"/root/ppkp9_kbd.dss"},30)
    e.call("resume",{},30); time.sleep(0.4); e.call("pause",{},30)
    region=0x0207E000; length=0x8000
    buf=bytearray(); i=0
    while len(buf)<length:
        buf+= han if (i%2==0) else geul; i+=1
    buf=bytes(buf[:length])
    for off in range(0,length,0x2000):
        e.call("write_memory",{"memory_type":"arm9","address":hex(region+off),"hex":buf[off:off+0x2000].hex()},40)
    e.call("resume",{},20); time.sleep(0.5); e.call("pause",{},20)
    e.screenshot(f"{SD}/onscreen_han.png")
    log("shot saved")
    e.close(); log("DONE")
except Exception:
    import traceback; log("ERR", traceback.format_exc())
finally:
    LOG.close()
    subprocess.run(["pkill","-9","-f","[d]esmume-cli"])
    subprocess.run(["pkill","-9","-f","[e]mucap-desmume-nds-bridge"])
    os._exit(0)
