# -*- coding: utf-8 -*-
"""이름 삽입 오프코드 직후에 남는 «조사만으로 이뤄진 런»을 뽑는다.

왜 필요한가
-----------
「우리빅토리즈 **は**」「곤타（곤다）**だ、**」처럼 한국어 문장 안에 일본어 조사가
남는 자리의 정체다. 세션41이 원인을 `walk_file.py:132` 의 `len(t) >= 2` 필터로
지목했고(1글자 런이 통째로 버려진다), 세션43이 그 모집단을 실측했다.

⛔ 필터를 전역으로 낮추면 노이즈가 폭증한다(1~2글자 런 3,272개 중 대부분이
「・」 반복이나 표 데이터의 한자 2글자다). 그래서 두 조건을 함께 건다:
  ① 직전 오프코드가 이름 삽입 계열(F8 08/09/17/29)
  ② 런이 조사·어미·구두점만으로 이뤄짐
실측(2026-08-09, 정본 폭 표): **923 사이트** — f4 415 · f25 390 · f27 83 · f30 24 ·
f8 8 · f18 3.

한국어 조사 결정
----------------
사용자 결정(세션43) = **받침 판정 훅**. 은/는·이/가는 앞 음절의 받침에 따라
달라지는데 이름이 런타임에 들어오므로 정적으로 못 고른다. 렌더 시점에 직전
음절의 charcode -> 한글 음절 -> 받침 유무를 보고 두 형태 중 하나를 그린다.
`tools/josa_audit.py` 에 판정 로직이 이미 있다.

    python tools/particle_sites.py            # 요약
    python tools/particle_sites.py --tsv out.tsv
"""
import argparse
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.path.join(BASE, "..", "Power Pro Kun Pocket 9 (Japan).nds")
WIDTHS = os.path.join(BASE, "survey", "ov28", "opcode_lengths.json")
FILES = (4, 8, 18, 20, 25, 27, 30)

# 이름/객체 삽입 계열. F8 08..09 = 이름 삽입 열기/닫기, F8 17 = 객체 이름 인덱스,
# F8 29 = 화자 지정(런타임 계측으로 폭 3 확정).
# ⭐ F8 07 = 스탯 이름 삽입. 세션43에 사용자가 「パワーが ５감소」를 지적해 찾았다 —
# 상태 증감 줄은 `<F807 인덱스> 「が」 <F86A 숫자> 「上がった/下がった」` 로 조립되고,
# 그 「が」의 도입 오프코드가 08/09/17/29 가 아니라 07 이라 처음 스캔이 통째로 놓쳤다.
NAME_OPS = {0x07, 0x08, 0x09, 0x17, 0x29}
PARTICLES = set("はがをにでとものやへねよかなだ")
PUNCT = set("、。！？「」（）")


def sites(rom=None):
    """[(fid, offset, byte_len, text)] — 이름 삽입 직후의 조사 전용 런."""
    if rom is None:
        rom = open(ORIG, "rb").read()
    L = json.load(open(WIDTHS))
    bare = {int(k): v for k, v in L["bare"].items()}
    f8 = {int(k): v for k, v in L["f8"].items() if v}
    fat = int.from_bytes(rom[0x48:0x4C], "little")
    out = []
    for fid in FILES:
        lo = int.from_bytes(rom[fat + fid * 8:fat + fid * 8 + 4], "little")
        hi = int.from_bytes(rom[fat + fid * 8 + 4:fat + fid * 8 + 8], "little")
        i, last = lo, None
        while i < hi - 1:
            b = rom[i]
            if b == 0:
                i += 1
                last = None
                continue
            if b >= 0xF8:
                if b == 0xF8:
                    last = rom[i + 1]
                    i += f8.get(rom[i + 1], 2)
                else:
                    last = None
                    i += bare.get(b, 1)
                continue
            st, chars = i, []
            while i < hi:
                c = rom[i]
                if c == 0 or c >= 0xF8:
                    break
                cc, nxt = P.bytes_to_cc(rom, i)
                ch = P.CC2CH.get(cc)
                if ch is None:
                    break
                chars.append(ch)
                i = nxt
            t = "".join(chars)
            if (last in NAME_OPS and 1 <= len(t) <= 3 and t
                    and all(ch in PARTICLES or ch in PUNCT for ch in t)):
                out.append((fid, st, i - st, t))
            if i == st:
                i += 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsv")
    a = ap.parse_args()
    rows = sites()
    per = collections.Counter(f for f, _o, _b, _t in rows)
    kinds = collections.Counter(t for _f, _o, _b, t in rows)
    print(f"particle-only runs after a name insert: {len(rows)}")
    print("  by file:", dict(sorted(per.items())))
    print("  most common:", kinds.most_common(12))
    if a.tsv:
        with open(a.tsv, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("fid\toffset\tbudget\tjp\tko\n")
            for fid, off, blen, t in rows:
                fh.write(f"{fid}\t0x{off:06X}\t{blen}\t{t}\t\n")
        print(f"wrote {a.tsv}")


if __name__ == "__main__":
    main()
