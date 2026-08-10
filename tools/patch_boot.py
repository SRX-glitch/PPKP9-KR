#!/usr/bin/env python3
"""PERSISTENT patch PoC: write Hangul 16x16 glyph tiles directly into a copy of
the .nds at the uncompressed font ROM region (0xBAA000, confirmed to feed the
name-entry screen), then boot that patched ROM fresh and navigate to the keyboard
to show the Hangul rendering from ROM (no live injection)."""
import sys, time, shutil
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR

PATCHED="/root/ppkp9_patched.nds"

GA16=[
 "0000000000000000","0000000000011000","0011111111011000","0000000011011000",
 "0000000011011000","0000000011011000","0000000011011000","0000000011011110",
 "0000000011011110","0000000011011000","0000000000011000","0000000000011000",
 "0000000000011000","0000000000011000","0000000000011000","0000000000000000"]
def tile(rows,r0,c0,ink=0xF):
    out=bytearray()
    for ry in range(8):
        row=rows[r0+ry]
        for bx in range(4):
            c=c0+bx*2
            p0=ink if row[c]=="1" else 0; p1=ink if row[c+1]=="1" else 0
            out.append(p0|(p1<<4))
    return bytes(out)
TL=tile(GA16,0,0);TR=tile(GA16,0,8);BL=tile(GA16,8,0);BR=tile(GA16,8,8)
META=TL+TR+BL+BR   # 128 bytes

# 1) build patched rom
shutil.copyfile(ROM, PATCHED)
d=bytearray(open(PATCHED,"rb").read())
start=0xBAA000; end=0xBAD000
off=start
while off<end:
    d[off:off+128]=META; off+=128
open(PATCHED,"wb").write(d)
print(f"patched {hex(start)}..{hex(end)} with 가 metatiles -> {PATCHED}")

# 2) boot patched rom fresh and navigate to keyboard
e=Emucap()
e.call("bootstrap",{},30)
print("launch:", e.call("launch",{"content_path":PATCHED,"system":"nds","name":"ppkp9p"},120)["text"][:80])
def adv(w=1.3):
    e.call("resume",{},30); time.sleep(w); e.call("pause",{},30)
def tap(x,y,w=1.4):
    e.call("touch",{"x":x,"y":y,"frames":8},30); adv(w)
def btn(b,w=1.4):
    e.call("press_buttons",{"buttons":[b],"frames":8},30); adv(w)
# boot to title/menu
for i in range(7):
    adv(1.3)
    if i%2==0: e.call("press_buttons",{"buttons":["start"],"frames":4},30)
tap(128,96,2.0); tap(128,96,1.5)      # title -> mode menu
tap(60,30,1.5); tap(60,30,1.5)        # サクセス
tap(128,150,1.5); tap(128,150,1.5)    # -> scenario select
tap(55,98,2.0); tap(55,98,2.0)        # select scenario
btn("a",1.5); tap(128,110,1.5); btn("a",1.5); tap(190,160,1.5); btn("a",2.0)  # -> keyboard
e.screenshot(f"{OUTDIR}/patched_kbd.png")
print("screenshot patched_kbd.png")
e.close(); print("DONE")
