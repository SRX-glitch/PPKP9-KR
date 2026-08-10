#!/usr/bin/env python3
"""Reverse of pokedecode: build char->byte(s) maps from the tables and encode text
back to the game's byte stream. Round-trip validates against the RAM dump."""
import sys, re

CS=sys.argv[1]
def load_tables(cs):
    lines=open(cs,encoding="utf-8").read().splitlines()
    in3=False; tabs={}
    def unesc(s): return re.sub(r'\\u([0-9a-fA-F]{4})', lambda x: chr(int(x.group(1),16)), s)
    for ln in lines:
        if "ポケ3以降の文字コード変換処理" in ln: in3=True
        m=re.search(r'array4\[(\d+)\]\s*=\s*"(.*)";\s*$', ln)
        if m and in3:
            i=int(m.group(1)); tabs.setdefault(i,[]).append(unesc(m.group(2)))
    T={1: tabs[1][1] if len(tabs.get(1,[]))>1 else tabs[1][0]}
    for i in range(2,18): T[i]=tabs.get(i,[""])[0]
    return T

def build_maps(T):
    dec={}; enc={}
    for b in range(1,232):
        if b-1 < len(T[1]):
            c=T[1][b-1]; dec[bytes([b])]=c; enc.setdefault(c,bytes([b]))
    for tbl in range(2,18):
        t=T[tbl]; b1=230+tbl
        for idx in range(len(t)):
            c=t[idx]
            if c in ("　","？"): continue
            key=bytes([b1,idx]); dec[key]=c; enc.setdefault(c,key)
    return dec,enc

def decode(buf,enc=None,T=None):
    out=[]; i=0
    while i<len(buf):
        b=buf[i]
        if b==0: break
        if 1<=b<=231: out.append(T[1][b-1] if b-1<len(T[1]) else "?"); i+=1
        elif 232<=b<=247:
            if i+1>=len(buf): break
            t=T[b-230]; out.append(t[buf[i+1]] if buf[i+1]<len(t) else "?"); i+=2
        else: break
    return "".join(out)

def encode(s,enc):
    out=bytearray()
    for c in s:
        if c in enc: out+=enc[c]
        else: return None,c   # unencodable
    return bytes(out),None

if __name__=="__main__":
    T=load_tables(CS); dec,enc=build_maps(T)
    print(f"encode map: {len(enc)} chars")
    # round-trip test on some known JP strings from the corpus
    tests=["お疲れ様でした。","野球のことが載ってるぞ。","上手くいかなかった","追い込まれると弱くなります","他の星に行きます"]
    ok=0
    for n,s in enumerate(tests):
        b,bad=encode(s,enc)
        if b is None: print(f"  test{n}: FAIL enc (unencodable char U+{ord(bad):04X})"); continue
        back=decode(b,T=T)
        exact = back==s
        print(f"  test{n}: {len(s)}ch -> {len(b)}B {b.hex()} -> {'EXACT' if exact else 'MISMATCH'}")
        if exact: ok+=1
    print(f"round-trip: {ok}/{len(tests)} exact")
