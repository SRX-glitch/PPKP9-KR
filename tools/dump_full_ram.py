#!/usr/bin/env python3
"""Boot original ROM to the keyboard state and dump full main RAM (4MB) + shared
WRAM, for offline compressed-font analysis."""
import sys, time
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR
KBD="/root/ppkp9_kbd.dss"

def read_block(e,mt,addr,length,chunk=0x2000):
    out=bytearray(); a=addr
    while length>0:
        n=min(chunk,length)
        j=e.call("read_memory",{"memory_type":mt,"address":hex(a),"length":n},60)["json"]
        if not j or "hex" not in j:
            print("read fail @",hex(a)); break
        out+=bytes.fromhex(j["hex"]); a+=n; length-=n
    return bytes(out)

e=Emucap()
e.call("bootstrap",{},30)
if not (e.call("status",{},30)["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)
e.call("load_state",{"path":KBD},30)
e.call("resume",{},30); time.sleep(0.4); e.call("pause",{},30)
print("dumping main RAM 4MB...")
main=read_block(e,"main",0x0,0x400000)
open(f"{OUTDIR}/main_full.bin","wb").write(main)
print("main_full.bin:",len(main))
e.close(); print("DONE")
