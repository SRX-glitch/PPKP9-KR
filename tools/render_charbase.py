#!/usr/bin/env python3
"""Render VRAM char-data at the real BG char-base offsets (from 2D regs) as clean
4bpp 8x8 tile sheets to reveal the keyboard font glyphs."""
import sys, os, struct, zlib
sd=os.path.join(os.path.dirname(__file__),"..","survey")
def png_gray(path,w,h,pix):
    def ch(t,d): return struct.pack(">I",len(d))+t+d+struct.pack(">I",zlib.crc32(t+d)&0xffffffff)
    raw=bytearray()
    for y in range(h): raw.append(0); raw+=pix[y*w:(y+1)*w]
    open(path,"wb").write(b"\x89PNG\r\n\x1a\n"+ch(b"IHDR",struct.pack(">IIBBBBB",w,h,8,0,0,0,0))+ch(b"IDAT",zlib.compress(bytes(raw),9))+ch(b"IEND",b""))
def tiles_4bpp(data,per_row,scale=4,gap=1):
    n=len(data)//32; rows=(n+per_row-1)//per_row
    W=per_row*(8+gap)*scale; H=rows*(8+gap)*scale; pix=bytearray(W*H)
    for t in range(n):
        gx=(t%per_row)*(8+gap)*scale; gy=(t//per_row)*(8+gap)*scale
        for by in range(8):
            for bx in range(4):
                b=data[t*32+by*4+bx]
                for half,val in ((0,b&0xF),(1,(b>>4)&0xF)):
                    c=val*17; X=gx+(bx*2+half)*scale; Y=gy+by*scale
                    for sy in range(scale):
                        for sx in range(scale): pix[(Y+sy)*W+X+sx]=c
    return W,H,pix

for fn,regions in [("kbd_subBG.bin",[("sub_char0x8000",0x8000,0x4000),("sub_char0xc000",0xc000,0x4000),("sub_char0x18000",0x18000,0x4000)]),
                   ("kbd_mainBG.bin",[("main_char0x8000",0x8000,0x4000),("main_char0x18000",0x18000,0x4000)])]:
    p=os.path.join(sd,fn)
    if not os.path.exists(p): print("missing",fn); continue
    d=open(p,"rb").read()
    for tag,off,ln in regions:
        seg=d[off:off+ln]
        W,H,pix=tiles_4bpp(seg,16,scale=4)
        png_gray(os.path.join(sd,f"cb_{tag}.png"),W,H,pix)
        print(f"rendered cb_{tag}.png ({len(seg)}B)")
