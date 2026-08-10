# -*- coding: utf-8 -*-
"""워크리스트가 기록한 런 시작이 «오프코드의 피연산자» 위인지 검사한다.

왜 필요한가 (세션44, 만세 고착)
--------------------------------
사용자가 『バンザイ』 커맨드를 쓰면 연출이 안 나오고 빈 대사창으로 **진행 불가**가
됐다. 원인은 파일25 `0x4CE8F1` 한 줄이었다:

    원본   … f8 22 05 │ f8 6a 06 │ f0 6f e9 ad │ 98 7e 8e 52 (バンザイ) …
    빌드   … f8 22 05 │ f8 6a ea 09 ec 75 00 │ ea 53 ea 51 (만세)   …
                            ↑ F8 6A 의 피연산자 06 이 한글 바이트로 덮였다

워크리스트는 런 시작을 `0x4CE8F1` 로 적었는데 그 자리는 **`F8 6A` 의 피연산자**이고
실제 런은 한 바이트 뒤(`0x4CE8F2`, 「か」)에서 시작한다. 엔진은 `F8 6A` 뒤에서 변수
인덱스를 읽으므로 그 한 바이트가 바뀌면 엉뚱한 곳으로 간다.

기존 게이트가 왜 못 잡았나
--------------------------
`insert_extra.hits_opcode` 는 **오프코드 바이트 자체**(`F8 6A`)와 겹치는지만 본다.
피연산자는 오프코드가 아니라고 보기 때문에 이 자리는 통과한다. `verify_writes` 도
「추출기가 기록한 런 안이면 텍스트」로 판정하므로 기록 자체가 한 바이트 틀리면
동어반복이 된다 — 세션44의 `code_write_guard` 와 같은 종류의 맹점이다.

무엇을 검사하나
---------------
원본 ROM 을 오프코드 폭 표(`opcode_lengths.json`, 세션43 정본)로 걸으면서 «오프코드와
그 피연산자가 차지하는 바이트»를 전부 마스크로 모은 뒤, 각 워크리스트 행의 시작
오프셋이 그 마스크 위에 있으면 보고한다.

    python tools/verify_operands.py                 # 전 파일
    python tools/verify_operands.py --fid 25        # 한 파일
    python tools/verify_operands.py --fix bad.tsv   # 문제 행만 TSV 로
"""
import argparse
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
PROJ = os.path.dirname(HERE)
SURVEY = os.path.join(PROJ, "survey")
ORIG = os.path.join(os.path.dirname(PROJ), "Power Pro Kun Pocket 9 (Japan).nds")
WIDTHS = os.path.join(SURVEY, "ov28", "opcode_lengths.json")
FILES = (4, 8, 13, 18, 20, 25, 27, 30)

import struct


def fat(rom):
    off, ln = struct.unpack("<II", rom[0x48:0x50])
    return [struct.unpack("<II", rom[off + i * 8:off + i * 8 + 8])
            for i in range(ln // 8)]


def widths():
    """(f8_widths, bare_widths) — how many bytes each opcode occupies.

    ⚠ The JSON keys are DECIMAL strings, so `F8 15` is `f8["21"]`. That trap has
    bitten this project once already (session 30's empty choice boxes).
    """
    d = json.load(open(WIDTHS, encoding="utf-8"))
    f8 = {int(k): v for k, v in d.get("f8", {}).items()}
    bare = {int(k): v for k, v in d.get("bare", {}).items()}
    return f8, bare


def opcode_mask(buf, f8w, barew):
    """set of byte offsets (buffer-relative) occupied by an opcode or its operands"""
    mask = set()
    i, n = 0, len(buf)
    while i < n:
        b = buf[i]
        if b == 0xF8 and i + 1 < n:
            w = f8w.get(buf[i + 1], 2)
            mask.update(range(i, min(i + w, n)))
            i += max(w, 2)
            continue
        if b in barew:
            w = barew[b]
            mask.update(range(i, min(i + w, n)))
            i += max(w, 1)
            continue
        i += 1
    return mask


def worklist_rows(fid):
    rows = []
    for name in (f"file{fid}_extra.tsv", f"file{fid}_runs.tsv"):
        p = os.path.join(SURVEY, "common", name)
        if not os.path.exists(p):
            continue
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            c = ln.split("\t")
            if len(c) < 3 or not c[0].startswith("0x"):
                continue
            try:
                rows.append((int(c[0], 16), int(c[1]), c, name))
            except ValueError:
                continue
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fid", type=int)
    ap.add_argument("--fix", help="write offending rows to this TSV")
    ap.add_argument("--list", type=int, default=10)
    a = ap.parse_args()

    rom = open(ORIG, "rb").read()
    tab = fat(rom)
    f8w, barew = widths()
    fids = (a.fid,) if a.fid else FILES

    total_bad, bad_rows = 0, []
    for fid in fids:
        lo, hi = tab[fid]
        if hi <= lo:
            continue
        rows = worklist_rows(fid)
        if not rows:
            continue
        mask = opcode_mask(rom[lo:hi], f8w, barew)
        bad = [(off, blen, c, src) for off, blen, c, src in rows
               if lo <= off < hi and (off - lo) in mask]
        if not bad:
            print(f"file{fid}: {len(rows)} rows, ok")
            continue
        total_bad += len(bad)
        print(f"file{fid}: {len(rows)} rows, **{len(bad)} start on an opcode operand**")
        for off, blen, c, src in bad[:a.list]:
            jp = c[4] if len(c) > 4 else ""
            ko = c[5] if len(c) > 5 else ""
            here = rom[off - 4:off + 6].hex(" ")
            print(f"    0x{off:06X} b={blen:<3d} {jp[:18]!r} -> {ko[:14]!r}")
            print(f"        bytes around: {here}   [{src}]")
        if len(bad) > a.list:
            print(f"    ... {len(bad) - a.list} more")
        bad_rows += [(fid, off, blen, c, src) for off, blen, c, src in bad]

    print(f"\ntotal rows starting on an opcode operand: {total_bad}")
    if a.fix and bad_rows:
        with open(a.fix, "w", encoding="utf-8") as f:
            f.write("fid\toffset\tbudget\tjp\tko\tsource\n")
            for fid, off, blen, c, src in bad_rows:
                jp = c[4] if len(c) > 4 else ""
                ko = c[5] if len(c) > 5 else ""
                f.write(f"{fid}\t0x{off:06X}\t{blen}\t{jp}\t{ko}\t{src}\n")
        print(f"wrote {len(bad_rows)} rows to {a.fix}")
    return 1 if total_bad else 0


if __name__ == "__main__":
    sys.exit(main())
