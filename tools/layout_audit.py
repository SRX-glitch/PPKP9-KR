#!/usr/bin/env python3
"""Predict dialogue-box layout damage from Korean being wider than Japanese.

Box geometry, read off the gameplay engine (overlay 1 @0x020BF958):
  - width accounting is 3 units per full-width glyph, 2 for the halfwidth kana
    table (charcode >= 0x1000), matching the scanner at 0x0203C9DC
  - the engine wraps when the column passes 0x38 = 56 units  -> 18 full glyphs
  - it then bumps a line counter and, at 3 lines, sets the "page full" flag
    (0x020BFC5C), i.e. a box shows 3 lines and waits for input

Each `F8 6B` entry is one authored line, so a translation wider than one line
silently costs an extra display line and can push a 3-line page over.

MTE does not distort this: the engine advances by render_char's actual returned
column, and an MTE code expands to its real glyphs, so width is counted per
rendered glyph -- which means the Korean cost is simply its character count,
spaces included (the space host is a full-width charcode, so a space costs a
full glyph slot).
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

BASE = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"
LINE_UNITS = 56
import glob as _glob
BATCHES = ["common_lines"] + sorted(
    (os.path.splitext(os.path.basename(p))[0]
     for p in _glob.glob(f"{BASE}/translation/batch*.tsv")),
    key=lambda n: int(n[5:]))


def widths(s, korean):
    """Per-glyph cursor advance, exactly as render_char returns it.

    render_char draws a glyph in slices, advancing the column by 2 and then, for
    charcodes below 0x1000, by 1 more (0x0203CE94/0x0203CEB8) -- so full width
    costs 3 and the halfwidth kana table costs 2, matching the scanner. Korean is
    always full width, spaces included: the space host is a normal charcode.
    """
    if korean:
        return [3] * len(s)
    out = []
    for ch in s:
        cc = P.CH2CC.get(ch)
        out.append(2 if (cc is not None and cc >= 0x1000) else 3)
    return out


def rows(s, korean=False):
    """Simulate the wrap: the engine breaks AFTER the glyph that pushes the
    column to >= 56 (0x020BFBFC), so a line holds 19 full-width glyphs."""
    n, col = 1, 0
    for w in widths(s, korean):
        col += w
        if col >= LINE_UNITS:
            n += 1
            col = 0
    return n - 1 if col == 0 and n > 1 else n


def main():
    trans = {}
    for name in BATCHES:
        p = f"{BASE}/translation/{name}.tsv"
        if not os.path.exists(p):
            continue
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            if "\t" in ln:
                jp, ko = ln.split("\t")[:2]
                if jp.strip() and ko.strip():
                    trans[jp.strip()] = ko.strip()

    occ = collections.Counter()
    for ln in open(f"{BASE}/survey/ov28/dialogue_runs.tsv", encoding="utf-8").read().splitlines():
        p = ln.split("\t")
        if len(p) >= 4:
            occ[p[3]] += 1

    same = grew = 0
    grew_occ = 0
    worst = []
    hist = collections.Counter()
    for jp, ko in trans.items():
        if jp not in occ:
            continue
        rj, rk = rows(jp), rows(ko, korean=True)
        hist[(rj, rk)] += 1
        if rk > rj:
            grew += 1
            grew_occ += occ[jp]
            worst.append((rk - rj, rk, rj, occ[jp], jp, ko))
        else:
            same += 1
    total = same + grew
    print(f"translated lines present in overlay 28: {total}")
    print(f"  fit in the same number of display lines : {same} ({same/total:.1%})")
    print(f"  need MORE display lines than the original: {grew} ({grew/total:.1%}), "
          f"{grew_occ} occurrences")
    print("\ndisplay-line count (JP -> KR): count")
    for (rj, rk), n in sorted(hist.items()):
        flag = "  <-- grew" if rk > rj else ""
        print(f"  {rj} -> {rk}: {n}{flag}")

    worst.sort(reverse=True)
    print("\nworst offenders (extra lines, KR rows, JP rows, occurrences):")
    for d, rk, rj, n, jp, ko in worst[:15]:
        print(f"  +{d} ({rj}->{rk}) x{n}  {jp}")
        print(f"        -> {ko}  [{len(ko)} glyphs]")

    # how close is the whole corpus to the one-line limit?
    over = [ko for jp, ko in trans.items() if jp in occ and rows(ko, korean=True) > 1]
    print(f"\nKorean lines wider than one display line: {len(over)}")
    lens = sorted(len(k) for k in trans.values())
    print(f"Korean glyph count: median {lens[len(lens)//2]}, "
          f"p90 {lens[int(len(lens)*0.9)]}, max {lens[-1]} (one line holds 19)")


if __name__ == "__main__":
    main()
