#!/usr/bin/env python3
"""For every run that HAS a translation but still shows Japanese, say WHY.

`jp_breakdown` counts them (session 44: 1,116, of which file 4 holds 888) but a
count does not tell you what to fix. Those runs fail for different reasons and
the fixes have nothing in common:

    no-worklist   nothing knows this offset -> an EXTRACTION gap (session 43's
                  missing_sites class). Translating more buys nothing.
    budget        the run is too short to hold even a redirect escape (< 3 B)
                  -> unfixable in place; needs record relocation
    over-budget   Korean is longer than the run, escape would fit -> should have
                  been redirected; if it was not, the region pass skipped it
    fits          Korean FITS and it still shows Japanese -> a pipeline bug,
                  the most suspicious class of all

⛔ Import note: use `rom_census`, NOT `reinsert`. `reinsert` imports `pokeencode`,
which reads `sys.argv[1]` as a charset path at module load, so importing it from
any script that takes a ROM argument crashes on the ROM's bytes.

    python tools/shipmiss_why.py builds/PPKP9_kr_v209_f8reloc.nds --fid 4
    python tools/shipmiss_why.py builds/PPKP9_kr_v209_f8reloc.nds --out gaps.tsv
"""
import argparse, collections, glob, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
PROJ = os.path.dirname(HERE)
SURVEY = os.path.join(PROJ, "survey")

import rom_census as R
import walk_file as W
import japanese_left as JL
from jp_breakdown import jp_runs


def corpus():
    """jp -> ko, from every source the build reads (jp_breakdown keeps only jp)."""
    out = {}
    for fn in sorted(glob.glob(os.path.join(PROJ, "translation", "*.tsv"))):
        if os.path.basename(fn).startswith("worksheet"):
            continue
        for ln in open(fn, encoding="utf-8").read().splitlines()[1:]:
            p = ln.split("\t")
            if len(p) >= 2 and p[0].strip() and p[1].strip():
                out.setdefault(p[0].strip(), p[1].strip())
            if len(p) >= 3 and p[0].startswith("0x") and p[2].strip():
                out.setdefault(p[1].strip(), p[2].strip())
    return out


def worklist(fid, base):
    """file-RELATIVE offset -> (budget, jp), from the file's own worklist.

    ⛔ The worklist stores offsets against the PRISTINE ROM, and the build
    relocates most of these files (file 4 moves from 0x5E.... to 0x2CD9400), so
    the raw numbers never match a built ROM. `base` is the file's pristine start
    and both sides are compared file-relative. Getting this wrong makes every
    single row look like an extraction gap.

    Deliberately file-based rather than `insert_extra.WORK()`: that pulls in
    `reinsert` (see the import note) and we only need offsets and budgets.
    """
    out = {}
    for name in (f"file{fid}_extra.tsv", f"file{fid}_runs.tsv"):
        p = os.path.join(SURVEY, "common", name)
        if not os.path.exists(p):
            p = os.path.join(SURVEY, name)
        if not os.path.exists(p):
            continue
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            c = ln.split("\t")
            if len(c) < 3 or not c[0].startswith("0x"):
                continue
            try:
                off = int(c[0], 16)
                blen = int(c[1])
            except ValueError:
                continue
            out.setdefault(off - base, (blen, c[-2] if len(c) > 3 else ""))
    return out


def enc_len(ko):
    """Rough encoded length: Hangul/kana are 2 bytes, ASCII digits 2, rest 1.

    Only used to split "fits" from "over-budget", so an approximation that never
    UNDER-counts Hangul is enough.
    """
    n = 0
    for ch in ko:
        n += 2 if ord(ch) > 0x7F or ch.isdigit() else 1
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rom")
    ap.add_argument("--fid", type=int, default=None)
    ap.add_argument("--list", type=int, default=6)
    ap.add_argument("--out", default=None, help="TSV of every row, with reason")
    a = ap.parse_args()

    rom = R.Rom(a.rom)
    pristine = R.Rom()          # the worklist's frame of reference
    tr = corpus()
    keep = JL.reassigned()
    esc = JL._skip_escapes(rom)

    fids = (a.fid,) if a.fid else (25, 4, 27, 20, 13, 30, 18, 8)
    grand = collections.Counter()
    rows = []

    for fid in fids:
        lo, hi = rom.span(fid)
        if hi <= lo:
            continue
        plo, _ = pristine.span(fid)
        work = worklist(fid, plo)
        why = collections.Counter()
        samples = collections.defaultdict(list)

        for off, t in jp_runs(rom, lo, hi, keep, esc):
            s = t.strip()
            if not W.looks_like_text(t) or s not in tr:
                continue
            ko = tr[s]
            rel = off - lo
            ent = work.get(rel)
            if ent is None:
                k = "no-worklist"
                blen = 0
            else:
                blen = ent[0]
                if blen < 3:
                    k = "budget"
                elif enc_len(ko) <= blen:
                    k = "fits"
                else:
                    k = "over-budget"
            why[k] += 1
            if len(samples[k]) < a.list:
                samples[k].append((off, blen, t, ko))
            rows.append((fid, off, blen, k, s, ko))

        if not why:
            continue
        grand.update(why)
        print(f"\nfile {fid}: {sum(why.values())} run(s) translated but still Japanese")
        for k, n in why.most_common():
            print(f"    {k:12s} {n:5d}")
            for off, blen, t, ko in samples[k]:
                print(f"        0x{off:06X} b={blen:<3d} {t[:26]!r} -> {ko[:20]!r}")

    print("\ntotal by reason:")
    for k, n in grand.most_common():
        print(f"  {k:12s} {n:5d}")

    if a.out and rows:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write("fid\toffset\tbudget\treason\tjp\tko\n")
            for fid, off, blen, k, jp, ko in rows:
                f.write(f"{fid}\t0x{off:06X}\t{blen}\t{k}\t{jp}\t{ko}\n")
        print(f"\nwrote {len(rows)} rows to {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
