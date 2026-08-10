#!/usr/bin/env python3
"""Load the title state (画面をタッチ! visible) and dump BG/OBJ VRAM of both
engines, render 4bpp tile sheets to locate the Japanese font glyphs."""
import sys, time, zlib, struct, os
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR

def png_gray(path,w,h,pix):
    def ch(t,d): return struct.pack(">I",len(d))+t+d+struct.pack(">I",zlib.crc32(t+d)&0xffffffff)
    raw=bytearray()
    for y in range(h): raw.append(0); raw+=pix[y*w:(y+1)*w]
    open(path,"wb").write(b"\x89PNG\r\n\x1a\n"+ch(b"IHDR",struct.pack(">IIBBBBB",w,h,8,0,0,0,0))+ch(b"IDAT",zlib.compress(bytes(raw),9))+ch(b"IEND",b""))

def tiles_4bpp(data,per_row=32):
    ntiles=len(data)//32; rows=(ntiles+per_row-1)//per_row
    W=per_row*8; H=rows*8; pix=bytearray(W*H)
    for t in range(ntiles):
        tx=(t%per_row)*8; ty=(t//per_row)*8
        for by in range(8):
            for bx in range(4):
                b=data[t*32+by*4+bx]
                pix[(ty+by)*W+tx+bx*2]=(b&0xF)*17
                pix[(ty+by)*W+tx+bx*2+1]=((b>>4)&0xF)*17
    return W,H,pix

def read_block(e,mt,addr,length,chunk=0x1000):
    out=bytearray(); a=addr
    while length>0:
        n=min(chunk,length)
        r=e.call("read_memory",{"memory_type":mt,"address":hex(a),"length":n},60)
        j=r["json"]
        if not j or "hex" not in j: break
        out+=bytes.fromhex(j["hex"]); a+=n; length-=n
    return bytes(out)

e=Emucap()
e.call("bootstrap",{},30)
if not (e.call("status",{},30)["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)
e.call("load_state",{"path":"/root/ppkp9_menu.dss"},30)
e.call("resume",{},30); time.sleep(0.5); e.call("pause",{},30)
e.screenshot(f"{OUTDIR}/vt_state.png")
regions=[("mainBG",0x06000000,0x40000),("subBG",0x06200000,0x20000),
         ("mainOBJ",0x06400000,0x40000),("subOBJ",0x06600000,0x20000)]
for name,addr,ln in regions:
    b=read_block(e,"arm9",addr,ln)
    open(f"{OUTDIR}/vt_{name}.bin","wb").write(b)
    if b:
        W,H,pix=tiles_4bpp(b); png_gray(f"{OUTDIR}/vt_{name}.png",W,H,pix)
    print(f"{name}: {len(b)}B -> vt_{name}.png")
e.close(); print("DONE")
