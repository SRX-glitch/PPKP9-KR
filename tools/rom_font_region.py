#!/usr/bin/env python3
"""Identify the NitroFS file containing ROM 0xBA7000 and render the font region
as 16x16 metatile glyphs (TL,TR,BL,BR) to locate the kana grid for patching."""
import sys, os, struct, zlib
ROM=sys.argv[1]; OUT=sys.argv[2]
d=open(ROM,"rb").read()
def u16(b,o): return struct.unpack_from("<H",b,o)[0]
def u32(b,o): return struct.unpack_from("<I",b,o)[0]
fnt_off=u32(d,0x40); fat_off=u32(d,0x48); fat_size=u32(d,0x4C)
fat=[(u32(d,fat_off+i*8),u32(d,fat_off+i*8+4)) for i in range(fat_size//8)]
names={}
def walk(dir_id,prefix):
    idx=dir_id&0xFFF; sub=u32(d,fnt_off+idx*8); first=u16(d,fnt_off+idx*8+4)
    p=fnt_off+sub; fid=first
    while True:
        t=d[p]; p+=1
        if t==0: break
        ln=t&0x7F; isdir=(t&0x80)!=0; nm=d[p:p+ln].decode("ascii","replace"); p+=ln
        if isdir: s=u16(d,p); p+=2; walk(s,prefix+"/"+nm)
        else: names[fid]=prefix+"/"+nm; fid+=1
walk(0xF000,"")

TARGET=0xBA7000
for fid,(s,e) in enumerate(fat):
    if s<=TARGET<e:
        print(f"ROM 0x{TARGET:X} is in file id={fid} '{names.get(fid,'?')}' extent 0x{s:X}..0x{e:X} size={e-s}")
        FILE=(fid,s,e); break
else:
    print("not in a FAT file (arm9/overlay/system region)"); FILE=None

def png_gray(path,w,h,pix):
    def ch(t,dd): return struct.pack(">I",len(dd))+t+dd+struct.pack(">I",zlib.crc32(t+dd)&0xffffffff)
    raw=bytearray()
    for y in range(h): raw.append(0); raw+=pix[y*w:(y+1)*w]
    open(path,"wb").write(b"\x89PNG\r\n\x1a\n"+ch(b"IHDR",struct.pack(">IIBBBBB",w,h,8,0,0,0,0))+ch(b"IDAT",zlib.compress(bytes(raw),9))+ch(b"IEND",b""))

def render_16x16(data, base, count, per_row=16, scale=3, order="TLTRBLBR"):
    # each glyph = 4 8x8 tiles (128 bytes) in given order
    W=per_row*(16+2)*scale; rows=(count+per_row-1)//per_row; H=rows*(16+2)*scale
    pix=bytearray(W*H)
    def draw_tile(tile, gx, gy):
        for by in range(8):
            for bx in range(4):
                b=tile[by*4+bx]
                for half,val in ((0,b&0xF),(1,(b>>4)&0xF)):
                    c=val*17; X=gx+(bx*2+half)*scale; Y=gy+by*scale
                    for sy in range(scale):
                        for sx in range(scale):
                            pix[(Y+sy)*W+X+sx]=c
    for g in range(count):
        go=base+g*128
        tiles=[data[go:go+32],data[go+32:go+64],data[go+64:go+96],data[go+96:go+128]]
        if order=="TLTRBLBR": tl,tr,bl,br=tiles
        else: tl,bl,tr,br=tiles
        gx=(g%per_row)*(16+2)*scale; gy=(g//per_row)*(16+2)*scale
        draw_tile(tl,gx,gy); draw_tile(tr,gx+8*scale,gy)
        draw_tile(bl,gx,gy+8*scale); draw_tile(br,gx+8*scale,gy+8*scale)
    return W,H,pix

# render the whole font region as 16x16 glyphs, both orders
region=d[0xBA7000:0xBB2000]   # ~44KB = ~350 glyphs of 128B
for order in ("TLTRBLBR","TLBLTRBR"):
    W,H,pix=render_16x16(region,0,len(region)//128,order=order)
    png_gray(f"{OUT}/romfont_{order}.png",W,H,pix)
    print(f"rendered romfont_{order}.png {W}x{H}")
