#!/usr/bin/env python3
"""Dump the live source buffer (main 0x2CE000..) and render as 4bpp tile sheets
at a few cell sizes to read the kana glyph layout for Hangul placement."""
import sys, time, zlib, struct
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR
KBD="/root/ppkp9_kbd.dss"

def png_gray(path,w,h,pix):
    def ch(t,d): return struct.pack(">I",len(d))+t+d+struct.pack(">I",zlib.crc32(t+d)&0xffffffff)
    raw=bytearray()
    for y in range(h): raw.append(0); raw+=pix[y*w:(y+1)*w]
    open(path,"wb").write(b"\x89PNG\r\n\x1a\n"+ch(b"IHDR",struct.pack(">IIBBBBB",w,h,8,0,0,0,0))+ch(b"IDAT",zlib.compress(bytes(raw),9))+ch(b"IEND",b""))

def render_4bpp_tiles(data,per_row,scale=3,gap=1):
    n=len(data)//32; rows=(n+per_row-1)//per_row
    W=per_row*(8+gap)*scale; H=rows*(8+gap)*scale; pix=bytearray(W*H)
    for t in range(n):
        gx=(t%per_row)*(8+gap)*scale; gy=(t//per_row)*(8+gap)*scale
        for by in range(8):
            for bx in range(4):
                b=data[t*32+by*4+bx]
                for half,val in ((0,b&0xF),(1,(b>>4)&0xF)):
                    px=bx*2+half; c=val*17
                    for sy in range(scale):
                        for sx in range(scale):
                            pix[(gy+by*scale+sy)*W+gx+px*scale+sx]=c
    return W,H,pix

e=Emucap()
e.call("bootstrap",{},30)
if not (e.call("status",{},30)["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)
e.call("load_state",{"path":KBD},30)
e.call("resume",{},30); time.sleep(0.4); e.call("pause",{},30)

buf=bytearray(); a=0x2CE000; end=0x2D8000
while a<end:
    j=e.call("read_memory",{"memory_type":"main","address":hex(a),"length":0x1000},60)["json"]
    if not j or "hex" not in j: break
    buf+=bytes.fromhex(j["hex"]); a+=0x1000
open(f"{OUTDIR}/srcbuf.bin","wb").write(buf)
print("srcbuf bytes:",len(buf))
for per in (16,32):
    W,H,pix=render_4bpp_tiles(buf,per,scale=3)
    png_gray(f"{OUTDIR}/srcbuf_{per}.png",W,H,pix)
    print(f"rendered srcbuf_{per}.png {W}x{H}")
e.close(); print("DONE")
