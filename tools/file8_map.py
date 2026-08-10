# -*- coding: utf-8 -*-
"""파일 8(오버레이 23)의 포인터 배열과 레코드 구조를 지도로 만든다.

왜 필요한가
-----------
파일 8 은 이 프로젝트에서 **가장 위험한 파일**이다. 세션29 의 세이브 파손이 여기 아니면
파일 20 이었고(끝내 특정 못 함), 세션35 는 「시나리오가 시작 안 된다」로 두 출하 경로를
함께 껐으며, 세션41 의 `PPKP9_TAIL_RUNS=8` 은 **프롤로그 고착**을 만들었다.
그때마다 대응은 「끄기」였고 구조는 한 번도 지도화되지 않았다.

그런데 남은 번역의 상당수가 이 파일에 있다 — 변동 메시지의 인물명(치요·타케미·이오리·
타카코)이 대표다. 그것들은 원문보다 한국어가 길어 인라인이 불가능하고, 리다이렉트는
위 사고들 때문에 막혀 있다. **구조를 알아야 안전한 경로가 열린다.**

실측(세션43, 원본 ROM)
----------------------
    파일 8 = ROM 0x443200~0x4549A0 (71,584B) = 오버레이 23 @RAM 0x021992C0
    오버레이 내부를 가리키는 정렬 u32 : 4,448개
    길이 4 이상 연속 = 포인터 배열     : 98개 / 4,353 엔트리
    포인터가 가리키는 레코드 시작점    : 3,637개

⭐ 가장 큰 배열(812엔트리 @0x44AE8C)은 **텍스트가 아니라 에셋 경로**다
   (`/FsBin/…/….bin`, 디코드하면 「…んツノホ」로 끝난다). 여기에 텍스트를 쓰면 게임이
   없는 파일을 찾는다 — 세션29 세이브 파손의 유력 후보이며, 어떤 경로로도 건드리면 안 된다.

⭐ 변동 메시지의 인물명 레코드는 **전부 포인터 1개씩 갖는다**:
       ちよ 0x44E3C0 · 武美 0x44E3D0 · 維織 0x44E3E8 · 貴子 0x44E400
       夏菜 0x44E418 · 奈津姫 0x44E448 · ハンサム 0x44E7C0 · パワー 0x44E4E0
   ⇒ 레코드를 오버레이 꼬리로 옮기고 그 포인터 하나만 재기록하면 길이 제약이 사라진다.
     인물사전 452레코드에서 이미 검증된 방식(`insert_profiles`)과 같은 구조이고,
     스크립트에 이스케이프를 심는 v179 방식(고착의 원인)과는 다른 경로다.

    python tools/file8_map.py            # 요약
    python tools/file8_map.py --arrays   # 배열 98개 전수
    python tools/file8_map.py --json out.json
"""
import argparse
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import expand_overlay as XO
import poketbl as P

ORIG = (r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/"
        r"Power Pro Kun Pocket 9 (Japan).nds")
FID = 8


def _span(rom, fid):
    fat = int.from_bytes(rom[0x48:0x4C], "little")
    return (int.from_bytes(rom[fat + fid * 8:fat + fid * 8 + 4], "little"),
            int.from_bytes(rom[fat + fid * 8 + 4:fat + fid * 8 + 8], "little"))


def _decode(rom, off, limit=48):
    """오프셋에서 텍스트를 디코드한다(글자가 아니면 즉시 중단)."""
    out, i = [], off
    while i < off + limit:
        c = rom[i]
        if c == 0 or c >= 0xF8:
            break
        cc, nxt = P.bytes_to_cc(rom, i)
        ch = P.CC2CH.get(cc)
        if ch is None:
            break
        out.append(ch)
        i = nxt
    return "".join(out)


def classify(rom, tgt):
    """포인터가 가리키는 것이 무엇인가.

    ⛔ `asset` 은 절대 건드리지 않는다. ASCII 경로가 이 코덱을 지나면
    「…んツノホ」(= `.bin`)로 끝나므로 그 꼬리로 판정한다 — `walk_file.looks_like_text`
    가 쓰는 것과 같은 신호다.
    """
    if rom[tgt] == 0xF8:
        sub = rom[tgt + 1]
        if sub == 0x5A:
            return "record(F85A)"
        if sub == 0x08:
            return "record(F808)"
        return f"record(F8{sub:02X})"
    t = _decode(rom, tgt)
    if t.endswith("ツノホ"):
        return "asset(.bin)"
    if not t:
        return "binary"
    jp = sum(1 for ch in t if 0x3040 <= ord(ch) <= 0x30FF or 0x4E00 <= ord(ch) <= 0x9FFF)
    # 진짜 문장은 가나·한자 밀도가 높다. 이진 데이터도 디코드는 되지만 밀도가 낮다.
    return "text" if len(t) >= 2 and jp / len(t) >= 0.6 else "binary"


def arrays(rom=None):
    """[(start, entries, {분류: 개수})] — 길이 4 이상의 포인터 배열."""
    if rom is None:
        rom = open(ORIG, "rb").read()
    lo, hi = _span(rom, FID)
    info = XO.overlay_of_file(rom, FID)
    ram, size = info[2], info[3]
    ptr = [a for a in range(lo, hi - 3, 4)
           if ram <= int.from_bytes(rom[a:a + 4], "little") < ram + size]
    runs = []
    for a in ptr:
        if runs and a == runs[-1][1] + 4:
            runs[-1][1] = a
        else:
            runs.append([a, a])
    out = []
    for s, e in runs:
        n = (e - s) // 4 + 1
        if n < 4:
            continue
        kinds = collections.Counter()
        for k in range(n):
            v = int.from_bytes(rom[s + k * 4:s + k * 4 + 4], "little")
            kinds[classify(rom, lo + (v - ram))] += 1
        out.append((s, n, dict(kinds)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arrays", action="store_true")
    ap.add_argument("--json")
    a = ap.parse_args()
    rom = open(ORIG, "rb").read()
    lo, hi = _span(rom, FID)
    arr = arrays(rom)
    agg = collections.Counter()
    for _s, _n, k in arr:
        agg.update(k)
    print(f"file {FID}: ROM {lo:#x}~{hi:#x} ({hi - lo:,}B)")
    print(f"포인터 배열 {len(arr)}개 / {sum(n for _s, n, _k in arr):,} 엔트리")
    for k, v in agg.most_common():
        print(f"  {k:16s} {v:5,}")
    asset = [(s, n) for s, n, k in arr if k.get("asset(.bin)", 0) / n > 0.5]
    print(f"\n⛔ 에셋 경로 배열 {len(asset)}개 — 어떤 경로로도 쓰기 금지:")
    for s, n in sorted(asset, key=lambda x: -x[1])[:10]:
        print(f"   {s:#x}  {n:5d} 엔트리")
    if a.arrays:
        print("\n전체 배열:")
        for s, n, k in sorted(arr, key=lambda x: -x[1]):
            print(f"   {s:#x}  {n:5d}  {k}")
    if a.json:
        json.dump([{"start": s, "entries": n, "kinds": k} for s, n, k in arr],
                  open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"wrote {a.json}")


if __name__ == "__main__":
    main()
