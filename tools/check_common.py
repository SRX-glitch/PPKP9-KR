#!/usr/bin/env python3
"""Validate the shared-file translations before anyone tries to insert them.

Three things can be wrong and only one of them is visible by reading the TSV:

  1. GLYPH BUDGET. Every Hangul syllable needs a slot in the font pack. The pack
     holds 1,658 and overlay 28's translation already claims most of it. A
     syllable file 27 needs that the pack does not have cannot be drawn at all.
  2. ENCODABILITY. Anything that is not a Hangul syllable has to already exist as
     a game charcode. This is where the look-alike punctuation traps live: ―, –,
     ~ and 〜 all read as a dash in an editor and only ～ (U+FF5E) has a glyph.
  3. WIDTH. A line longer than the original still has to fit the text box.

    python tools/check_common.py                 # all shared files
    python tools/check_common.py --file 27 --list
"""
import argparse, glob, json, os, sys, collections

sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

BASE = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"
COMMON = f"{BASE}/survey/common"
KRMAP = f"{BASE}/survey/font/kr_map.json"

# Same table tl.py uses. Every one of these renders as something else or as
# nothing; naming the replacement is the point.
LOOKALIKE = {"(": "（", ")": "）", "~": "～", "%": "％", "—": "～", "!": "！",
             "?": "？", ",": "、", ".": "。", '"': "「", "'": "「", "―": "～",
             "–": "～", "─": "～", "-": "～", "〜": "～", "‥": "・・",
             ":": "・", ";": "、"}


def is_hangul(ch):
    return 0xAC00 <= ord(ch) <= 0xD7A3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", type=int)
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()

    m = json.load(open(KRMAP, encoding="utf-8"))
    have = set(m["syl"])                     # syllables the pack already draws
    one = set(m.get("one", {}))
    raw = set(m.get("raw", {}))
    print(f"font pack: {len(have)} syllables allocated, capacity 1658")

    rows_all = []
    for path in sorted(glob.glob(f"{COMMON}/file*_runs.tsv")):
        fid = int(os.path.basename(path)[4:].split("_")[0])
        if a.file is not None and fid != a.file:
            continue
        for line in open(path, encoding="utf-8").read().splitlines()[1:]:
            f = line.split("\t")
            if len(f) >= 4 and f[3]:
                rows_all.append((fid, int(f[0]), int(f[1]), f[2], f[3]))
    print(f"translated rows: {len(rows_all)}")

    need = collections.Counter()             # new syllables, weighted by uses
    bad = collections.Counter()              # not encodable at all
    look = collections.Counter()             # look-alike punctuation
    wide = []
    for fid, n, occ, jp, ko in rows_all:
        for ch in ko:
            if ch in LOOKALIKE:
                look[ch] += 1
                continue
            if is_hangul(ch):
                if ch not in have:
                    need[ch] += occ
                continue
            if ch in one or ch in raw or ch == " ":
                continue
            if P.CH2CC.get(ch) is None:
                bad[ch] += 1
        if len(ko) > len(jp):
            wide.append((fid, n, len(jp), len(ko), jp, ko))

    # Every miss is data for the eventual font-pack rework: it says which
    # syllable the natural translation wanted and what had to be used instead.
    # Appending here means the record builds itself instead of depending on
    # whoever is translating remembering to write it down.
    if need:
        gaps = f"{COMMON}/font_gaps.tsv"
        seen = set()
        if os.path.exists(gaps):
            seen = {l.split("\t")[0] for l in
                    open(gaps, encoding="utf-8").read().splitlines()[1:]}
        fresh = [c for c in need if c not in seen]
        if fresh:
            with open(gaps, "a", encoding="utf-8", newline="") as fh:
                for c in fresh:
                    hits = [str(n) for fid, n, occ, jp, ko in rows_all if c in ko]
                    fh.write(f"{c}\t{a.file if a.file else '?'}\t{','.join(hits[:6])}"
                             f"\t\t\t\tAUTO: 미해결 — 대체어 미정\n")
            print(f"   ! font_gaps.tsv 에 {len(fresh)}자 추가: {' '.join(fresh)}")

    print(f"\n1. GLYPH BUDGET")
    print(f"   distinct NEW Hangul syllables required: {len(need)}")
    print(f"   pack headroom (1658 - {len(have)}): {1658 - len(have)}")
    short = len(need) - (1658 - len(have))
    print(f"   -> {'SHORT by ' + str(short) if short > 0 else 'fits'}")
    if need:
        print("   rarest (drop these first if you must):",
              " ".join(c for c, _ in need.most_common()[:-13:-1]))

    print(f"\n2. ENCODABILITY")
    print(f"   look-alike punctuation used: {dict(look) or 'none'}")
    print(f"   characters with no charcode: {dict(bad) or 'none'}")

    print(f"\n3. WIDTH  (translation longer than the original)")
    print(f"   rows: {len(wide)} / {len(rows_all)}")
    over = [w for w in wide if w[3] - w[2] >= 6]
    print(f"   longer by 6+ chars: {len(over)}")
    for w in sorted(over, key=lambda w: w[2] - w[3])[:12 if not a.list else len(over)]:
        print(f"     f{w[0]} #{w[1]}  {w[2]}->{w[3]}  {w[4]}  =>  {w[5]}")


if __name__ == "__main__":
    main()
