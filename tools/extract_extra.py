#!/usr/bin/env python3
"""Emit a worklist for the text `extract_common.py` never saw.

`extract_common.py` anchors on `F8 6B`, the dialogue MESSAGE opener. That is one
of dozens of opcodes that introduce text: file 4 alone has 76, and the ones it
misses carry real sentences -- 「に着いたぞ。」, 「』を飲んだ！」, 「」ってなんだと思うでやんすか？」 --
the continuation fragments that follow a name or item insert. Whole screens read as
Japanese because of it.

This walks with the validated opcode widths (tools/walk_file.py) and writes every
still-untranslated run WITH ITS OFFSET, because these runs cannot be located the
way insert_common locates its own (by re-walking `F8 6B` and matching text) --
there is no opener to anchor on.

    python tools/extract_extra.py 4      -> survey/common/file4_extra.tsv
"""
import os, sys, argparse, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import walk_file as W
import poketbl as P

OUT = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/common"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fid", type=int)
    ap.add_argument("--min-budget", type=int, default=3)
    a = ap.parse_args()

    rom = open(W.ORIG, "rb").read()
    tr = W.translated()
    lo, hi = W.fat_span(rom, a.fid)

    rows, seen = [], collections.Counter()
    for tag, off, blen, t in W.walk(rom, lo, hi):
        if t in tr:
            continue
        seen[t] += 1
        rows.append((off, blen, tag, t))

    # one row per distinct string, carrying its smallest budget: identical text
    # must get one translation, and it has to fit the tightest place it appears
    best = {}
    for off, blen, tag, t in rows:
        if t not in best or blen < best[t][1]:
            best[t] = (off, blen, tag)
    out = [(v[0], v[1], v[2], seen[t], t) for t, v in best.items()
           if v[1] >= a.min_budget]
    out.sort(key=lambda r: (-r[3], -r[1]))

    path = os.path.join(OUT, f"file{a.fid}_extra.tsv")
    # ⚠ Preserve Korean already entered here. Regenerating naively wipes it twice
    # over: the rows are rewritten from scratch, AND `translated()` reads THIS file,
    # so anything already filled in counts as translated and is dropped from the
    # new list entirely. Both effects silently discard finished work.
    keep = {}
    if os.path.exists(path):
        for ln in open(path, encoding="utf-8").read().splitlines()[1:]:
            f = ln.split("\t")
            if len(f) >= 6 and f[5].strip():
                keep[f[4]] = (f[0], f[1], f[2], f[3], f[5])
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("offset\tbudget\topcode\toccurrences\tjp\tko\n")
        for t, (off, b, tag, n, ko) in keep.items():
            f.write(f"{off}\t{b}\t{tag}\t{n}\t{t}\t{ko}\n")
        for off, blen, tag, n, t in out:
            if t in keep:
                continue
            f.write(f"0x{off:06X}\t{blen}\t{tag}\t{n}\t{t}\t\n")
    if keep:
        print(f"  preserved {len(keep)} existing translations")
    print(f"file {a.fid}: {len(rows)} untranslated runs, "
          f"{len(best)} distinct, {len(out)} with budget >= {a.min_budget}")
    print(f"wrote {path}")
    top = collections.Counter(r[2] for r in out)
    print(f"  by introducing opcode: {dict(top.most_common(8))}")


if __name__ == "__main__":
    main()
