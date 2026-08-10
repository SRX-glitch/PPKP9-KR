#!/usr/bin/env python3
"""Boot to title, dump ARM9 VRAM (0x06000000) + main RAM, render as 4bpp & 1bpp
tile sheets to PNG for visual font inspection. Pure-python PNG (no PIL)."""
import sys, time, zlib, struct
sys.path.insert(0, "/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR

def png_gray(path, w, h, pix):
    def chunk(t, d): return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t+d)&0xffffffff)
    raw=bytearray()
    for y in range(h):
        raw.append(0); raw += pix[y*w:(y+1)*w]
    out=b"\x89PNG\r\n\x1a\n"
    out+=chunk(b"IHDR", struct.pack(">IIBBBBB", w,h,8,0,0,0,0))
    out+=chunk(b"IDAT", zlib.compress(bytes(raw),9))
    out+=chunk(b"IEND", b"")
    open(path,"wb").write(out)

def tiles_4bpp(data, tiles_per_row=32):
    # DS 4bpp: 8x8 tile = 32 bytes, 2 px per byte (low nibble first)
    ntiles=len(data)//32
    rows=(ntiles+tiles_per_row-1)//tiles_per_row
    W=tiles_per_row*8; H=rows*8
    pix=bytearray(W*H)
    for t in range(ntiles):
        tx=(t%tiles_per_row)*8; ty=(t//tiles_per_row)*8
        for by in range(8):
            for bx in range(4):
                b=data[t*32+by*4+bx]
                lo=b&0xF; hi=(b>>4)&0xF
                px0=tx+bx*2; py=ty+by
                pix[py*W+px0]=lo*17
                pix[py*W+px0+1]=hi*17
    return W,H,pix

def tiles_1bpp(data, tiles_per_row=32):
    # 8x8 tile = 8 bytes, 1 bit per px
    ntiles=len(data)//8
    rows=(ntiles+tiles_per_row-1)//tiles_per_row
    W=tiles_per_row*8; H=rows*8
    pix=bytearray(W*H)
    for t in range(ntiles):
        tx=(t%tiles_per_row)*8; ty=(t//tiles_per_row)*8
        for by in range(8):
            b=data[t*8+by]
            for bit in range(8):
                on=(b>>(7-bit))&1
                pix[(ty+by)*W+tx+bit]=255 if on else 0
    return W,H,pix

def read_block(e, memtype, addr, length, chunk=0x1000):
    out=bytearray()
    a=addr
    while length>0:
        n=min(chunk,length)
        r=e.call("read_memory",{"memory_type":memtype,"address":hex(a),"length":n},60)
        j=r["json"]
        if not j or "hex" not in j:
            print("  read fail @",hex(a),":",r["text"][:120]); break
        out+=bytes.fromhex(j["hex"]); a+=n; length-=n
    return bytes(out)

e=Emucap()
e.call("bootstrap",{},30)
st=e.call("status",{},30)
if not (st["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)
# advance to title (logos->title)
for _ in range(4):
    e.call("resume",{},30); time.sleep(1.2); e.call("pause",{},30)
e.screenshot(f"{OUTDIR}/vram_state.png")
print("state screenshot saved")

# dump BG/OBJ VRAM engine A: 0x06000000..0x06080000 (512K) -> take 0x20000
vram=read_block(e,"arm9",0x06000000,0x20000)
open(f"{OUTDIR}/vram_A.bin","wb").write(vram)
print("vram bytes:",len(vram))
if vram:
    W,H,pix=tiles_4bpp(vram); png_gray(f"{OUTDIR}/vram_4bpp.png",W,H,pix)
    W,H,pix=tiles_1bpp(vram); png_gray(f"{OUTDIR}/vram_1bpp.png",W,H,pix)
    print("rendered vram_4bpp.png, vram_1bpp.png")

# also dump a chunk of main RAM to hunt decompressed font working set
main=read_block(e,"main",0x0,0x40000)
open(f"{OUTDIR}/main_0.bin","wb").write(main)
print("main bytes:",len(main))
e.close()
print("DONE")
