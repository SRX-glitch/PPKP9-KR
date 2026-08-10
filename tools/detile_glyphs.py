#!/usr/bin/env python3
"""De-tile the VRAM SUB font (kbd_subBG 0x8000..0xC000) into full glyphs at
several cell sizes/arrangements and render, to determine the real glyph cell."""
import os,struct,zlib
sd=os.path.join(os.path.dirname(__file__),"..","survey")
def png_gray(path,w,h,pix):
    def ch(t,d): return struct.pack(">I",len(d))+t+d+struct.pack(">I",zlib.crc32(t+d)&0xffffffff)
    raw=bytearray()
    for y in range(h): raw.append(0); raw+=pix[y*w:(y+1)*w]
    open(path,"wb").write(b"\x89PNG\r\n\x1a\n"+ch(b"IHDR",struct.pack(">IIBBBBB",w,h,8,0,0,0,0))+ch(b"IDAT",zlib.compress(bytes(raw),9))+ch(b"IEND",b""))

d=open(os.path.join(sd,"kbd_subBG.bin"),"rb").read()
font=d[0x8000:0xC000]  # 512 tiles of 32B (4bpp 8x8)

def tile_px(t):  # return 8x8 list of nibble values, row-major
    px=[[0]*8 for _ in range(8)]
    for by in range(8):
        for bx in range(4):
            b=t[by*4+bx]
            px[by][bx*2]=b&0xF; px[by][bx*2+1]=(b>>4)&0xF
    return px

tiles=[tile_px(font[i*32:i*32+32]) for i in range(len(font)//32)]

# Arrangement A: glyphs are 2x2 tile blocks laid out sequentially:
#   tile order within glyph = TL,TR,BL,BR  (row-major of tiles)
# Arrangement B: TL,BL,TR,BR (column-major)
for tag,order in [("seq_TLTRBLBR",[(0,0),(0,1),(1,0),(1,1)]),
                  ("seq_TLBLTRBR",[(0,0),(1,0),(0,1),(1,1)])]:
    nG=len(tiles)//4
    per=16; rows=(nG+per-1)//per; scale=3; gap=2
    W=per*(16+gap)*scale; H=rows*(16+gap)*scale; pix=bytearray(W*H)
    for g in range(nG):
        gt=tiles[g*4:g*4+4]
        gx=(g%per)*(16+gap)*scale; gy=(g//per)*(16+gap)*scale
        for qi,(ry,rx) in enumerate(order):
            tp=gt[qi]
            for yy in range(8):
                for xx in range(8):
                    c=tp[yy][xx]*17
                    X=gx+(rx*8+xx)*scale; Y=gy+(ry*8+yy)*scale
                    for sy in range(scale):
                        for sx in range(scale): pix[(Y+sy)*W+X+sx]=c
    png_gray(os.path.join(sd,f"detile_{tag}.png"),W,H,pix)
    print("wrote detile_%s.png (%d glyphs)"%(tag,nG))
