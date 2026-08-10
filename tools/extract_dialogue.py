#!/usr/bin/env python3
"""Filter the decoded RAM text runs down to real dialogue lines and save a clean
corpus. Dialogue = has hiragana + punctuation, coherent (low garbage)."""
import sys, re
IN=sys.argv[1]; OUT=sys.argv[2]
HIRA=re.compile(r'[ぁ-ん]')
KANJI=re.compile(r'[一-鿿]')
# garbage markers: interleaved index artifacts (katakana single between kanji), replacement
PUNC=set("、。！？「」（）…～")
def repetitive(s):
    # reject runs dominated by one repeating bigram (BG maps / index tables)
    if len(s)<8: return False
    bg={}
    for i in range(len(s)-1):
        k=s[i:i+2]; bg[k]=bg.get(k,0)+1
    top=max(bg.values())
    # unique-char ratio low OR one bigram covers a big share = repetitive
    return top > len(s)*0.15 or len(set(s))/len(s) < 0.30
WORDS=["った","ない","って","んだ","する","した","いる","ある","です","ます","だな","だよ",
 "けど","から","ので","のに","こと","もの","れる","られ","せる","でも","いう","思","言",
 "見て","来て","行","なる","わけ","かな","でしょ","だろ","ちゃん","くん","さん","たち",
 "じゃ"," than","なん","どう","この","その","あの","ここ","よう","たい","ください","おれ","オレ","ボク","きみ"]
def score(s):
    if len(s)<6: return 0
    if repetitive(s): return 0
    if "?" in s: return 0
    h=len(HIRA.findall(s))
    if h<4 or h/len(s)<0.4: return 0
    kata=len(re.findall(r'[ァ-ヴ]',s))
    if kata/max(1,len(s))>0.25: return 0
    # require real Japanese words -> rejects random-char garbage
    hits=sum(1 for w in WORDS if w in s)
    if hits<2: return 0
    p=sum(1 for c in s if c in PUNC)
    return h + hits*6 + p*3 + (len(s)>15)*4

rows=[]
for ln in open(IN,encoding="utf-8"):
    parts=ln.rstrip("\n").split("\t")
    if len(parts)<3: continue
    off,_,s=parts[0],parts[1],parts[2]
    sc=score(s)
    if sc>=12: rows.append((sc,off,s))
rows.sort(reverse=True)
seen=set(); uniq=[]
for sc,off,s in rows:
    key=s.strip()
    if key in seen: continue
    seen.add(key); uniq.append((off,s))
with open(OUT,"w",encoding="utf-8") as f:
    for off,s in uniq: f.write(f"{off}\t{s}\n")
print(f"extracted {len(uniq)} clean dialogue lines -> {OUT}")
# print length stats + a few via ascii-safe (write only)
tot=sum(len(s) for _,s in uniq)
print(f"total chars: {tot}")
