import sys, subprocess, os, shutil, time, json
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
    SRC=0x0208435C; DST=0x022D3700; NOUT=0x120
    def rd(addr,n,mt="arm9"):
        j=e.call("read_memory",{"memory_type":mt,"address":hex(addr),"length":n},20)["json"]
        return bytes.fromhex(j["hex"]) if j and "hex" in j else b""
    def wr(addr,data,mt="arm9"):
        e.call("write_memory",{"memory_type":mt,"address":hex(addr),"hex":data.hex()},20)
    def decode_read():
        e.call("resume",{},20); time.sleep(0.05); e.call("pause",{},20)
        return rd(DST,NOUT,"arm9")
    wr(SRC, b"\x00"*36); zero=decode_read()
    # per-byte: set byte i=0xFF, read, record changed nibbles vs zero
    results={}
    for i in range(36):
        p=bytearray(36); p[i]=0xFF; wr(SRC,bytes(p)); out=decode_read()
        lit=[]
        for o in range(len(out)):
            if out[o]!=zero[o]:
                # record which nibbles differ
                if (out[o]&0xF)!=(zero[o]&0xF): lit.append((o,0,out[o]&0xF))
                if (out[o]>>4)!=(zero[o]>>4): lit.append((o,1,(out[o]>>4)&0xF))
        results[i]=lit
        log("byte %2d: %d nibbles: %s"%(i,len(lit),[(hex(o),h,v) for o,h,v in lit[:8]]))
    open(f"{SD}/byte_probe.json","w").write(json.dumps({str(k):v for k,v in results.items()}))
    log("saved byte_probe.json")
    e.close(); log("DONE")
except Exception:
    import traceback; log("ERR", traceback.format_exc())
finally:
    LOG.close()
    subprocess.run(["pkill","-9","-f","[d]esmume-cli"])
    subprocess.run(["pkill","-9","-f","[e]mucap-desmume-nds-bridge"])
    os._exit(0)
