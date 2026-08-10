#!/usr/bin/env python3
"""Drive to the stable mode-select menu, dump main RAM broadly, render as 1bpp
glyph sheets (16x16 and 12x12) to spot the decompressed font working set."""
import sys, time, zlib, struct
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR

def png_gray(path,w,h,pix):
    def ch(t,d): return struct.pack(">I",len(d))+t+d+struct.pack(">I",zlib.crc32(t+d)&0xffffffff)
    raw=bytearray()
    for y in range(h): raw.append(0); raw+=pix[y*w:(y+1)*w]
    out=b"\x89PNG\r\n\x1a\n"+ch(b"IHDR",struct.pack(">IIBBBBB",w,h,8,0,0,0,0))
    out+=ch(b"IDAT",zlib.compress(bytes(raw),9))+ch(b"IEND",b"")
    open(path,"wb").write(out)

def render_1bpp(data, gw, gh, per_row=48):
    row_bytes=(gw+7)//8
    glyph_bytes=row_bytes*gh
    ng=len(data)//glyph_bytes
    rows=(ng+per_row-1)//per_row
    # 1px gap between glyphs
    W=per_row*(gw+1); H=rows*(gh+1)
    pix=bytearray(W*H)
    for g in range(ng):
        gx=(g%per_row)*(gw+1); gy=(g//per_row)*(gh+1)
        for y in range(gh):
            for x in range(gw):
                byte=data[g*glyph_bytes+y*row_bytes+(x//8)]
                on=(byte>>(7-(x%8)))&1
                pix[(gy+y)*W+gx+x]=255 if on else 40
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
# drive well into the game (menu)
for i in range(8):
    e.call("resume",{},30); time.sleep(1.3); e.call("pause",{},30)
    if i%2==0: e.call("press_buttons",{"buttons":["start"],"frames":4},30)
    e.call("touch",{"x":128,"y":150,"frames":4},30)
e.screenshot(f"{OUTDIR}/ramfont_state.png")
# dump main RAM 0x02000000 .. +0xC0000 (768KB)
main=read_block(e,"main",0x0,0xC0000)
open(f"{OUTDIR}/main_menu.bin","wb").write(main)
print("main bytes:",len(main))
for gw,gh,tag in ((16,16,"16x16"),(12,12,"12x12"),(8,16,"8x16"),(8,8,"8x8")):
    W,H,pix=render_1bpp(main,gw,gh)
    png_gray(f"{OUTDIR}/font_{tag}.png",W,H,pix)
    print("rendered font_%s.png (%dx%d)"%(tag,W,H))
e.close()
print("DONE")
