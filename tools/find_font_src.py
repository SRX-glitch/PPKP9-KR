#!/usr/bin/env python3
"""Take real glyph tiles from the keyboard VRAM dump and find_pattern them in
live main RAM to locate the font SOURCE (which is DMA'd to VRAM each frame)."""
import sys, time
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
from emucap_drv import Emucap, ROM, OUTDIR
KBD="/root/ppkp9_kbd.dss"

vram=open(f"{OUTDIR}/kbd_subBG.bin","rb").read()
# collect mid-density 32-byte tiles (candidate glyphs) from the font band
cands=[]
for off in range(0x4000, min(len(vram),0x18000), 32):
    tile=vram[off:off+32]
    ink=sum(bin(b).count("1") for b in tile)/(32*8)
    if 0.12<ink<0.55:
        cands.append((off,tile))
print(f"candidate glyph tiles: {len(cands)}")

e=Emucap()
e.call("bootstrap",{},30)
if not (e.call("status",{},30)["json"] or {}).get("connected"):
    e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)
e.call("load_state",{"path":KBD},30)
e.call("resume",{},30); time.sleep(0.4); e.call("pause",{},30)

# probe find_pattern API once
r=e.call("find_pattern",{"memory_type":"main","hex":cands[0][1].hex()},40)
print("find_pattern sample reply:", r["text"][:200])

hits=[]
tested=0
import random
random.seed(1)
sample=cands[::max(1,len(cands)//40)][:40]
for off,tile in sample:
    r=e.call("find_pattern",{"memory_type":"main","hex":tile.hex()},40)
    j=r["json"]; txt=r["text"]
    tested+=1
    if j and (j.get("matches") or j.get("offsets") or j.get("addresses") or j.get("count")):
        hits.append((off,txt[:160]))
        print(f"VRAM off 0x{off:X} -> MATCH in main: {txt[:160]}")
print(f"tested {tested}, hits {len(hits)}")
# also try ARM9 bus (covers more) for one tile
r=e.call("find_pattern",{"memory_type":"arm9","hex":sample[0][1].hex()},40)
print("arm9 search sample:", r["text"][:160])
e.close(); print("DONE")
