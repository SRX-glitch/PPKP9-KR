import sys, subprocess, os, shutil, time
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
    def rd(off,n,mt="main"):
        out=bytearray(); x=off
        while n>0:
            k=min(0x10000,n)
            j=e.call("read_memory",{"memory_type":mt,"address":hex(x),"length":k},60)["json"]
            if not j or "hex" not in j: log("readfail@",hex(x)); break
            out+=bytes.fromhex(j["hex"]); x+=k; n-=k
        return bytes(out)
    main=rd(0x0,0x400000,"main")
    open(f"{SD}/main_kbd_full.bin","wb").write(main)
    log("main dump len", hex(len(main)))
    def findall(pat):
        r=[]; i=0
        while True:
            j=main.find(pat,i)
            if j<0: break
            r.append(0x02000000+j); i=j+1
        return r
    for name,val in [("SAD 0x022D3720","20372d02"),("DAD 0x06208400","00842006"),
                     ("bufbase 0x022D3700","00372d02"),("VRAM 0x06208000","00822006"),
                     ("SAD-0x20 0x022D3700? try 0x022D3720 word-aligned","20372d02")]:
        hits=findall(bytes.fromhex(val))
        log(f"{name}: {len(hits)} hits", [hex(h) for h in hits[:16]])
    e.close(); log("DONE")
except Exception:
    import traceback; log("ERR", traceback.format_exc())
finally:
    LOG.close()
    subprocess.run(["pkill","-9","-f","[d]esmume-cli"])
    subprocess.run(["pkill","-9","-f","[e]mucap-desmume-nds-bridge"])
    os._exit(0)
