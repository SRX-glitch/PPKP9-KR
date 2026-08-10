#!/usr/bin/env python3
"""Search the ROM for chunks of the runtime source buffer (srcbuf.bin) to learn
whether the bottom-screen font/graphics are stored uncompressed (patchable) or
compressed. Reports which srcbuf regions appear verbatim in the ROM and where."""
import sys, os
ROM=sys.argv[1]
BUF=sys.argv[2] if len(sys.argv)>2 else os.path.join(os.path.dirname(__file__),"..","survey","srcbuf.bin")
rom=open(ROM,"rb").read()
buf=open(BUF,"rb").read()
print(f"rom={len(rom)} buf={len(buf)}")

# take non-trivial 32-byte chunks from buf, search rom
found=0; checked=0
hits=[]
for off in range(0, len(buf)-32, 64):
    chunk=buf[off:off+32]
    # skip low-entropy chunks (all same byte / mostly zero)
    if len(set(chunk))<6: continue
    checked+=1
    idx=rom.find(chunk)
    if idx>=0:
        hits.append((off,idx))
        found+=1
        if found<=25:
            print(f"  buf@0x{off:X} -> ROM 0x{idx:X}")
print(f"checked {checked} chunks, {found} found verbatim in ROM")
if found:
    # cluster ROM hit locations
    rl=sorted(set(h[1] for h in hits))
    print("ROM hit span:", hex(rl[0]), "..", hex(rl[-1]), f"({len(rl)} distinct)")
else:
    print("=> buffer content NOT verbatim in ROM: font/graphics are COMPRESSED or assembled at runtime.")
