#!/usr/bin/env python3
"""Find translations that were written against the wrong draft column.

The translation drafts in `translation/work/draft_*.tsv` are laid out
`n | id | occ | max | prev | jp | next` -- `prev`/`next` are CONTEXT, only `jp`
is to be translated. If a row's Korean actually renders `next` (or `prev`), the
pair is wrong: that Japanese ships with someone else's line, and its own line
never gets translated. Found by accident on `に連れて行けば、`, which carried
「이런 놈도 조금은 전력이 될까。）」 -- the translation of its `next`.

The test is exact, not fuzzy: take the Korean some batch assigned to `next`, and
flag the row if `jp`'s Korean is the same string. Identical Korean for two
genuinely near-identical Japanese lines is common and legitimate, so keying on the
draft's own neighbour column is what keeps this from drowning in false positives.

⚠ A hit names a PAIR, and you decide which half is wrong -- the tool cannot.
`セーブ`→`세이브` and `を選んで、`→`세이브` both get flagged; only the second is the
error. And two lines can share Korean legitimately (`全然。` and `さっぱり。` are both
「전혀。」). Read the context and judge; session 30 found 8 real errors among 12 hits,
all of them in batch120.
"""
import os, sys, glob, collections

BASE = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"


def batches():
    """jp -> (ko, file, lineno) over every batch worklist."""
    out = {}
    for fn in sorted(glob.glob(os.path.join(BASE, "translation", "*.tsv"))):
        if os.path.basename(fn).startswith("worksheet"):
            continue
        for i, ln in enumerate(open(fn, encoding="utf-8").read().splitlines()[1:], 2):
            p = ln.split("\t")
            if len(p) >= 2 and p[0].strip() and p[-1].strip() and not p[0].startswith("0x"):
                out.setdefault(p[0], (p[-1], os.path.basename(fn), i))
    return out


def main():
    tr = batches()
    hits = []
    for fn in sorted(glob.glob(os.path.join(BASE, "translation", "work", "draft_*.tsv"))):
        for ln in open(fn, encoding="utf-8").read().splitlines()[1:]:
            p = ln.split("\t")
            if len(p) < 7:
                continue
            prev, jp, nxt = p[4], p[5], p[6]
            if jp not in tr:
                continue
            ko = tr[jp][0]
            for name, other in (("next", nxt), ("prev", prev)):
                if other and other != jp and other in tr and tr[other][0] == ko:
                    hits.append((os.path.basename(fn), p[0], name, jp, ko,
                                 other, tr[jp][1], tr[jp][2]))
                    break

    print(f"rows whose Korean belongs to a neighbouring column: {len(hits)}\n")
    for f, n, which, jp, ko, other, bf, bl in hits:
        print(f"{bf}:{bl}   ({f} row {n}, matches its `{which}`)")
        print(f"  jp   {jp}")
        print(f"  ko   {ko}      <- this actually renders: {other}")
        print()
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
