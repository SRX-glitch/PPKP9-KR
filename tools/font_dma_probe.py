import sys, json, subprocess, os, shutil, time
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
    def rd(addr,length,mt="arm9"):
        j=e.call("read_memory",{"memory_type":mt,"address":hex(addr),"length":length},30)["json"]
        return bytes.fromhex(j["hex"]) if j and "hex" in j else None
    b0=rd(0x06208000,32); log("VRAM 0x06208000 BEFORE resume:", b0.hex() if b0 else None)
    e.call("resume",{},30); time.sleep(0.6); e.call("pause",{},30)
    b1=rd(0x06208000,32); log("VRAM 0x06208000 AFTER resume :", b1.hex() if b1 else None)
    # DMA registers (arm9 I/O)
    log("--- DMA channels (SAD, DAD, CNT) ---")
    for ch in range(4):
        base=0x040000B0+ch*12
        sad=rd(base,4); dad=rd(base+4,4); cnt=rd(base+8,4)
        def u(x): return int.from_bytes(x,"little") if x else None
        log(f"DMA{ch}: SAD={u(sad):#010x} DAD={u(dad):#010x} CNT={u(cnt):#010x}")
    # display + vram control
    log("DISPCNT_A 0x04000000:", (rd(0x04000000,4) or b'').hex())
    log("DISPCNT_B 0x04001000:", (rd(0x04001000,4) or b'').hex())
    log("VRAMCNT   0x04000240:", (rd(0x04000240,12) or b'').hex())
    log("SUB BGCNT 0x04001008:", (rd(0x04001008,16) or b'').hex())
    e.close(); log("DONE")
except Exception:
    import traceback; log("ERR", traceback.format_exc())
finally:
    LOG.close()
    subprocess.run(["pkill","-9","-f","[d]esmume-cli"])
    subprocess.run(["pkill","-9","-f","[e]mucap-desmume-nds-bridge"])
    os._exit(0)
