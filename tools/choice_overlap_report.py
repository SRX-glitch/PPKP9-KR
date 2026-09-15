# -*- coding: utf-8 -*-
"""choice_overlap_report.py -- WHERE the choice-preview overlap happens, with text.

Extends choice_width.py: for every F8 F8 preview group, decodes the ORIGINAL
Japanese siblings and the BUILD's Korean siblings. A sibling whose build bytes
are an F7 escape gets its Korean from the worklists (offset-keyed rows), so
escape groups are no longer "unknown width". Reports every group whose Korean
spread >= 2 cells while the Japanese spread was <= 1 -- the exact condition
that leaves the previous sibling's tail on screen (「방금 낚였다보했다」).

    PYTHONIOENCODING=utf-8 python tools/choice_overlap_report.py [build.nds]
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
BASE = os.path.dirname(HERE)
GAMEDIR = os.path.dirname(BASE)
ORIG = os.path.join(GAMEDIR, "Power Pro Kun Pocket 9 (Japan).nds")

import poketbl as P
from choice_width import fat_span, TERM

BUILD = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    BASE, "builds", "PPKP9_kr_v224_short108.nds")

CC2CH = {}
for ch, cc in P.CH2CC.items():
    CC2CH.setdefault(cc, ch)


def decode_seg(buf, i, end):
    """(text, cells, has_escape, stop_index) for one preview segment."""
    out = []
    cells = 0
    esc = False
    while i < end:
        b = buf[i]
        if b in TERM or (b == 0xF8 and i + 1 < end and buf[i + 1] == 0xF8):
            break
        if b == 0xF7:
            esc = True
            out.append("<esc>")
            i += 2
            continue
        if b == 0xF8:
            break
        if b >= 0xE8:
            cc = 256 + (b - 232) * 256 + buf[i + 1]
            out.append(CC2CH.get(cc, "?"))
            cells += 1
            i += 2
        else:
            out.append(CC2CH.get(b - 1, " " if b == 0 else "?"))
            cells += 1
            i += 1
    return "".join(out), cells, esc, i


def ko_width(s):
    return sum(0 if c == "　" else 1 for c in s) + s.count("　")


def worklist_ko(fid):
    out = {}
    p = os.path.join(BASE, "survey", "common", f"file{fid}_extra.tsv")
    if os.path.exists(p):
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            parts = ln.split("\t")
            if len(parts) >= 6 and not ln.startswith("#"):
                try:
                    out[int(parts[0], 16)] = parts[5]
                except ValueError:
                    pass
    return out


def main():
    orig = open(ORIG, "rb").read()
    build = open(BUILD, "rb").read()
    report = []
    for fid in (4, 8, 18, 20, 25, 27, 30):
        plo, phi = fat_span(orig, fid)
        blo, bhi = fat_span(build, fid)
        wl = worklist_ko(fid)
        i = plo
        while i < phi - 2:
            if not (orig[i] == 0xF8 and orig[i + 1] == 0xF8):
                i += 1
                continue
            sibs = []
            j = i
            while j < phi - 2 and orig[j] == 0xF8 and orig[j + 1] == 0xF8:
                jp, jw, _e, k = decode_seg(orig, j + 2, phi)
                # Korean side, same pristine offset mapped into the build
                bt, bw, besc, _k2 = decode_seg(build, j + 2 + (blo - plo), bhi)
                if besc:
                    ko = wl.get(j + 2)
                    if ko is not None:
                        bt, bw = ko, ko_width(ko)
                    else:
                        bt, bw = bt, None       # escape, ko unknown
                sibs.append((j + 2, jp, jw, bt, bw))
                if k < phi and orig[k] in TERM:
                    k += 1
                if k <= j:
                    break
                j = k
            i = j + 1
            if len(sibs) < 2 or all(w == 0 for _o, _j, w, _b, _w2 in sibs):
                continue
            jws = [w for _o, _j, w, _b, _w2 in sibs]
            bws = [w for _o, _j, _w, _b, w in sibs]
            if None in bws:
                continue                        # still unknown -- rare now
            if max(bws) - min(bws) >= 2 and max(jws) - min(jws) <= 1:
                report.append((fid, sibs))
    lines = []
    for fid, sibs in report:
        lines.append(f"f{fid} group @0x{sibs[0][0]:06X}")
        for o, jp, jw, ko, kw in sibs:
            lines.append(f"    0x{o:06X} [{jw:2d}] {jp!r:<28} -> [{kw:2d}] {ko!r}")
    text = "\n".join(lines)
    print(text)
    print(f"\n{len(report)} groups need width balancing")
    out = os.path.join(BASE, "survey", "choice_overlap_v224.txt")
    open(out, "w", encoding="utf-8").write(text + "\n")
    print("wrote", out)


if __name__ == "__main__":
    main()
