#!/usr/bin/env python3
"""Produce a clean, deduplicated, story-ordered dialogue list from the decoded RAM
text: strip control-code prefixes, require real JP words, dedupe, sort by offset."""
import sys, re
IN=sys.argv[1]; OUT=sys.argv[2]
HIRA=re.compile(r'[ぁ-ん]')
WORDS=["った","ない","って","んだ","する","した","いる","ある","です","ます","だな","だよ",
 "けど","から","ので","のに","こと","もの","れる","られ","せる","でも","いう","思","言",
 "見て","来て","行","なる","わけ","かな","でしょ","だろ","ちゃん","くん","さん","たち",
 "じゃ","なん","どう","この","その","あの","ここ","よう","たい","くれ","おれ","オレ","ボク","きみ","だ。","た。","よ。","ね。","か？"]
# leading control-code prefixes commonly seen (decoder artifacts): [ヒえいうデえボ] + small kana
PREFIX=re.compile(r'^(?:[ヒえいうデボネクバ][ぁ-んァ-ン]){1,2}')
def repetitive(s):
    if len(s)<8: return False
    bg={}
    for i in range(len(s)-1): bg[s[i:i+2]]=bg.get(s[i:i+2],0)+1
    return max(bg.values())>len(s)*0.15 or len(set(s))/len(s)<0.30
def clean(s):
    s=s.strip()
    s=PREFIX.sub("",s)          # drop leading control code
    s=s.strip("　 ")
    return s
BAD=set("㎏㎞％￥♂♀◎★→←↑↓○●＠＋◇◆□■△▲▼※〒♯♭♪♫✛☆✉")
def ok(s):
    if len(s)<6 or repetitive(s) or "?" in s: return False
    if sum(1 for c in s if c in BAD)>0: return False        # UI/control symbols -> not prose
    if s.count("（")+s.count("）")+s.count("(")+s.count(")")>0: return False
    h=len(HIRA.findall(s))
    if h<4 or h/len(s)<0.5: return False
    if len(re.findall(r'[ァ-ヴ]',s))/max(1,len(s))>0.25: return False
    # allowed chars = JP + basic punctuation; reject if too many "other"
    other=len(re.findall(r'[^ぁ-んァ-ンー一-鿿、。！？「」『』…～・　]',s))
    if other>len(s)*0.08: return False
    return sum(1 for w in WORDS if w in s)>=2

rows=[]
for ln in open(IN,encoding="utf-8"):
    p=ln.rstrip("\n").split("\t")
    if len(p)<3: continue
    off=int(p[0],16); s=clean(p[2])
    if ok(s): rows.append((off,s))
rows.sort()
seen=set(); uniq=[]
for off,s in rows:
    if s in seen: continue
    seen.add(s); uniq.append((off,s))
with open(OUT,"w",encoding="utf-8") as f:
    for off,s in uniq: f.write(f"0x{off:06X}\t{s}\n")
print(f"clean unique dialogue lines: {len(uniq)}  chars: {sum(len(s) for _,s in uniq)}")
