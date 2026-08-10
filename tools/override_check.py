#!/usr/bin/env python3
"""Vet candidate rows for `translation/extra_overrides.tsv` before they go in.

`fit.py` answers "does it fit?". It does not answer the other question an
override raises: **`extra_overrides.tsv` is keyed by the JAPANESE text**, so a
short fragment like 「意する」 or 「探知できる！」 rewrites EVERY worklist row that
carries that string, in every file, not just the one being fixed. A key that
matches more than one row has to be looked at before it is used.

Takes the same `jp<TAB>ko` file the overrides use and prints, per row:
budget fit (plain encoder, the one the build uses), missing glyphs, and every
worklist row the key would hit with its current Korean.

    python tools/override_check.py translation/_pending.tsv
"""
import argparse, glob, io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import koenc

BASE = os.path.join(HERE, "..")
COMMON = os.path.join(BASE, "survey", "common")
FONT = os.path.join(BASE, "survey", "font", "kr_font_map.json")


def encoder():
    return koenc.Encoder({"syl": {k: int(v) for k, v in
                                  json.load(open(FONT, encoding="utf-8")).items()},
                          "one": {}, "raw": {" ": "00"}})


def worklist_rows():
    """jp -> [(fid, offset, budget, current ko)] across every extra worklist."""
    out = {}
    for p in sorted(glob.glob(os.path.join(COMMON, "file*_extra.tsv"))):
        fid = os.path.basename(p).split("file")[-1].split("_")[0]
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            f = ln.split("\t")
            if len(f) >= 5:
                out.setdefault(f[4], []).append(
                    (fid, f[0], int(f[1]), f[5].strip() if len(f) > 5 else ""))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="jp<TAB>ko file (header row skipped)")
    a = ap.parse_args()
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

    enc, rows = encoder(), worklist_rows()
    bad = multi = 0
    for ln in open(a.path, encoding="utf-8").read().splitlines()[1:]:
        f = ln.split("\t")
        if len(f) < 2 or not f[0].strip() or not f[1].strip():
            continue
        jp, ko = f[0].strip(), f[1].strip()
        hits = rows.get(jp, [])
        try:
            n = len(enc.encode(ko))
        except KeyError as e:
            print(f"  !! NO CHARCODE {e}   {jp} -> {ko}")
            bad += 1
            continue
        if not hits:
            print(f"  !! key not in any worklist   {jp} -> {ko}")
            bad += 1
            continue
        b = min(h[2] for h in hits)
        if n > b:
            print(f"  !! +{n - b} over ({n}/{b})   {jp} -> {ko}")
            bad += 1
            continue
        flag = "  " if len(hits) == 1 else "<<"
        print(f"  {flag} {n:>3}/{b:<3} x{len(hits)}  {jp} -> {ko}")
        if len(hits) > 1:
            multi += 1
            for fid, off, bb, cur in hits:
                print(f"        file{fid} {off} budget {bb}  now={cur or '(empty)'}")
    print(f"\n{bad} rejected, {multi} keys hit more than one row (read those)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
