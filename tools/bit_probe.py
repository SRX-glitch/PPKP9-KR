import sys, subprocess, os, shutil, time
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
shutil.rmtree("/root/.local/share/emucap/desmume-nds", ignore_errors=True)
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
    SRC=0x0208435C; DST=0x022D3728  # byte0 -> 0x28
    def rd(addr,n,mt="arm9"):
        j=e.call("read_memory",{"memory_type":mt,"address":hex(addr),"length":n},20)["json"]
        return bytes.fromhex(j["hex"]) if j and "hex" in j else b""
    def wr(addr,data,mt="arm9"):
        e.call("write_memory",{"memory_type":mt,"address":hex(addr),"hex":data.hex()},20)
    def probe(byte0):
        p=bytearray(36); p[0]=byte0; wr(SRC,bytes(p))
        e.call("resume",{},20); time.sleep(0.05); e.call("pause",{},20)
        out=rd(DST,2)  # 2 bytes = 4 nibbles = pixels 0..3
        # pixel order: 0x28 lo, 0x28 hi, 0x29 lo, 0x29 hi
        px=[out[0]&0xF,(out[0]>>4)&0xF,out[1]&0xF,(out[1]>>4)&0xF]
        return px
    # test each 2-bit field independently
    for name,vals in [("bits6-7(px?)",[0x40,0x80,0xC0]),("bits4-5",[0x10,0x20,0x30]),
                      ("bits2-3",[0x04,0x08,0x0C]),("bits0-1",[0x01,0x02,0x03])]:
        for v in vals:
            log("byte0=%#04x (%s): pixels=%s"%(v,name,probe(v)))
    e.close(); log("DONE")
except Exception:
    import traceback; log("ERR", traceback.format_exc())
finally:
    LOG.close()
    subprocess.run(["pkill","-9","-f","[d]esmume-cli"])
    subprocess.run(["pkill","-9","-f","[e]mucap-desmume-nds-bridge"])
    os._exit(0)
