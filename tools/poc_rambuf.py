import sys, json, subprocess, os, shutil, time, base64
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
    e.call("load_state",{"path":"/root/ppkp9_kbd.dss"},30)
    e.call("resume",{},30); time.sleep(0.6); e.call("pause",{},30)
    e.screenshot(f"{SD}/poc_rb_before.png")
    # overwrite a chunk of the font RAM buffer with 0xFF (solid white glyphs)
    def wr(addr, data, mt="main"):
        h=data.hex()
        return e.call("write_memory",{"memory_type":mt,"address":hex(addr),"hex":h},30)["text"][:120]
    payload=b"\xFF"*0x1000   # 4KB = 128 tiles solid
    log("write result:", wr(0x2D3740, payload, "main"))
    # let it run so DMA re-copies to VRAM
    e.call("resume",{},30); time.sleep(0.8); e.call("pause",{},30)
    e.screenshot(f"{SD}/poc_rb_after.png")
    # read back to confirm the write stuck in RAM
    j=e.call("read_memory",{"memory_type":"main","address":hex(0x2D3740),"length":32},30)["json"]
    log("readback 0x022D3740:", j.get("hex") if j else None)
    e.close(); log("DONE")
except Exception:
    import traceback; log("ERR", traceback.format_exc())
finally:
    LOG.close()
    subprocess.run(["pkill","-9","-f","[d]esmume-cli"])
    subprocess.run(["pkill","-9","-f","[e]mucap-desmume-nds-bridge"])
    os._exit(0)
