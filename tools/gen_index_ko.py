#!/usr/bin/env python3
"""Build Korean for the encyclopedia's `No NN  <label>` index records.

These are the lines beside the entry number on the top screen. They could never
be patched in place: the recorded offset lands on the SECOND byte of the `f7 68`
number glyph, so `insert_tables.verify_offset` refuses them (correctly -- writing
there wrecks the glyph). Through the pointer array the whole record is ours, so
the prefix and padding are preserved verbatim and only the label is replaced.

Most labels are already translated somewhere -- `file30_entries.tsv`,
`file30_album.tsv`, `file30_table.tsv` -- so they are reused rather than
retranslated, which is also what keeps the name spellings consistent. MANUAL
covers the rest.

    python tools/gen_index_ko.py      -> appends to translation/profiles_ko.tsv
"""
import io, os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMON = os.path.join(BASE, "survey", "common")
WORK = os.path.join(COMMON, "file30_profiles.tsv")
OUT = os.path.join(BASE, "translation", "profiles_ko.tsv")
NUL = "\\0"

MANUAL = {
    "ゲリラ": "게릴라", "最強の忍び": "최강의 닌자", "薬師": "약사",
    "格闘家": "격투가", "情報屋": "정보상", "議長": "의장",
    "宇宙三兄弟": "우주 삼형제", "秘密警察": "비밀경찰", "兵士": "병사",
    "海賊手下（リコの部下）": "해적 부하（리코의 부하）",
    "失業者": "실업자", "賞金首": "현상수배범", "忍者": "닌자",
    "ギャスビゴー星人": "갸스비고 성인", "ドマグニー人": "도마그니 인",
    "カニ人間": "게인간", "主人公（ミニ）": "주인공（미니）",
    "三田": "산다", "チャン太": "챤타", "六学院": "로쿠가쿠인",
    "進藤": "신도", "寺門": "지몬", "光山先輩": "미츠야마 선배",
    "松竹珍": "쇼치쿠친", "師匠": "스승", "同級生": "동급생",
    "主人公の母親": "주인공의 어머니",
    # ⚠ 제작중, not 작성중 -- 0x3248F4 already shipped 제작중 and two spellings
    # of the same placeholder land on the same screen.
    "作成中": "제작중",
}

PAT = re.compile(r"^(No(?:%s)\d+(?:%s)+)(.*?)((?:%s)*)$"
                 % (re.escape(NUL), re.escape(NUL), re.escape(NUL)))
STRIP = re.compile(r"^[^\d]*\d+\s*")          # drops the `No02` / `ネo103` prefix


def sources():
    d = {}
    for n in ("file30_entries.tsv", "file30_album.tsv", "file30_table.tsv"):
        p = os.path.join(COMMON, n)
        if not os.path.exists(p):
            continue
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            f = ln.split("\t")
            if len(f) >= 2 and f[-1].strip():
                d[f[-2]] = f[-1].strip()
    return d


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    src = sources()
    done = {ln.split("\t")[0].strip().upper()
            for ln in open(OUT, encoding="utf-8").read().splitlines()[1:]}
    out, miss = [], []
    for ln in open(WORK, encoding="utf-8").read().splitlines()[1:]:
        f = ln.split("\t")
        if len(f) > 5 and f[5].strip():
            continue
        if f[0].strip().upper() in done or not f[4].startswith("No"):
            continue
        m = PAT.match(f[4])
        if not m:
            continue
        pre, label, tail = m.groups()
        ko = src.get(f[4].replace(NUL, ""))
        ko = STRIP.sub("", ko) if ko else MANUAL.get(label)
        if not ko:
            miss.append(label)
            continue
        out.append(f"{f[0]}\t{pre}{ko}{tail}")

    with open(OUT, "a", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"appended {len(out)} index records to {os.path.basename(OUT)}")
    if miss:
        print(f"  {len(miss)} still without Korean: {sorted(set(miss))[:8]}")


if __name__ == "__main__":
    main()
