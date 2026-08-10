#!/usr/bin/env python3
"""Read DS 2D engine registers at the keyboard screen to locate the text BG's
screen-base and char-base precisely (the rigorous way to find the font tiles)."""
import sys, time, struct
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR
KBD="/root/ppkp9_kbd.dss"

def rd(e, addr, n):
    j=e.call("read_memory",{"memory_type":"arm9","address":hex(addr),"length":n},40)["json"]
    return bytes.fromhex(j["hex"]) if j and "hex" in j else b""
def u16(b,o): return struct.unpack_from("<H",b,o)[0]
def u32(b,o): return struct.unpack_from("<I",b,o)[0]

e=Emucap()
e.call("bootstrap",{},30)
if not (e.call("status",{},30)["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)
e.call("load_state",{"path":KBD},30)
e.call("resume",{},30); time.sleep(0.4); e.call("pause",{},30)

for eng,base in (("MAIN",0x04000000),("SUB",0x04001000)):
    regs=rd(e,base,0x60)
    if len(regs)<0x60: print(eng,"reg read short"); continue
    dispcnt=u32(regs,0x00)
    print(f"\n=== {eng} engine @{hex(base)} ===")
    print(f"  DISPCNT=0x{dispcnt:08X}  bgmode={dispcnt&7}  display={'BG' if (dispcnt>>16)&3==1 else (dispcnt>>16)&3}")
    charbase_blk=(dispcnt>>24)&7; scrbase_blk=(dispcnt>>27)&7
    print(f"  ext charBaseBlock={charbase_blk} (x64KB) screenBaseBlock={scrbase_blk} (x64KB)")
    for bg in range(4):
        cnt=u16(regs,0x08+bg*2)
        prio=cnt&3; charb=(cnt>>2)&0xF; scrb=(cnt>>8)&0x1F; sz=(cnt>>14)&3; color256=(cnt>>7)&1
        print(f"  BG{bg}CNT=0x{cnt:04X} prio={prio} charBase={charb}(*16KB={hex(charb*0x4000)}) screenBase={scrb}(*2KB={hex(scrb*0x800)}) 256col={color256} size={sz} enabled={(dispcnt>>(8+bg))&1}")
e.close(); print("\nDONE")
