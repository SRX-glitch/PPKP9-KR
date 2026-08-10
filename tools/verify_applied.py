#!/usr/bin/env python3
"""Prove that a named set of translation changes is really in a built ROM.

"I edited the worklist and then rebuilt" is not evidence -- a worklist row can be
dropped for being over budget, filtered out of a SHIP list, or shadowed by a
duplicate. This searches the built ROM for the actual bytes.

Two encodings are tried for each string, because build_kr may have used either:
the MTE-compressed form (`kr_map.json`) or the plain per-charcode form. A line
that was redirected lives in the grown region rather than inline, and searching
the whole file finds it either way.

    python tools/verify_applied.py [rom]
"""
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import koenc

BASE = r"C:/Users/jngji/Desktop/실험실"
ROM = sys.argv[1] if len(sys.argv) > 1 else BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/builds/PPKP9_mte.nds"
KR = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font/kr_map.json"
INTRO = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/translation/intro_lines.tsv"

# (group, japanese-or-label, korean that must be present)
CHECKS = [
    ("고유명사", "デスパレス", "데스팰리스"),
    ("고유명사", "ルナリング", "루나링"),
    ("고유명사", "大村", "오무라"),
    ("고유명사", "レガタ", "레가타"),
    ("고유명사", "カンタ", "칸타"),
    ("오프닝 다듬기", "おいおい・・・", "어이어이・・・"),
    ("오프닝 다듬기", "やっちまえ！", "쳐라！"),
    ("오프닝 다듬기", "なんだと", "뭐라고"),
    ("오프닝 다듬기", "ぼうやじゃなくて", "꼬마 아니야"),
    ("오프닝 다듬기", "おじさんは…", "아저씨 배가 너무 고프다。"),
    ("오프닝 다듬기", "そして、戦争と…", "그리고 전쟁과 혼란을 거쳐"),
    ("오프닝 다듬기", "今、宇宙には", "우주엔"),
    ("오프닝 다듬기", "「わかった。」", "「알았다。」"),
    ("오프닝 다듬기", "「さあな。", "「글쎄다。"),
    ("어미 でやんす", "オイラ知らないでやんす！", "모르겠습죠！"),
    ("어미 でやんす", "オイラ知ってるでやんす！", "다 알고있습죠"),
    ("어미 でやんす", "カレー屋でやんす！", "우린 카레집입죠！"),
    ("어미 でやんす", "すごいでやんす！", "아저씨、대단합죠！"),
    ("어미 ですぞ", "これを食べるといいですぞ。", "이걸 드시면 좋소。"),
    ("어미 ですぞ", "料理のレシピは、秘密ですぞ？", "요리 레시피는、비밀이오？"),
    ("어미 ですぞ", "おいしいですぞ。", "맛있소。"),
    ("어미 ですぞ", "君もまだまだですぞ。", "자네도 아직 멀었소。"),
    ("어미 っす", "まだ、いるっすか？", "아직 있어요？"),
    ("어미 っす", "今日はどうするっすか？", "오늘은 어떻게 해요？"),
    ("어미 っす", "まじっすか！", "진짜？"),
    ("어미 っす", "おもしろそうじゃないっすか！", "재밌겠네요！"),
    ("어미 っす", "（オスッ！）", "（안녕！）"),
    ("짝 오류 수정", "ムシャぶるい", "무사떨림"),
    ("짝 오류 수정", "を選んで、", "을 골라서、"),
    ("짝 오류 수정", "バンザイメーター", "반자이 미터"),
    ("짝 오류 수정", "の長さに応じた期間", "의 길이에 따른 기간"),
    ("짝 오류 수정", "経営者に逆らったら", "경영자에게 반항하면"),
    ("짝 오류 수정", "かわいくて", "귀엽고"),
    ("짝 오류 수정", "に連れて行けば、", "에 넣으면、"),
    ("짝 오류 수정", "がとれる。", "을 잡을 수 있다。"),
    ("짝 오류 수정", "必要な", "필요한"),
    ("짝 오류 수정", "だったら・・・", "그렇다면・・・"),
]


def main():
    rom = open(ROM, "rb").read()
    m = json.load(open(KR, encoding="utf-8"))
    mte = koenc.Encoder(m)
    plain = koenc.Encoder({**m, "mte": {}})

    print(f"ROM: {os.path.basename(ROM)}  ({len(rom):,} B)\n")
    bad, group = 0, None
    for g, jp, ko in CHECKS:
        if g != group:
            print(f"[{g}]")
            group = g
        hit = ""
        for name, enc in (("mte", mte), ("plain", plain)):
            try:
                b = enc.encode(ko)
            except KeyError as e:
                hit = f"UNENCODABLE {e}"
                break
            if rom.find(b) >= 0:
                hit = f"ok ({name}, {len(b)}B)"
                break
        if not hit.startswith("ok"):
            bad += 1
            print(f"  ✗ {jp}  ->  {ko}   {hit or 'NOT FOUND IN ROM'}")
        else:
            print(f"  ✓ {ko!r:34} {hit}")

    # every intro line, decoded straight out of the built ROM at its own offset
    n = ok = 0
    for ln in open(INTRO, encoding="utf-8").read().splitlines()[1:]:
        p = ln.split("\t")
        if len(p) < 3 or not p[0].strip():
            continue
        off, ko = int(p[0], 16), p[2].strip()
        n += 1
        b = mte.encode(ko)
        if rom[off:off + len(b)] == b:
            ok += 1
        else:
            print(f"  ✗ intro 0x{off:06X} expected {ko!r}")
    print(f"\n[오프닝] {ok}/{n} lines byte-exact at their own ROM offsets")
    print(f"\n{len(CHECKS) - bad}/{len(CHECKS)} spot checks passed"
          f"{'' if not bad else f'  -- {bad} FAILED'}")
    return 1 if (bad or ok != n) else 0


if __name__ == "__main__":
    sys.exit(main())
