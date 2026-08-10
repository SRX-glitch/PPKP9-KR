#!/usr/bin/env python3
"""Decode Power Pro Kun Pocket (Poke3+) text using char tables from PokeTEXT.
Encoding: 0x00 sep; 0x01-0xE7 -> t1[b] (1-based); 0xE8-0xF7 -> t[b-230][nextb] (0-based)."""
import sys, re

CS=sys.argv[1]; DUMP=sys.argv[2]; OUT=sys.argv[3] if len(sys.argv)>3 else None

# --- line-based table extraction from the poke3 method ---
lines=open(CS,encoding="utf-8").read().splitlines()
in_poke3=False
tables={}   # idx -> list of variant strings (in order)
def unesc(s):
    return re.sub(r'\\u([0-9a-fA-F]{4})', lambda x: chr(int(x.group(1),16)), s)
for ln in lines:
    if "ポケ3以降の文字コード変換処理" in ln: in_poke3=True
    if in_poke3 and "ポケ1と2" in ln: pass
    m=re.search(r'array4\[(\d+)\]\s*=\s*"(.*)";\s*$', ln)
    if m and in_poke3:
        idx=int(m.group(1)); s=unesc(m.group(2))
        tables.setdefault(idx,[]).append(s)
# pick variants: base table1 -> the 5-16 version (index 1 in list if present else first)
def pick(idx, which=0):
    v=tables.get(idx,[])
    return v[which] if which<len(v) else (v[0] if v else "")
T={}
T[1]=pick(1,1) if len(tables.get(1,[]))>1 else pick(1,0)  # 5-16 variant
for i in range(2,18):
    T[i]=pick(i,0)
print("tables:", {i:len(T[i]) for i in sorted(T) if T[i]})

def ch1(b):
    t=T[1]; return t[b-1] if 1<=b<=len(t) else "?"
def ch2(b1,b2):
    t=T.get(b1-230,""); return t[b2] if t and 0<=b2<len(t) else "?"

def decode_run(buf,i,maxlen=400):
    out=[]; n=len(buf)
    while i<n and len(out)<maxlen:
        b=buf[i]
        if b==0: break
        if 1<=b<=231: out.append(ch1(b)); i+=1
        elif 232<=b<=247:
            if i+1>=n: break
            out.append(ch2(b,buf[i+1])); i+=2
        else: break
    return "".join(out), i

KANA=re.compile(r'[぀-ヿ]')      # hiragana+katakana (strongest signal)
JPALL=re.compile(r'[぀-ヿ㐀-鿿]')
def good(s):
    if len(s)<4: return False
    if "?" in s: return False
    kana=len(KANA.findall(s)); jp=len(JPALL.findall(s))
    return kana>=2 and jp>=len(s)*0.7

buf=open(DUMP,"rb").read()
results=[]; i=0
while i<len(buf):
    b=buf[i]
    if 1<=b<=247:
        s,j=decode_run(buf,i)
        if good(s):
            results.append((i,s)); i=max(j,i+1); continue
    i+=1
seen=set(); uniq=[]
for off,s in results:
    if s not in seen: seen.add(s); uniq.append((off,s))
# surface the longest coherent runs (real sentences), not kana noise
uniq_bylen=sorted(uniq,key=lambda x:-len(x[1]))
print(f"=== {len(uniq)} unique runs; longest lengths: {[len(s) for _,s in uniq_bylen[:15]]}")
if OUT:
    with open(OUT,"w",encoding="utf-8") as f:
        for off,s in uniq_bylen: f.write(f"0x{off:06X}\t({len(s)})\t{s}\n")
    print("wrote",OUT, f"({len(uniq)} runs), sorted by length")
