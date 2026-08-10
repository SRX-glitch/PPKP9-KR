#!/usr/bin/env python3
"""Test the 1bpp-font + BitUnPack theory: take a SEQUENCE of consecutive VRAM
font tiles, reduce each to 1bpp (both bit orders), concatenate, and search the
RAM dump AND ROM for that contiguous byte sequence = the 1bpp font source."""
import os, struct
sd=os.path.join(os.path.dirname(__file__),"..","survey")
ram=open(os.path.join(sd,"main_full.bin"),"rb").read()
rom=open("/mnt/c/Users/jngji/Desktop/실험실/rom/Power Pro Kun Pocket 9 (Japan).nds","rb").read()
vram=open(os.path.join(sd,"kbd_subBG.bin"),"rb").read()

def tile_to_1bpp(t, msb=True):
    px=[]
    for b in t: px.append(b&0xF); px.append((b>>4)&0xF)
    out=bytearray()
    for row in range(8):
        byte=0
        for col in range(8):
            if px[row*8+col]!=0:
                byte |= (1<<(7-col)) if msb else (1<<col)
        out.append(byte)
    return bytes(out)

# try sequences starting at several offsets in the font region
def find_seq(vbase, ntiles, msb):
    seq=bytearray()
    for k in range(ntiles):
        seq+=tile_to_1bpp(vram[vbase+k*32:vbase+k*32+32], msb)
    ri=ram.find(bytes(seq)); oi=rom.find(bytes(seq))
    return seq, ri, oi

print("searching 1bpp glyph sequences (16 consecutive tiles) ...")
found=False
for vbase in range(0x8000,0xB000,0x200):
    for msb in (True,False):
        seq,ri,oi=find_seq(vbase,16,msb)
        if ri>=0 or oi>=0:
            found=True
            print(f"  VRAM 0x{vbase:X} 16 tiles {'MSB' if msb else 'LSB'}: RAM={hex(ri) if ri>=0 else '-'} ROM={hex(oi) if oi>=0 else '-'}")
# also try 8-tile sequences if 16 failed
if not found:
    print("  16-tile: none. Trying 8-tile sequences...")
    for vbase in range(0x8000,0xB000,0x100):
        for msb in (True,False):
            seq,ri,oi=find_seq(vbase,8,msb)
            if ri>=0 or oi>=0:
                found=True
                print(f"  VRAM 0x{vbase:X} 8 tiles {'MSB' if msb else 'LSB'}: RAM={hex(ri) if ri>=0 else '-'} ROM={hex(oi) if oi>=0 else '-'}")
if not found:
    print("  => 1bpp sequence not found either. Font uses different packing/codec.")
