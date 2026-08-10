#!/usr/bin/env python3
"""Build a real persistent patch: overwrite the uncompressed 4bpp tile region
(ROM 0xBAA000-0xBAC000, confirmed to render on the charamake screen) with bold
Hangul glyphs, save patched .nds + an IPS patch, then boot & navigate & shoot."""
import sys, time, shutil, struct
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR
PATCHED="/root/ppkp9_kr.nds"
IPS="/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/ppkp9_kr.ips"

# bold 16x16 '가' (fills the cell; 1=ink)
GA=[
 "0111111111100110","0100000001100110","0100000001100110","0000000001100110",
 "0000000001100110","0111111111100110","0000000001100110","0000000001111110",
 "0000000001100110","0000000001100110","0000000001100110","0000000001100110",
 "0000000001100110","0000000001100110","0000000001100110","0000000000000000"]
def t8(rows,r0,c0,ink=0xF):
    o=bytearray()
    for ry in range(8):
        r=rows[r0+ry]
        for bx in range(4):
            c=c0+bx*2; p0=ink if r[c]=="1" else 0; p1=ink if r[c+1]=="1" else 0
            o.append(p0|(p1<<4))
    return bytes(o)
META=t8(GA,0,0)+t8(GA,0,8)+t8(GA,8,0)+t8(GA,8,8)  # 128B TL,TR,BL,BR

orig=bytearray(open(ROM,"rb").read())
patched=bytearray(orig)
START=0xBAA000; END=0xBAC000
off=START
while off<END: patched[off:off+128]=META; off+=128
open(PATCHED,"wb").write(patched)

# IPS (patch only the changed region as one record; IPS offsets are 24-bit, fits)
def make_ips(orig,new,path):
    rec=bytearray(b"PATCH")
    o=START
    while o<END:
        chunk=bytes(new[o:o+0xFFFF if END-o>0xFFFF else END-o])
        rec+=struct.pack(">I",o)[1:]      # 3-byte offset
        rec+=struct.pack(">H",len(chunk)) # 2-byte size
        rec+=chunk
        o+=len(chunk)
    rec+=b"EOF"
    open(path,"wb").write(rec)
make_ips(orig,patched,IPS)
print(f"patched {hex(START)}..{hex(END)} -> {PATCHED}; IPS -> {IPS}")

# boot patched & navigate to charamake keyboard, screenshotting each late step
e=Emucap()
e.call("bootstrap",{},30)
print("launch:", e.call("launch",{"content_path":PATCHED,"system":"nds","name":"ppkp9kr"},120)["text"][:60])
def adv(w): e.call("resume",{},30); time.sleep(w); e.call("pause",{},30)
def tap(x,y,w=1.4): e.call("touch",{"x":x,"y":y,"frames":8},30); adv(w)
def btn(b,w=1.4): e.call("press_buttons",{"buttons":[b],"frames":8},30); adv(w)
for i in range(7):
    adv(1.3)
    if i%2==0: e.call("press_buttons",{"buttons":["start"],"frames":4},30)
tap(128,96,2.0); tap(128,96,1.5)
tap(60,30,1.5); tap(60,30,1.5)
tap(128,150,1.5); tap(128,150,1.5)
tap(55,98,2.0); tap(55,98,2.0)
btn("a",1.5); e.screenshot(f"{OUTDIR}/kr_a.png")
tap(128,110,1.5); e.screenshot(f"{OUTDIR}/kr_b.png")
btn("a",1.5); e.screenshot(f"{OUTDIR}/kr_c.png")
tap(190,160,1.5); e.screenshot(f"{OUTDIR}/kr_d.png")
btn("a",2.2); e.screenshot(f"{OUTDIR}/kr_e.png")
adv(1.5); e.screenshot(f"{OUTDIR}/kr_f.png")
print("shots kr_a..kr_f saved")
e.close(); print("DONE")
