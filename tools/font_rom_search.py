#!/usr/bin/env python3
"""Search the ROM for the font as a contiguous 1bpp glyph sequence (robust vs.
single-tile false positives). Uses medium-density consecutive VRAM font tiles."""
import os,sys
sd=os.path.join(os.path.dirname(__file__),"..","survey")
rom=open("/mnt/c/Users/jngji/Desktop/실험실/rom/Power Pro Kun Pocket 9 (Japan).nds","rb").read()
vram=open(os.path.join(sd,"kbd_subBG.bin"),"rb").read()

def tile_1bpp(t, msb=True):
    px=[]
    for b in t: px.append(b&0xF); px.append((b>>4)&0xF)
    out=bytearray()
    for row in range(8):
        byte=0
        for col in range(8):
            if px[row*8+col]!=0: byte|=(1<<(7-col)) if msb else (1<<col)
        out.append(byte)
    return bytes(out)

# find a run of consecutive MEDIUM-density non-blank tiles in the font region
def find_run(start_search):
    for base in range(start_search, 0xC000-32*40, 32):
        run=[]
        for k in range(40):
            t=vram[base+k*32:base+k*32+32]
            ink=sum(bin(b).count("1") for b in t)  # out of 256
            if 30<ink<150: run.append(t)
            else: break
        if len(run)>=12:
            return base,run
    return None,None

for start in (0x8000,0x8400,0x8800,0x9000,0xA000):
    base,run=find_run(start)
    if not run: continue
    for msb in (True,False):
        seq=b"".join(tile_1bpp(t,msb) for t in run[:12])
        i=rom.find(seq)
        if i>=0:
            print(f"FONT FOUND @ROM 0x{i:X}  (from VRAM 0x{base:X}, {'MSB' if msb else 'LSB'}, {len(run)} tiles)")
            sys.exit(0)
    # also try 4bpp direct (in case font uncompressed 4bpp in ROM)
    seq4=b"".join(run[:12])
    i=rom.find(seq4)
    if i>=0:
        print(f"FONT FOUND (4bpp) @ROM 0x{i:X} from VRAM 0x{base:X}")
        sys.exit(0)
print("1bpp/4bpp font sequence NOT found in ROM -> font is custom-compressed (not a raw 1bpp/4bpp blob).")
