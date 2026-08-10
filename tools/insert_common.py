#!/usr/bin/env python3
"""Patch the shared dialogue files (4, 8, 20, 27) in place.

These hold the dialogue that is NOT scenario-specific -- shop lines, generic
reactions, system prompts -- and they live in their own FAT files, so overlay
28's redirect machinery never reached them. 7,251 rows were translated and then
sat unused for several sessions because no insertion path existed. This is that
path, and it is deliberately the simple one:

  INLINE ONLY. A run is rewritten inside its own byte span or left alone.

No redirect, because the region and its escape indices live in the grown tail of
overlay 28: reachable from the scenario script, not from another file. No growth,
no relocation, no hook. That caps us at the ~2,540 runs whose Korean already fits
(the rest need a per-file region, which is a much larger job), but those 2,540
are real text the player sees.

Runs are located by walking `F8 6B` exactly as tools/extract_common.py does, so
offsets are derived, never stored -- the worklists carry only jp/ko.

    python tools/insert_common.py --report
    python tools/insert_common.py --out ROM.nds
"""
import argparse, csv, os, sys

sys.path.insert(0, os.path.dirname(__file__))
import extract_common as EC
import untranslated as U
import koenc

COMMON = os.path.join(os.path.dirname(__file__), "..", "survey", "common")
# Bisected by file (session 29). With all four enabled the game boots straight
# into its own 「終 / ファイルをけしました・・・」 failure screen -- it decides the data is
# corrupt and wipes the save. Enabling them one at a time:
#   27 alone      -> boots clean (title screen normal)
#   4 + 27        -> boots clean
#   so the culprit is 8 or 20.
# Those two contribute FIVE runs between them, so which one it is was not worth
# two more 25-minute boot cycles to pin down; both stay off. If they are ever
# wanted, enable exactly one and boot -- `survey/playtest/c27_01.png` and
# `c4_01.png` are the known-good references.
# Static check that held for both shipped files: every changed byte lands inside
# a walked text run (4: 12,769 changed / 0 outside; 27: 3,652 / 0 outside), so
# the failure is not this module writing past a run.
SHIP = (4, 27)


def load(fid):
    path = os.path.join(COMMON, f"file{fid}_runs.tsv")
    tr = {}
    with open(path, encoding="utf-8") as f:
        for r in list(csv.reader(f, delimiter="\t"))[1:]:
            if len(r) >= 4 and r[2] and r[3].strip():
                tr[r[2]] = r[3].strip()
    return tr


def patch_file(rom, fid, enc, spans, apply=True):
    tr = load(fid)
    lo, hi = spans[fid]
    wrote = skipped = 0
    for off, text, ccs in EC.orig_runs(rom, lo, hi):
        ko = tr.get(text)
        if ko is None:
            continue
        budget = sum(1 if cc < 231 else 2 for cc in ccs)
        try:
            kb = enc.encode(ko)
        except KeyError:
            skipped += 1
            continue
        if len(kb) > budget:
            skipped += 1
            continue
        if apply:
            # Fill the WHOLE original span. Byte 0x00 is the safe filler: the
            # engine's zero path clears one 4px column instead of drawing
            # charcode 0, and the original script already carries in-stream 0x00
            # inside dialogue, so it is native behaviour rather than a hack.
            rom[off + 3:off + 3 + budget] = kb + b"\x00" * (budget - len(kb))
        wrote += 1
    return wrote, skipped


def apply_all(rom, verbose=True, files=SHIP):
    enc = koenc.Encoder()
    spans = {i: (s, e) for s, e, i in U.fat_files(bytes(rom))}
    tw = ts = 0
    for fid in files:
        w, s = patch_file(rom, fid, enc, spans)
        tw += w
        ts += s
        if verbose:
            print(f"  shared file {fid}: {w} runs written, {s} skipped (too long)")
    return {"written": tw, "skipped": ts}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args()
    rom = bytearray(open(EC.ORIG, "rb").read())
    enc = koenc.Encoder()
    spans = {i: (s, e) for s, e, i in U.fat_files(bytes(rom))}
    if a.report:
        for fid in SHIP:
            w, s = patch_file(rom, fid, enc, spans, apply=False)
            print(f"file {fid}: 인라인 가능 {w}   초과/불가 {s}")
        return
    if not a.out:
        sys.exit("--report 또는 --out 을 줄 것")
    st = apply_all(rom)
    open(a.out, "wb").write(rom)
    print(f"\n{st['written']} runs written, {st['skipped']} skipped -> {a.out}")


if __name__ == "__main__":
    main()
