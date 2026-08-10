# -*- coding: utf-8 -*-
"""번역은 이미 있는데 «그 자리를 아는 워크리스트가 없는» 런을 전수로 뽑는다.

왜 필요한가
-----------
사용자가 첫 경기까지 직접 진행하며 보낸 스크린샷에서 미번역 줄이 여럿 나왔는데,
확인해 보니 **번역이 없는 게 아니라 그 자리가 어느 워크리스트에도 없는** 경우가 많다.
대표 사례(세션43):

    file25_extra.tsv 0x4CE940 「治療が」   -> 치료        ✅ 있다
    file25_extra.tsv 0x4CE946 「上手くいった！」 -> 잘 됐다！   ✅ 있다(성공 문구)
    ROM      0x4CE963 「上手くいかなかった！」            ⛔ 없다(실패 문구)
                      batch148 에 「잘 안 됐다！」로 번역돼 있는데도.

⇒ 화면에는 「치료 上手くいかなかった！」처럼 반쪽으로 나온다.

같은 계열의 앞선 사고들: 세션30 인트로 111줄, 세션35 선택지 386/512, 세션38 공용 텍스트
2,858곳, 세션43 バンザイ·体力. **매번 「번역이 없다」가 아니라 「추출이 없다」였다.**

⛔ `dialogue_runs.tsv` 는 `F8 6B` 게이트라 `F8 5A`/`FA`/`FC` 로 도입되는 런을 통째로
   빠뜨린다(실측: 오프셋 0x2632 다음이 0x3148 — 그 사이 0xB16 바이트가 공백).
   `file*_extra.tsv` 가 그 자리를 담당하는데, 거기서도 빠진 것이 이 도구가 찾는 대상이다.

    python tools/missing_sites.py            # 파일별 요약
    python tools/missing_sites.py --fid 25   # 한 파일 전수
    python tools/missing_sites.py --tsv out.tsv   # 워크리스트에 붙일 형식으로
"""
import argparse
import collections
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import insert_extra as IX
import poketbl as P
import walk_file as W

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = (4, 8, 13, 18, 20, 25, 27, 30)


def corpus():
    """{일본어: 한국어} — 배치 코퍼스 + 모든 워크리스트의 번역."""
    out = {}
    tdir = os.path.join(BASE, "translation")
    names = sorted(glob.glob(tdir + "/batch*.tsv"),
                   key=lambda p: int(re.search(r"batch(\d+)\.tsv$", p).group(1)))
    for p in [os.path.join(tdir, "common_lines.tsv")] + names:
        try:
            rows = open(p, encoding="utf-8").read().splitlines()[1:]
        except OSError:
            continue
        for ln in rows:
            f = ln.split("\t")
            if len(f) >= 2 and f[0].strip() and f[1].strip():
                out[f[0].strip()] = f[1].strip()
    for p in glob.glob(os.path.join(BASE, "survey", "common", "file*_runs.tsv")):
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            f = ln.split("\t")
            if len(f) >= 4 and f[3].strip():
                out.setdefault(f[2], f[3].strip())
    return out


def known(fid):
    """이 파일에서 «이미 자리를 아는» 오프셋.

    ⛔ `rows()`(워크리스트 행)가 아니라 **`WORK()`(=`sites()`, 모든 출현)** 이 정본이다.
    세션38 이후 인서터는 같은 문자열의 모든 출현에 쓰므로, 워크리스트 행만 「안다」고
    치면 이미 출하되는 자리까지 «누락»으로 보고한다(실측 33,127 → 대부분 오탐).
    """
    out = {off for off, _b, _jp, _ko in IX.WORK(fid)}
    # ⛔ 파일 25 = 오버레이 28. 그 대사는 `insert_extra` 가 아니라 `build_kr` 이
    # `survey/ov28/dialogue_runs.tsv`(+`extract_names`)로 직접 쓴다. 이걸 빼면
    # 이미 출하되는 23,541곳이 「누락」으로 잡힌다.
    if fid == 25:
        lo = IX._fat_lo(open(IX.ORIG, "rb").read(), 25)
        p = os.path.join(BASE, "survey", "ov28", "dialogue_runs.tsv")
        for ln in open(p, encoding="utf-8").read().splitlines():
            f = ln.split("\t")
            if len(f) >= 4:
                try:
                    out.add(lo + int(f[0], 16))
                except ValueError:
                    pass
        try:
            import extract_names as EN
            out |= {lo + o for o, _b, _t in EN.runs()}
        except Exception:
            pass
    return out


def scan(rom, fid, tr):
    """[(offset, budget, jp, ko)] — 번역이 있는데 워크리스트에 없는 런."""
    lo, hi = W.fat_span(rom, fid)
    have = known(fid)
    out = []
    for _tag, off, blen, t in W.walk(rom, lo, hi):
        if off in have:
            continue
        ko = tr.get(t)
        if ko is None:
            continue
        # ⛔ 오프코드 바이트를 건드리는 자리는 제외 — 세션43의 마커 위 쓰기 사고
        if IX.hits_opcode(fid, off, blen):
            continue
        out.append((off, blen, t, ko))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fid", type=int)
    ap.add_argument("--tsv")
    a = ap.parse_args()
    rom = open(IX.ORIG, "rb").read()
    tr = corpus()
    fids = (a.fid,) if a.fid else FILES
    total, rows = 0, []
    for fid in fids:
        try:
            got = scan(rom, fid, tr)
        except Exception as e:
            print(f"file{fid}: skip ({e})")
            continue
        total += len(got)
        rows += [(fid,) + r for r in got]
        if got:
            print(f"file{fid}: {len(got)}곳")
            for off, blen, jp, ko in got[:6]:
                print(f"   {off:#08x} b{blen}  {jp!r} -> {ko!r}")
    print(f"\n번역은 있는데 자리를 모르는 런: 총 {total}곳")
    if a.tsv:
        by = collections.defaultdict(list)
        for fid, off, blen, jp, ko in rows:
            by[fid].append((off, blen, jp, ko))
        with open(a.tsv, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("fid\toffset\tbudget\topcode\toccurrences\tjp\tko\n")
            for fid in sorted(by):
                for off, blen, jp, ko in sorted(by[fid]):
                    fh.write(f"{fid}\t0x{off:06X}\t{blen}\tF85A\t1\t{jp}\t{ko}\n")
        print(f"wrote {a.tsv}")


if __name__ == "__main__":
    main()
