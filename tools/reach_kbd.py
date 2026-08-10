#!/usr/bin/env python3
"""Replay nav into the name-entry (kana keyboard) screen, save that state, then
dump all VRAM regions + main RAM and render 4bpp/1bpp sheets. The on-screen kana
grid is the font — this gives clean known glyphs to locate the font source."""
import sys, time, zlib, struct, os
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR

KBD="/root/ppkp9_kbd.dss"; DLG="/root/ppkp9_dlg.dss"

def png_gray(path,w,h,pix):
    def ch(t,d): return struct.pack(">I",len(d))+t+d+struct.pack(">I",zlib.crc32(t+d)&0xffffffff)
    raw=bytearray()
    for y in range(h): raw.append(0); raw+=pix[y*w:(y+1)*w]
    open(path,"wb").write(b"\x89PNG\r\n\x1a\n"+ch(b"IHDR",struct.pack(">IIBBBBB",w,h,8,0,0,0,0))+ch(b"IDAT",zlib.compress(bytes(raw),9))+ch(b"IEND",b""))
def tiles_4bpp(data,per_row=32):
    n=len(data)//32; rows=(n+per_row-1)//per_row; W=per_row*8; H=rows*8; pix=bytearray(W*H)
    for t in range(n):
        tx=(t%per_row)*8; ty=(t//per_row)*8
        for by in range(8):
            for bx in range(4):
                b=data[t*32+by*4+bx]
                pix[(ty+by)*W+tx+bx*2]=(b&0xF)*17; pix[(ty+by)*W+tx+bx*2+1]=((b>>4)&0xF)*17
    return W,H,pix
def read_block(e,mt,addr,length,chunk=0x1000):
    out=bytearray(); a=addr
    while length>0:
        n=min(chunk,length)
        j=e.call("read_memory",{"memory_type":mt,"address":hex(a),"length":n},60)["json"]
        if not j or "hex" not in j: break
        out+=bytes.fromhex(j["hex"]); a+=n; length-=n
    return bytes(out)

e=Emucap()
e.call("bootstrap",{},30)
if not (e.call("status",{},30)["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)

if os.path.exists(KBD):
    e.call("load_state",{"path":KBD},30)
    e.call("resume",{},30); time.sleep(0.6); e.call("pause",{},30)
else:
    e.call("load_state",{"path":DLG},30)
    e.call("resume",{},30); time.sleep(0.6); e.call("pause",{},30)
    seq=[("t",55,98),("t",55,98),("b","a"),("t",128,110),("b","a"),("t",190,160),("b","a")]
    for s in seq:
        if s[0]=="t": e.call("touch",{"x":s[1],"y":s[2],"frames":8},30)
        else: e.call("press_buttons",{"buttons":[s[1]],"frames":8},30)
        e.call("resume",{},30); time.sleep(1.5); e.call("pause",{},30)
    print("save kbd state:", e.call("save_state",{"path":KBD},30)["text"][:60])

e.screenshot(f"{OUTDIR}/kbd_state.png")
for name,addr,ln in [("mainBG",0x06000000,0x40000),("subBG",0x06200000,0x20000),
                     ("mainOBJ",0x06400000,0x40000),("subOBJ",0x06600000,0x20000)]:
    b=read_block(e,"arm9",addr,ln); open(f"{OUTDIR}/kbd_{name}.bin","wb").write(b)
    if b: W,H,pix=tiles_4bpp(b); png_gray(f"{OUTDIR}/kbd_{name}.png",W,H,pix)
    print(f"{name}: {len(b)}B")
e.close(); print("DONE")
