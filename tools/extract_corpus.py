#!/usr/bin/env python3
"""Extract the Shift-JIS (cp932) script corpus from ARM9 + all overlays.
Estimates initial localization volume. Writes UTF-8 samples + stats. Read-only."""
import struct, sys, os, re, json

def u32(b,o): return struct.unpack_from("<I",b,o)[0]
JP = re.compile(r'[぀-ヿ一-鿿＀-￯]')
GAIJI = re.compile(r'[-]')

def extract(b):
    """yield (offset, text) for SJIS runs (0x00-terminated) with real JP content"""
    out=[]; i=0; n=len(b); start=0; cur=bytearray()
    def flush(start,cur):
        if len(cur)<4: return None
        try: s=cur.decode("cp932")
        except: return None
        if JP.search(s) and len([c for c in s if ord(c)>0x20])>=2:
            return s
        return None
    while i<n:
        c=b[i]
        if c==0 or (c<0x20 and c not in (0x0a,)):
            s=flush(start,cur)
            if s is not None: out.append((start,s))
            cur=bytearray(); i+=1; start=i; continue
        if not cur: start=i
        cur.append(c); i+=1
    return out

def main():
    rom=sys.argv[1]; outdir=sys.argv[2]
    os.makedirs(outdir,exist_ok=True)
    d=open(rom,"rb").read()
    arm9_off=u32(d,0x20); arm9_size=u32(d,0x2C)
    ov9_off=u32(d,0x50); ov9_size=u32(d,0x54); fat_off=u32(d,0x48)
    blobs=[("arm9", d[arm9_off:arm9_off+arm9_size])]
    for i in range(ov9_size//32):
        e=ov9_off+i*32; ovid=u32(d,e); fileid=u32(d,e+24)
        fs=u32(d,fat_off+fileid*8); fe=u32(d,fat_off+fileid*8+4)
        blobs.append((f"ov{ovid:02d}", d[fs:fe]))

    per={}; total_strings=0; total_jpchars=0; gaiji=set(); all_rows=[]
    for name,b in blobs:
        rows=extract(b)
        jpchars=sum(len(JP.findall(s)) for _,s in rows)
        for _,s in rows: gaiji.update(GAIJI.findall(s))
        per[name]={"strings":len(rows),"jp_chars":jpchars,"bytes":len(b)}
        total_strings+=len(rows); total_jpchars+=jpchars
        for off,s in rows: all_rows.append((name,off,s))

    # unique strings (dedupe repeated UI text)
    uniq=set(s for _,_,s in all_rows)
    stats={"total_strings":total_strings,"unique_strings":len(uniq),
           "total_jp_chars":total_jpchars,"gaiji_count":len(gaiji),
           "per_container":per}
    json.dump(stats, open(os.path.join(outdir,"corpus_stats.json"),"w",encoding="utf-8"),
              indent=2, ensure_ascii=False)
    # write full corpus (UTF-8) for inspection
    with open(os.path.join(outdir,"corpus.txt"),"w",encoding="utf-8") as f:
        for name,off,s in all_rows:
            f.write(f"[{name}:0x{off:06X}] {s}\n")
    # gaiji list
    with open(os.path.join(outdir,"gaiji.txt"),"w",encoding="utf-8") as f:
        for g in sorted(gaiji):
            f.write(f"U+{ord(g):04X}\n")

    print(f"TOTAL strings (SJIS w/ JP): {total_strings}")
    print(f"UNIQUE strings           : {len(uniq)}")
    print(f"TOTAL Japanese chars     : {total_jpchars}")
    print(f"Distinct gaiji (E000-F8FF): {len(gaiji)}")
    print("\nPer-container (top 12 by strings):")
    for name,st in sorted(per.items(),key=lambda x:-x[1]['strings'])[:12]:
        print(f"  {name:6} strings={st['strings']:6} jp_chars={st['jp_chars']:7} bytes={st['bytes']:8}")
    print(f"\nWrote {outdir}/corpus.txt, corpus_stats.json, gaiji.txt")

if __name__=="__main__":
    main()
