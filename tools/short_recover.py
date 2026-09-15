# -*- coding: utf-8 -*-
"""short_recover.py -- turn safe no-worklist SHORT sites into recorded rows.

Session 45's ② class: 216 short (<4B) no-worklist sites that MIN_MULTI_BYTES
rightly keeps sites() away from. The safe path is a RECORDED worklist row per
site (recorded offsets are exempt from the gate, and the want-gate still
verifies the pristine bytes at write time). This tool:

  1. reads survey/shipmiss_v216.tsv (live v216 offsets -> pristine via deltas)
  2. keeps no-worklist rows, encoded jp >= 3B, ko clean of kana/kanji
  3. drops sites whose surroundings look like code/tables (audit_sites scorers)
  4. re-walks the pristine file and requires a run to START at the site with
     EXACTLY the row's jp text -- budget and introducing opcode come from the
     walk, not from guesses
  5. refuses a row whose jp already exists in that file's worklist with a
     DIFFERENT ko (sites() keeps one ko per jp -- a second spelling would
     silently hijack every recorded site of that string)
  6. appends rows to survey/common/file{fid}_extra.tsv (--write), else reports

    PYTHONIOENCODING=utf-8 python tools/short_recover.py [--write]
"""
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
from audit_sites import arm_likeness, table_likeness

# live v216 offset -> pristine (deltas measured by audit_sites on v216)
DELTA = {"4": 0x277A400, "8": 0x285C000, "18": 0x2D04600,
         "20": 0x2C40600, "25": 0x2558800, "27": 0x27B7C00, "30": 0x2B2F000}


def enclen(s):
    n = 0
    for ch in s:
        cc = P.CH2CC.get(ch)
        if cc is None:
            return None
        n += 1 if cc < 231 else 2
    return n


def has_jp(s):
    for c in s:
        name = unicodedata.name(c, "")
        if "HIRAGANA" in name or "KATAKANA" in name or "CJK" in name:
            return True
    return False


def main():
    write = "--write" in sys.argv
    orig = open(ORIG, "rb").read()
    rows = [r.split("\t") for r in open(
        os.path.join(BASE, "survey", "shipmiss_v216.tsv"),
        encoding="utf-8").read().splitlines()[1:]]
    # index existing worklist jp->ko per file, and walk runs per file
    runs = {}
    existing = {}
    adds = {}
    skipped = {"dirty": 0, "suspect": 0, "no-run": 0, "jp-conflict": 0,
               "short": 0}
    for p in rows:
        fid, off_l, _b, reason, jp, ko = p[0], int(p[1], 16), p[2], p[3], p[4], p[5]
        if reason != "no-worklist" or not ko:
            continue
        jb = enclen(jp)
        if jb is None or jb < 3:
            skipped["short"] += 1
            continue
        if jb >= 4:
            continue        # >=4B sites are ①/other classes, not ②'s gate-blocked
        if has_jp(ko):
            skipped["dirty"] += 1
            continue
        o = off_l - DELTA[fid]
        if arm_likeness(orig, o) >= 0.3 or table_likeness(orig, o) >= 0.6:
            skipped["suspect"] += 1
            continue
        if fid not in runs:
            lo, hi = W.fat_span(orig, int(fid))
            runs[fid] = {roff: (tag, blen, t)
                         for tag, roff, blen, t in W.walk(orig, lo, hi)}
            path = os.path.join(BASE, "survey", "common",
                                f"file{fid}_extra.tsv")
            existing[fid] = {}
            if os.path.exists(path):
                for ln in open(path, encoding="utf-8").read().splitlines()[1:]:
                    parts = ln.split("\t")
                    if len(parts) >= 6 and not ln.startswith("#"):
                        existing[fid][parts[4]] = parts[5]
        hit = runs[fid].get(o)
        if not hit or hit[2] != jp:
            skipped["no-run"] += 1
            continue
        prev = existing[fid].get(jp)
        if prev not in (None, "", ko):
            skipped["jp-conflict"] += 1
            continue
        tag, blen, _t = hit
        adds.setdefault(fid, []).append(
            f"0x{o:06X}\t{blen}\t{tag}\t1\t{jp}\t{ko}")
    total = sum(len(v) for v in adds.values())
    for fid in sorted(adds):
        print(f"file {fid}: {len(adds[fid])} rows")
        for r in adds[fid][:6]:
            print("   ", r)
    print(f"total addable: {total}, skipped: {skipped}")
    if write:
        for fid, lst in adds.items():
            path = os.path.join(BASE, "survey", "common",
                                f"file{fid}_extra.tsv")
            t = open(path, encoding="utf-8").read()
            if not t.endswith("\n"):
                t += "\n"
            t += "\n".join(lst) + "\n"
            open(path, "w", encoding="utf-8").write(t)
            print(f"appended {len(lst)} rows to {path}")


if __name__ == "__main__":
    main()
