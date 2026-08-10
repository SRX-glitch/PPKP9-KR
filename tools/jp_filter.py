#!/usr/bin/env python3
"""Rank `file*_extra.tsv` rows by how likely they are to be real game text.

Roughly half the extra worklists are graphics/table data that the charcode
decoder turns into plausible-looking kana (「搭さいあい」, 「えペラだ。」, 「ェぺェゲェフィサェネ」).
Translating those wastes effort and, worse, writes Korean over binary data.

⛔ MEASURED NEGATIVE RESULT -- do not retry character n-grams.
A character bigram model and a trigram-with-backoff model were both trained on
this ROM's 21,711 hand-translated Japanese lines (a clean corpus: `さい` in the
batches is 「うるさい！」/「ください」, not the junk pattern) and scored against 59
hand-labelled real and 61 hand-labelled junk rows from `file4_extra.tsv`:

    bigram    real -8.48..-2.25   junk -8.10..-4.34   -> no separation
    trigram   real -9.59..-1.77   junk -9.21..-4.21   -> no separation

The reason is structural, not a tuning problem: the junk IS made of common kana
in common orders. 「あさい」 and 「ペラです。」 are perfectly ordinary Japanese
character sequences that simply do not mean anything. Only meaning separates
them, so no character-level statistic can. This is the same lesson as
`hunt_text.py`'s blacklist failures, one level deeper.

✅ WHAT WORKS: the INTRODUCING OPCODE, which is structure rather than statistics.
On the same 120 labelled rows:

    FC        0 real / 28 junk        FA      8 real /  6 junk
    F808     18 real /  0 junk        FE      2 real /  7 junk
    F8F8     11 real /  0 junk        FF      1 real /  3 junk
    F809      7 real /  1 junk        F822    0 real /  5 junk

Verified against random samples over all 16,575 rows of files 4/25/27 (see the
tiers below). Tiering does not DROP anything -- `tier C` rows stay in the
worklist and stay reachable with `--all`; they are just last in line.

    python tools/jp_filter.py --census
"""
import os, sys, io, collections, random

BASE = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"
COMMON = BASE + "/survey/common"

# Opcodes that introduce a script string. Sampled rows are dialogue, menu labels
# and item names with no junk visible.
TIER_A = {"FA", "FB", "F809", "F808", "F815", "F804", "F825", "F803",
          "F829", "F8F8", "F86B", "F823", "F805", "F80B", "F85A"}
# Mixed: real sentences and decoded data both appear under these.
TIER_B = {"FE", "FD", "FF", "F800", "F822"}
# Effectively all data. FC alone was 28 of 61 labelled junk rows and 0 of 59 real.
TIER_C = {"FC", "F9", "F882", "F88F", "F834"}


def tier(opcode):
    if opcode in TIER_A:
        return "A"
    if opcode in TIER_C:
        return "C"
    if opcode in TIER_B:
        return "B"
    return "B"          # unseen opcode: worth a look, but not ahead of tier A


def census():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    byop = collections.defaultdict(list)
    for fid in (4, 25, 27, 13, 18, 24, 30, 31):
        p = f"{COMMON}/file{fid}_extra.tsv"
        if not os.path.exists(p):
            continue
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            f = ln.split("\t")
            if len(f) >= 5:
                byop[f[2]].append((fid, f[4], (len(f) > 5 and f[5].strip())))
    tot = collections.Counter()
    for op, v in sorted(byop.items(), key=lambda k: -len(k[1])):
        t = tier(op)
        tot[t] += len(v)
        random.seed(1)
        s = random.sample(v, min(3, len(v)))
        print(f"  {t}  {op:5} n={len(v):5}  " +
              " | ".join(f"f{a}:{b[:16]}" for a, b, _ in s))
    print(f"\ntiers: {dict(tot)}   (A first, then B; C is data)")


if __name__ == "__main__":
    census()
