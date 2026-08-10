#!/usr/bin/env python3
"""Byte-fit checker for candidate Korean, so wording can be chosen before merging.

`merge_extra --over` only reports rows that are already merged, which makes
revising a phrase a three-step round trip. This takes `jp<TAB>ko` lines on stdin
(or `--jp`/`--ko`) and prints the run's real budget next to what the candidate
costs, using the same plain encoder the build uses.

Why it matters: the budget is rarely the reason a line reads stiffly. 「命の恩人
みたいな物だろう？」 has 17 bytes; 「목숨 은인이잖아？」 (16 B) and 「생명의 은인이지？」
(16 B) both fit, and only the second reads like Korean. Check candidates instead
of mechanically dropping particles to make the first one fit.

    printf '命の恩人みたいな物だろう？\t생명의 은인이지？\n' | python tools/fit.py
    python tools/fit.py --jp '…' --ko '…' --ko '…'      # compare wordings
"""
import os, sys, io, json, glob, argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import koenc

BASE = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"
COMMON = BASE + "/survey/common"
FONTDIR = BASE + "/survey/font"


def encoder():
    fontmap = {k: int(v) for k, v in
               json.load(open(os.path.join(FONTDIR, "kr_font_map.json"),
                              encoding="utf-8")).items()}
    return koenc.Encoder({"syl": fontmap, "one": {}, "raw": {" ": "00"}})


def budgets():
    """jp -> smallest budget across every extra worklist it appears in."""
    out = {}
    for p in sorted(glob.glob(f"{COMMON}/file*_extra.tsv")):
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            f = ln.split("\t")
            if len(f) >= 5:
                b = int(f[1])
                if f[4] not in out or b < out[f[4]]:
                    out[f[4]] = b
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jp")
    ap.add_argument("--ko", action="append", default=[])
    a = ap.parse_args()
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    enc, bud = encoder(), budgets()

    pairs = [(a.jp, k) for k in a.ko] if a.jp else [
        (ln.split("\t")[0], ln.split("\t")[1])
        for ln in sys.stdin.read().splitlines() if "\t" in ln]

    for jp, ko in pairs:
        b = bud.get(jp)
        try:
            n = len(enc.encode(ko))
        except KeyError as e:
            print(f"  ??  {ko}   <- no charcode ({e}); run build_fontpack.py")
            continue
        if b is None:
            print(f"  ??  {ko}   ({n} B; jp not found in any worklist)")
        else:
            mark = "OK " if n <= b else f"+{n - b}"
            print(f"  {mark} {n:>3}/{b:<3} {ko}")


if __name__ == "__main__":
    main()
