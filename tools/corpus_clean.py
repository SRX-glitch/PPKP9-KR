#!/usr/bin/env python3
import struct, re, sys, os
d=open(sys.argv[1],"rb").read()
outdir=sys.argv[2]; os.makedirs(outdir,exist_ok=True)
def u32(b,o): return struct.unpack_from("<I",b,o)[0]
ov9_off=u32(d,0x50); ov9_size=u32(d,0x54); fat_off=u32(d,0x48)
FW = re.compile(r'[぀-ヿ㐀-鿿]')   # full-width kana + kanji (excludes half-width katakana noise)
def run_ok(s):
    best=cur=0
    for ch in s:
        if FW.match(ch): cur+=1; best=max(best,cur)
        else: cur=0
    return best>=4
def extract(b):
    out=[];i=0;n=len(b);cur=bytearray();start=0
    while i<n:
        c=b[i]
        if c==0 or (c<0x20 and c!=0x0a):
            if len(cur)>=6:
                try:
                    s=cur.decode("cp932")
                    if run_ok(s): out.append((start,s))
                except: pass
            cur=bytearray();i+=1;start=i;continue
        if not cur:start=i
        cur.append(c);i+=1
    return out
containers=[("arm9",d[u32(d,0x20):u32(d,0x20)+u32(d,0x2C)])]
for i in range(ov9_size//32):
    e=ov9_off+i*32;ovid=u32(d,e);fid=u32(d,e+24)
    fs=u32(d,fat_off+fid*8);fe=u32(d,fat_off+fid*8+4)
    containers.append((f"ov{ovid:02d}",d[fs:fe]))
allrows=[];per={}
for name,b in containers:
    r=extract(b);per[name]=len(r)
    for off,s in r: allrows.append((name,off,s))
uniq=set(s for _,_,s in allrows)
tot_ch=sum(len(FW.findall(s)) for _,_,s in allrows)
with open(os.path.join(outdir,"corpus_clean.txt"),"w",encoding="utf-8") as f:
    for name,off,s in allrows: f.write(f"[{name}:0x{off:06X}] {s}\n")
print(f"CLEAN strings (>=4 consec full-width JP): {len(allrows)}")
print(f"UNIQUE: {len(uniq)}")
print(f"Full-width JP chars total: {tot_ch}")
print("top containers:")
for name,c in sorted(per.items(),key=lambda x:-x[1])[:12]:
    print(f"  {name}: {c}")
