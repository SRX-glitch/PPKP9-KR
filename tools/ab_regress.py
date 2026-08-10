#!/usr/bin/env python3
"""Which runs went BACKWARDS between two builds?

The user's report after session 39: some lines that used to be Korean are
Japanese again. That is the question a coverage percentage cannot answer -- two
builds can sit at the same percentage while trading thousands of lines.

Definition used here, and it is deliberately map-independent:

    a run is STILL JAPANESE  <=>  its bytes are byte-identical to the pristine ROM

That works across builds whose font maps differ (kr_map.json is rewritten every
time the allocation changes, so "does this charcode mean Hangul" is not
comparable between two ROMs -- but "did the build touch these bytes" is).

Offsets are file-relative, because the build relocates overlays and the same run
sits at a different absolute offset in each ROM.

    python tools/ab_regress.py <old.nds> <new.nds>
    python tools/ab_regress.py <old.nds> <new.nds> --list 40
"""
import os, sys, argparse, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P
import rom_census as R
import walk_file as W

FILES = (25, 4, 27, 20, 30, 18, 8, 13)


def pristine_runs(rom, fid):
    """[(rel_off, nbytes, jp)] -- dialogue runs as they are in the ORIGINAL ROM."""
    lo, hi = rom.span(fid)
    seen, out = set(), []
    buf = []

    def hit(cc, source, off, text):
        buf.append((off, text))

    R.src_dialogue(rom, lo, hi, hit)
    for off, t in buf:
        if off in seen:
            continue
        seen.add(off)
        nb = len(b"".join(P.cc_to_bytes(P.CH2CC[c]) for c in t if c in P.CH2CC))
        if nb and any(W.is_jp(c) for c in t):
            out.append((off - lo, nb, t))
    return out


def still_japanese(rom, fid, runs, pristine):
    """set of rel_offs whose bytes this ROM left untouched"""
    lo, _hi = rom.span(fid)
    plo, _ = pristine.span(fid)
    out = set()
    for rel, nb, _t in runs:
        if rom.b[lo + rel:lo + rel + nb] == pristine.b[plo + rel:plo + rel + nb]:
            out.add(rel)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("old")
    ap.add_argument("new")
    ap.add_argument("--list", type=int, default=12)
    a = ap.parse_args()

    pr = R.Rom()
    old = R.Rom(a.old)
    new = R.Rom(a.new)
    print(f"old = {os.path.basename(a.old)}\nnew = {os.path.basename(a.new)}\n")

    tot_reg, tot_gain = [], []
    for fid in FILES:
        if pr.span(fid)[1] <= pr.span(fid)[0]:
            continue
        runs = pristine_runs(pr, fid)
        if not runs:
            continue
        jo = still_japanese(old, fid, runs, pr)
        jn = still_japanese(new, fid, runs, pr)
        reg = jn - jo            # was translated, now Japanese
        gain = jo - jn           # was Japanese, now translated
        txt = {r: t for r, _n, t in runs}
        tot_reg += [(fid, r, txt[r]) for r in reg]
        tot_gain += [(fid, r, txt[r]) for r in gain]
        print(f"f{fid:<3d} runs {len(runs):6,}  japanese old {len(jo):6,} "
              f"-> new {len(jn):6,}   REGRESSED {len(reg):5,}  gained {len(gain):5,}")

    print(f"\nTOTAL regressed {len(tot_reg):,}  gained {len(tot_gain):,}")
    print("\nregressed (was Korean, now Japanese):")
    for fid, r, t in tot_reg[:a.list]:
        print(f"   f{fid:<3d} +0x{r:06X}  {t[:44]}")
    if len(tot_reg) > a.list:
        print(f"   ... and {len(tot_reg) - a.list:,} more")

    c = collections.Counter(t for _f, _r, t in tot_reg)
    print("\nmost-repeated regressed lines:")
    for t, n in c.most_common(10):
        print(f"   {n:4d}x  {t[:44]}")


if __name__ == "__main__":
    main()
