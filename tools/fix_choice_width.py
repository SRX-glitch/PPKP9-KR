# -*- coding: utf-8 -*-
"""fix_choice_width.py -- pad choice-preview siblings to equal width.

Runs the same judgment as choice_overlap_report (277 F8 F8 groups, Korean
spread >= 2 where the Japanese spread was <= 1), then for every flagged group
pads each shorter sibling's Korean with trailing U+3000 up to the group's
longest sibling. The pad rides an OFFSET-keyed worklist row (updated in place
if the offset already has one, appended otherwise, budget/opcode from the
walker), so the want-gate still guards the write and MIN_MULTI stays intact.

    python tools/fix_choice_width.py           # report what would change
    python tools/fix_choice_width.py --write   # apply to file{fid}_extra.tsv
"""
import glob
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
BASE = os.path.dirname(HERE)
GAMEDIR = os.path.dirname(BASE)
ORIG = os.path.join(GAMEDIR, "Power Pro Kun Pocket 9 (Japan).nds")

import poketbl as P
import walk_file as W
from choice_width import fat_span, TERM
from choice_overlap_report import ko_width, worklist_ko

BUILD = os.path.join(BASE, "builds", "PPKP9_kr_v224_short108.nds")
BASES = {4: 0x55F000, 8: 0x443200, 18: 0x1ECA00, 20: 0x22DA00,
         25: 0x4CC000, 27: 0x5E5A00, 30: 0x311E00}

CC2CH = {}
for ch, cc in P.CH2CC.items():
    CC2CH.setdefault(cc, ch)
KR = {cc: ch for ch, cc in json.load(
    open(os.path.join(BASE, "survey", "font", "kr_font_map.json"),
         encoding="utf-8")).items()}


def decode(buf, i, end, korean):
    out, cells, esc = [], 0, False
    while i < end:
        b = buf[i]
        if b in TERM or (b == 0xF8 and i + 1 < end and buf[i + 1] == 0xF8):
            break
        if b == 0xF7:
            esc = True
            i += 2
            continue
        if b == 0xF8:
            break
        if b >= 0xE8:
            cc = 256 + (b - 232) * 256 + buf[i + 1]
            out.append((KR.get(cc) if korean else None) or CC2CH.get(cc, "?"))
            cells += 1
            i += 2
        else:
            out.append(CC2CH.get(b - 1, " " if b == 0 else "?"))
            cells += 1
            i += 1
    return "".join(out), cells, esc, i


def corpus_map():
    def hasjp(s):
        return any(("HIRAGANA" in unicodedata.name(c, "")
                    or "KATAKANA" in unicodedata.name(c, "")
                    or "CJK" in unicodedata.name(c, "")) for c in s)
    out = {}
    for p in (sorted(glob.glob(os.path.join(BASE, "translation", "common_lines.tsv")))
              + sorted(glob.glob(os.path.join(BASE, "translation", "batch*.tsv")))
              + sorted(glob.glob(os.path.join(BASE, "translation", "file*_ko*.tsv")))
              + sorted(glob.glob(os.path.join(BASE, "translation", "dialogue_ko.tsv")))):
        for ln in open(p, encoding="utf-8", errors="replace").read().splitlines()[1:]:
            parts = ln.split("\t")
            if len(parts) >= 2:
                jp, ko = parts[-2].strip(), parts[-1].strip()
                if jp and ko and not hasjp(ko):
                    out[jp] = ko
    return out


