#!/usr/bin/env python3
"""Survey Japanese verbal tics (語尾) and how consistently we translated them.

A character whose every line ends in 「でやんす」 or 「ですぞ」 reads as one voice in
Japanese. If the Korean renders that tic three different ways -- or drops it --
the character stops sounding like themselves and the conversation loses its
shape. This finds the tics and shows what we actually did with each.

    python tools/tics.py                # which tics exist, how often
    python tools/tics.py --tic でやんす  # every line with that tic + its Korean
"""
import os, sys, glob, re, collections, argparse

BASE = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"
TRANS = BASE + "/translation"
COMMON = BASE + "/survey/common"

# Distinctive endings worth checking. Plain 「だ/です/ます/よ/ね」 are not tics --
# every character uses them -- so they are deliberately absent.
TICS = [
    "でやんす", "でげす", "でござる", "ござい", "ですぞ", "じゃぞ", "のじゃ",
    "ですな", "ますな", "だべ", "だっぺ", "っす", "ざます", "ますわ", "ですわ",
    "だわい", "ナリ", "だす", "どすえ", "であります", "ありんす", "にゃ",
    "だもん", "だもの", "かしら", "ですの", "ますの", "でおじゃる", "たまえ",
    "だぜ", "だぞ", "ぜよ", "ばい", "けん", "やねん", "でんがな", "でっせ",
]


def pairs():
    """Every (jp, ko) pair the project has produced, from all worklist shapes."""
    out = []
    for fn in sorted(glob.glob(os.path.join(TRANS, "*.tsv"))):
        for ln in open(fn, encoding="utf-8").read().splitlines()[1:]:
            p = ln.split("\t")
            if len(p) >= 2 and p[0] and p[-1]:
                # intro_lines.tsv is (offset, jp, ko); batches are (jp, ko)
                jp, ko = (p[1], p[2]) if p[0].startswith("0x") and len(p) >= 3 \
                    else (p[0], p[-1])
                out.append((jp, ko, os.path.basename(fn)))
    for fn in sorted(glob.glob(os.path.join(COMMON, "file*_runs.tsv"))):
        for ln in open(fn, encoding="utf-8").read().splitlines()[1:]:
            p = ln.split("\t")
            if len(p) >= 4 and p[2] and p[3]:
                out.append((p[2], p[3], os.path.basename(fn)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tic")
    ap.add_argument("--limit", type=int, default=40)
    a = ap.parse_args()

    ps = pairs()
    if a.tic:
        n = 0
        for jp, ko, src in ps:
            if a.tic in jp:
                print(f"{src:22s} {jp}\n{'':22s}  -> {ko}")
                n += 1
                if n >= a.limit:
                    break
        print(f"\n{n} shown")
        return

    print(f"translated pairs: {len(ps)}\n")
    print(f"{'tic':12s} {'lines':>6s}   Korean endings actually used")
    for tic in TICS:
        hits = [(jp, ko) for jp, ko, _ in ps if tic in jp]
        if not hits:
            continue
        # what the Korean ends with, ignoring trailing punctuation
        ends = collections.Counter()
        for _, ko in hits:
            k = re.sub(r"[。、！？」）・\s]+$", "", ko)
            ends[k[-3:]] += 1
        top = "  ".join(f"{e}({n})" for e, n in ends.most_common(6))
        print(f"{tic:12s} {len(hits):6d}   {top}")


if __name__ == "__main__":
    main()
