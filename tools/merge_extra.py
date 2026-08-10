#!/usr/bin/env python3
"""Merge `translation/file*_ko*.tsv` staging files into the `file*_extra.tsv` worklists.

`insert_extra.py` reads the `ko` column of `survey/common/file{N}_extra.tsv` and
writes it at the recorded offset. Editing a 12,000-row worklist by hand is not a
workflow, so translation is staged in flat `jp\tko` files and merged here.

Every merged row is fit-checked with the SAME plain encoder the build uses
(`enc_plain` -- no MTE: the MTE hook only expands inside overlay 28's walker, and
these runs live in files 4/25/27). A row whose Korean does not fit its budget is
still merged, but reported, because `insert_extra` would silently skip it and the
line would ship in Japanese with nothing to say why.

    python tools/merge_extra.py             # merge + report
    python tools/merge_extra.py --check     # report only, write nothing
    python tools/merge_extra.py --over      # list the over-budget rows to shorten
"""
import os, sys, glob, argparse, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import koenc
import poketbl as P

BASE = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"
COMMON = BASE + "/survey/common"
TDIR = BASE + "/translation"
FONTDIR = BASE + "/survey/font"
# The worklists insert_extra ships plus the ones staged for it.
# ⭐ SESSION 41: 18/20/30 joined the list when `insert_extra.SHIP_LATE` started
# writing them. Without them a staged row for those files merges NOWHERE and the
# `--check` report reads "+0 merged" with no error -- the translation is simply
# lost. ⚠ Only 4/27 (side_region) and 30 (tail_region) have a redirect path, so
# an over-budget row in 18/20 really is dropped; that is what the report is for.
# File 8 is here for STAGING only -- `insert_extra` never writes it (its rows are
# pointered, and `insert_file8.apply_orphans` reads them back through
# `IX.WORK(8)`), but without it a staged file-8 row merges nowhere, exactly like
# 18/20/30 did before session 41.
FILES = (4, 8, 18, 20, 25, 27, 30)


def plain_encoder():
    """The encoder build_kr calls `enc_plain`: complete Hangul font pack, raw-byte
    space, and NO MTE dictionary. Using the on-disk kr_map.json instead would
    quietly bring the MTE entries in and under-count every line's bytes."""
    fontmap = {k: int(v) for k, v in
               json.load(open(os.path.join(FONTDIR, "kr_font_map.json"),
                              encoding="utf-8")).items()}
    return koenc.Encoder({"syl": fontmap, "one": {}, "raw": {" ": "00"}})


def _pairs(path):
    for ln in open(path, encoding="utf-8").read().splitlines()[1:]:
        f = ln.split("\t")
        if len(f) >= 2 and f[0].strip() and f[1].strip():
            yield f[0].strip(), f[1].strip()


def staged():
    out = {}
    for p in sorted(glob.glob(f"{TDIR}/file*_ko*.tsv")):
        out.update(_pairs(p))
    return out


def overrides():
    """Corrections that REPLACE a `ko` already in a worklist.

    Staging files only fill empty cells, so a translation that turned out not to
    fit its budget could not be revised through them -- and relying on the
    staging files' alphabetical sort order to shadow each other is exactly the
    kind of invisible rule that goes wrong silently. Overrides are explicit,
    applied last, and every replacement is printed."""
    p = f"{TDIR}/extra_overrides.tsv"
    return dict(_pairs(p)) if os.path.exists(p) else {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--over", action="store_true")
    a = ap.parse_args()

    enc = plain_encoder()
    tr = staged()
    ov = overrides()
    print(f"[staged] {len(tr)} jp->ko pairs from translation/file*_ko*.tsv, "
          f"{len(ov)} overrides")

    grand = {"merged": 0, "already": 0, "replaced": 0, "over": 0, "unmapped": 0}
    over_rows = []
    for fid in FILES:
        path = f"{COMMON}/file{fid}_extra.tsv"
        lines = open(path, encoding="utf-8").read().splitlines()
        head, body = lines[0], lines[1:]
        out, merged, already, over, repl = [], 0, 0, 0, 0
        for ln in body:
            f = ln.split("\t")
            if len(f) < 5:
                out.append(ln)
                continue
            while len(f) < 6:
                f.append("")
            jp, ko = f[4], f[5].strip()
            if not ko and jp in tr:
                ko = tr[jp]
                merged += 1
            elif ko:
                already += 1
            if jp in ov and ov[jp] != ko:
                print(f"  ~~ file{fid} {f[0]} override: {ko or '(empty)'} -> {ov[jp]}")
                ko = ov[jp]
                repl += 1
            if ko:
                try:
                    n = len(enc.encode(ko))
                except KeyError as e:
                    # Do NOT clear the cell. The font pack is regenerated at the
                    # top of every build from these very columns, so a syllable
                    # missing HERE usually just means kr_font_map.json is stale --
                    # wiping the Korean to "fix" that destroyed the translation
                    # and then hid it from the regeneration that would have
                    # added the glyph. Warn and leave the work alone.
                    grand["unmapped"] += 1
                    print(f"  !! file{fid} {f[0]} no charcode: {e}"
                          f"\n     (run tools/build_fontpack.py and re-check; "
                          f"if it persists the pack is slot-limited)")
                else:
                    if n > int(f[1]):
                        over += 1
                        over_rows.append((fid, f[0], int(f[1]), n, jp, ko))
            f[5] = ko
            out.append("\t".join(f))
        if not a.check:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(head + "\n" + "\n".join(out) + "\n")
        print(f"  file {fid}: +{merged} merged, {already} already present, "
              f"{repl} overridden, {over} over budget")
        grand["merged"] += merged
        grand["already"] += already
        grand["replaced"] += repl
        grand["over"] += over

    if a.over:
        print(f"\n-- {len(over_rows)} over-budget rows (shorten these) --")
        for fid, off, b, n, jp, ko in sorted(over_rows, key=lambda r: r[3] - r[2],
                                             reverse=True):
            print(f"  f{fid} {off} budget {b} need {n} (+{n - b})  {jp}  ->  {ko}")
    print(f"\n{grand}")
    if a.check:
        print("(--check: nothing written)")


if __name__ == "__main__":
    main()
