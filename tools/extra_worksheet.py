#!/usr/bin/env python3
"""Emit the next translation worksheet from a `survey/common/file*_extra.tsv` worklist.

The extra worklists are the inline-budget rows that `insert_extra.py` writes by
offset. They are already ordered by (-occurrences, -budget), so "the next N
untranslated rows" is already the right priority order -- the tail is flat
(session 31 measured only ~106 rows with occurrence >= 3 in file 4), so there is
no frequency shortcut to be had beyond that.

Rows already carrying Korean are skipped, and so is anything already translated
in `translation/file*_ko*.tsv` (the staging files `merge_extra.py` reads back).

    python tools/extra_worksheet.py 4 --n 250 --out translation/f4_w01.tsv

The `max` column is how many Hangul syllables the budget holds if the line were
pure Hangul (2 B each). Punctuation and spaces are 1 B, so a line can exceed it.
`merge_extra.py` is the authority on fit; this column is only a writing aid.
"""
import os, sys, glob, argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jp_filter

BASE = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"
COMMON = BASE + "/survey/common"
TDIR = BASE + "/translation"


def staged():
    """jp -> ko from every `translation/file*_ko*.tsv` staging file."""
    out = {}
    for p in sorted(glob.glob(f"{TDIR}/file*_ko*.tsv")):
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            f = ln.split("\t")
            if len(f) >= 2 and f[0].strip() and f[1].strip():
                out[f[0].strip()] = f[1].strip()
    return out


def worklist(fid):
    """(offset, budget, opcode, occurrences, jp, ko) rows of one worklist."""
    p = f"{COMMON}/file{fid}_extra.tsv"
    for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
        f = ln.split("\t")
        if len(f) >= 5:
            yield f[0], int(f[1]), f[2], int(f[3]), f[4], (f[5] if len(f) > 5 else "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fid", type=int)
    ap.add_argument("--n", type=int, default=250)
    ap.add_argument("--out", default=None)
    ap.add_argument("--skip", type=int, default=0,
                    help="skip the first N eligible rows (for parallel batches)")
    ap.add_argument("--tier", default="A",
                    help="opcode tiers to include, e.g. A, AB, ABC (jp_filter)")
    ap.add_argument("--near", type=int, default=0,
                    help="only rows within N worklist rows (by offset) of an "
                         "ALREADY TRANSLATED row; 0 disables. See the note below.")
    a = ap.parse_args()
    # ⭐⭐ SESSION 41 -- THE SELECTOR THAT ACTUALLY FINDS THE MIXED-LANGUAGE LINES.
    # The user's observation: on screen, Korean runs for a while and then one
    # Japanese line appears. Those lines are NOT noise and NOT missing from the
    # worklist -- they are ordinary untranslated rows sitting INSIDE an otherwise
    # finished stretch of script. Two selectors already in this repo miss them:
    #   * `--tier A` (introducing opcode) was calibrated on files 4/25/27 and does
    #     not transfer -- file 30's tier A is mostly graphics data.
    #   * `untranslated_worksheet.py` walks `rom_census.src_dialogue`, which is
    #     `F8 6B`-gated, and file 30's epilogue text is not F8 6B, so that tool
    #     reports f30/dialogue = 0 and sees none of it.
    # Proximity is the signal that does transfer, because script and data live in
    # CONTIGUOUS blocks: a row whose neighbours are translated is real text.
    # Verified on the line photographed in the album epilogue (No.33):
    #   f30 0x328AE8 「つ、ついに！ついに完成したぞ！」 -- untranslated, and its
    #   next four neighbours are all translated and all on that same screen.
    # Measured with a +-8 window at >=50% translated: 1,947 rows across the
    # worklists (f4 1,364 - f27 358 - f30 110 - f25 38 - f18 34 - f8 23 - f20 20),
    # while files 13/24/31 score ZERO, which matches them being untouched data.

    done = staged()
    if a.near:
        # Offset order is worklist order here; distance is in ROWS, not bytes,
        # so a dense stretch of short lines is not penalised against a sparse one.
        wl = sorted(worklist(a.fid), key=lambda r: int(r[0], 16))
        has_ko = [bool(r[5].strip()) or r[4] in done for r in wl]
        rows = []
        for i, (off, budget, op, occ, jp, ko) in enumerate(wl):
            if ko.strip() or jp in done:
                continue
            lo, hi = max(0, i - a.near), min(len(wl), i + a.near + 1)
            d = min((abs(j - i) for j in range(lo, hi) if has_ko[j]), default=None)
            if d is None:
                continue
            rows.append((d, -occ, budget, off, jp))
        rows.sort()
        rows = [(-occ, budget, off, jp) for _d, occ, budget, off, jp in rows]
        dropped = 0
    else:
        rows, dropped = [], 0
        for off, budget, op, occ, jp, ko in worklist(a.fid):
            if ko.strip() or jp in done:
                continue
            if jp_filter.tier(op) not in a.tier:
                dropped += 1
                continue
            rows.append((occ, budget, off, jp))

    picked = rows[a.skip:a.skip + a.n]
    out = a.out or f"{TDIR}/f{a.fid}_worksheet.tsv"
    if not os.path.isabs(out):
        out = os.path.join(BASE, out)
    with open(out, "w", encoding="utf-8", newline="") as f:
        f.write("occ\tbudget\tmax\toffset\tjp\tko\n")
        for occ, budget, off, jp in picked:
            f.write(f"{occ}\t{budget}\t{budget // 2}\t{off}\t{jp}\t\n")
    print(f"{out}: {len(picked)} rows (tier {a.tier} pool {len(rows)}, "
          f"{dropped} rows in other tiers, staged elsewhere {len(done)})")


if __name__ == "__main__":
    main()
