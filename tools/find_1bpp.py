#!/usr/bin/env python3
"""Take the DENSEST, most distinctive glyph tile from the confirmed VRAM font
(0x8000+), convert to 1bpp (both bit orders), and full-scan main RAM + the ROM
for a UNIQUE match = the 1bpp font source."""
import sys, time
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR

vram=open(f"{OUTDIR}/kbd_subBG.bin","rb").read()
# rank font tiles by density, pick the most distinctive (dense, non-uniform)
best=[]
for off in range(0x8000,0xC000,32):
    t=vram[off:off+32]
    ink=sum(bin(b).count("1") for b in t)
    best.append((ink,off,t))
best.sort(reverse=True)
picks=[b for b in best if 100<b[0]<160][:6]   # medium-dense, glyph-like

def to1bpp(t,msb=True):
    px=[]
    for b in t: px.append(b&0xF); px.append((b>>4)&0xF)
    out=bytearray()
    for row in range(8):
        byte=0
        for col in range(8):
            if px[row*8+col]!=0:
                byte|=(1<<(7-col)) if msb else (1<<col)
        out.append(byte)
    return bytes(out)

rom=open("/mnt/c/Users/jngji/Desktop/실험실/rom/Power Pro Kun Pocket 9 (Japan).nds","rb").read()

def rom_find(pat):
    out=[]; s=0
    while True:
        i=rom.find(pat,s)
        if i<0 or len(out)>=5: break
        out.append(i); s=i+1
    return out

def ram_full(e,hexpat):
    start=0; res=[]
    while start<0x400000:
        j=e.call("find_pattern",{"memory_type":"main","hex":hexpat,"start":start,"length":0x400000-start},40)["json"]
        if not j: break
        res+=j.get("matches",[])
        if not j.get("truncated_scan") or len(res)>=6: break
        start=j.get("start",start)+j.get("scanned",0)
        if j.get("scanned",0)==0: break
    return res

e=Emucap()
e.call("bootstrap",{},30)
if not (e.call("status",{},30)["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"ppkp9"} if False else {"content_path":ROM,"system":"nds","name":"ppkp9"},120)
e.call("load_state",{"path":"/root/ppkp9_kbd.dss"},30)
e.call("resume",{},30); time.sleep(0.4); e.call("pause",{},30)

for ink,off,t in picks:
    for msb in (True,False):
        p=to1bpp(t,msb)
        rmatch=rom_find(p)
        ramatch=ram_full(e,p.hex())
        print(f"glyph 0x{off:X} ink={ink} {'msb' if msb else 'lsb'}: ROM={[hex(x) for x in rmatch]} RAM={[hex(x) for x in ramatch[:4]]}")
e.close(); print("DONE")