def main():
    write = "--write" in sys.argv
    orig = open(ORIG, "rb").read()
    build = open(BUILD, "rb").read()
    rm = json.load(open(os.path.join(BASE, "survey", "redirect_manifest.json"),
                        encoding="utf-8"))
    red25 = {int(k, 16): v["ko"] for k, v in rm.items()
             if isinstance(v, dict) and v.get("ko")}
    tails = {}
    for fid in (8, 18, 20, 25, 30):
        p = os.path.join(BASE, "survey", f"tail_manifest_{fid}.json")
        if os.path.exists(p):
            tails[fid] = {e["rel"]: e["ko"] for e in
                          json.load(open(p, encoding="utf-8"))
                          if isinstance(e, dict) and e.get("ko")}
    corpus = corpus_map()
    changes = {}
    manual = []
    for fid in (4, 8, 18, 20, 25, 27, 30):
        plo, phi = fat_span(orig, fid)
        blo, bhi = fat_span(build, fid)
        wl = worklist_ko(fid)
        d = blo - plo
        base = BASES[fid]
        lo, hi = W.fat_span(orig, fid)
        runs = {roff: (tag, blen, t) for tag, roff, blen, t in W.walk(orig, lo, hi)}
        i = plo
        while i < phi - 2:
            if not (orig[i] == 0xF8 and orig[i + 1] == 0xF8):
                i += 1
                continue
            sibs = []
            j = i
            while j < phi - 2 and orig[j] == 0xF8 and orig[j + 1] == 0xF8:
                jp, jw, _e, k = decode(orig, j + 2, phi, korean=False)
                kt, kw, kesc, _ = decode(build, j + 2 + d, bhi, korean=True)
                if kesc:
                    ko = (wl.get(j + 2)
                          or (red25.get(j + 2 - base) if fid == 25 else None)
                          or tails.get(fid, {}).get(j + 2 - base)
                          or corpus.get(jp))
                    kt, kw = ko, (ko_width(ko) if ko else None)
                sibs.append((j + 2, jp, jw, kt, kw))
                if k < phi and orig[k] in TERM:
                    k += 1
                if k <= j:
                    break
                j = k
            i = j + 1
            sibs = [s for s in sibs if s[2] > 0]
            if len(sibs) < 2:
                continue
            kws = [s[4] for s in sibs]
            jws = [s[2] for s in sibs]
            if None in kws:
                continue
            if not (max(kws) - min(kws) >= 2 and max(jws) - min(jws) <= 1):
                continue
            target = max(kws)
            for o, jp, jw, kt, kw in sibs:
                if kw >= target or kt is None:
                    continue
                if "?" in jp or "?" in (kt or ""):
                    manual.append((fid, o, jp, kt))
                    continue
                # a sibling still showing Japanese needs a TRANSLATION first --
                # kana cannot ride the Korean encoder. The list screens' tiny
                # labels have fixed renderings.
                kt = kt.rstrip(" ")
                kw = ko_width(kt)
                if any(("HIRAGANA" in unicodedata.name(c, "")
                        or "KATAKANA" in unicodedata.name(c, "")
                        or "CJK" in unicodedata.name(c, ""))
                       for c in kt if c not in "・～ー"):
                    mini = {"なし": "없음", "その６": "그６", "その９": "그９",
                            "次へ": "다음"}
                    kt = mini.get(kt)
                    if kt is None:
                        manual.append((fid, o, jp, kt))
                        continue
                    kw = ko_width(kt)
                run = runs.get(o)
                if run and run[2] == jp:
                    tag, blen = run[0], run[1]
                else:
                    # F8F8 interiors are not always in the walk index; the
                    # want-gate re-verifies the jp bytes at write time anyway.
                    tag, blen = "F8F8", sum(
                        1 if P.CH2CC[c] < 231 else 2 for c in jp)
                padded = kt + "　" * (target - kw)
                changes.setdefault(fid, []).append((o, blen, tag, jp, padded))
    for fid in sorted(changes):
        print(f"file {fid}: {len(changes[fid])} sibling(s) to pad")
        for o, blen, tag, jp, ko in changes[fid]:
            print(f"    0x{o:06X} [{tag} b={blen}] {jp} -> {ko!r}")
    if manual:
        print("manual (skipped):")
        for fid, o, jp, kt in manual:
            print(f"    f{fid} 0x{o:06X} {jp} / {kt}")
    if not write:
        return
    for fid, lst in changes.items():
        path = os.path.join(BASE, "survey", "common", f"file{fid}_extra.tsv")
        lines = open(path, encoding="utf-8").read().splitlines()
        by_off = {}
        for n, ln in enumerate(lines):
            parts = ln.split("\t")
            if len(parts) >= 6 and not ln.startswith("#"):
                try:
                    by_off[int(parts[0], 16)] = n
                except ValueError:
                    pass
        added = updated = 0
        for o, blen, tag, jp, ko in lst:
            row = f"0x{o:06X}\t{blen}\t{tag}\t1\t{jp}\t{ko}"
            if o in by_off:
                lines[by_off[o]] = row
                updated += 1
            else:
                lines.append(row)
                added += 1
        open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        print(f"file {fid}: {updated} updated, {added} appended -> {path}")


if __name__ == "__main__":
    main()
