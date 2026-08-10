#!/usr/bin/env python3
"""The remaining Japanese: is it a capacity problem or a translation problem?

`japanese_left.py` says how much is left. It cannot say what to DO about it, and
those are different jobs with different owners:

    translated, not shipped   we already have the Korean and the build dropped it
                              (region cap, byte budget, no redirect path) -> a
                              capacity/pipeline fix wins it back for free
    not translated            nobody has written the Korean yet -> translation work
    not real text             the walker decoded binary as text -> noise, ignore

Getting this wrong is expensive in both directions: chasing capacity when the
text was never translated buys nothing, and translating what the build is
silently dropping is work thrown away.

    python tools/jp_breakdown.py <built.nds>
"""
import os, sys, glob, argparse, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P
import rom_census as R
import walk_file as W

PROJ = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"


def translations():
    """every Japanese string we have Korean for, from every source the build reads"""
    out = set()
    for fn in sorted(glob.glob(PROJ + "/translation/*.tsv")):
        if os.path.basename(fn).startswith("worksheet"):
            continue
        for ln in open(fn, encoding="utf-8").read().splitlines()[1:]:
            p = ln.split("\t")
            if len(p) >= 2 and p[0].strip() and p[1].strip():
                out.add(p[0].strip())
            if len(p) >= 3 and p[0].startswith("0x") and p[2].strip():
                out.add(p[1].strip())
    for fn in sorted(glob.glob(PROJ + "/survey/common/*.tsv")):
        for ln in open(fn, encoding="utf-8").read().splitlines()[1:]:
            p = ln.split("\t")
            if len(p) >= 4 and p[3].strip():
                out.add(p[2].strip())
            if len(p) >= 6 and p[5].strip():
                out.add(p[4].strip())
    return out


def jp_runs(rom, lo, hi, keep, esc):
    """dialogue runs that are STILL JAPANESE ON SCREEN, as (offset, text).

    ⛔ Two filters that are not optional, both learned the hard way:

    `keep`  charcodes the font pack reassigned to Hangul. Decoding the built ROM
            with poketbl alone reads our own Korean back as the kanji those
            charcodes used to mean -- the first version of this tool filed
            「茜瑛蛾」 as untranslated Japanese when it is Korean on screen.

    `esc`   bytes belonging to our redirect escapes. `F7` is below 0xF8 so a text
            walker starts a run on it and decodes the offset payload as
            characters (「ｳむそ」). The hook consumes those; nothing is drawn.
    """
    out, buf = [], []

    def hit(cc, source, off, text):
        buf.append((off, cc, text))

    R.src_dialogue(rom, lo, hi, hit)
    runs = {}
    for off, cc, t in buf:
        runs.setdefault(off, (t, []))[1].append(cc)
    for off, (t, ccs) in runs.items():
        if off in esc:
            continue
        live = [c for c in ccs if c not in keep]
        if not live:
            continue                       # every charcode is ours -> Korean
        txt = "".join(P.CC2CH.get(c, "") for c in live)
        if any(W.is_jp(c) for c in txt):
            out.append((off, txt))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rom")
    ap.add_argument("--list", type=int, default=6)
    a = ap.parse_args()

    rom = R.Rom(a.rom)
    tr = translations()
    import japanese_left as JL
    keep = JL.reassigned()
    esc = JL._skip_escapes(rom)
    print(f"translation corpus: {len(tr):,} distinct Japanese strings; "
          f"{len(keep)} charcodes reassigned, {len(esc):,} bytes are escapes")

    tally = collections.Counter()
    per_file = collections.defaultdict(collections.Counter)
    samples = collections.defaultdict(list)
    for fid in (25, 4, 27, 20, 13, 30, 18, 8):
        lo, hi = rom.span(fid)
        if hi <= lo:
            continue
        for off, t in jp_runs(rom, lo, hi, keep, esc):
            if not W.looks_like_text(t):
                k = "not real text"
            elif t.strip() in tr:
                k = "translated, not shipped"
            else:
                k = "not translated"
            tally[k] += 1
            per_file[fid][k] += 1
            if len(samples[k]) < a.list:
                samples[k].append((fid, off, t))

    tot = sum(tally.values())
    print(f"\nstill-Japanese dialogue runs in the built ROM: {tot:,}")
    for k in ("translated, not shipped", "not translated", "not real text"):
        n = tally[k]
        print(f"  {k:26s} {n:7,}  {n / tot * 100:5.1f}%")
        for fid, off, t in samples[k]:
            print(f"        f{fid:<3d} 0x{off:06X}  {t[:44]}")
    print("\nby file:")
    for fid, c in sorted(per_file.items(), key=lambda kv: -sum(kv[1].values())):
        print(f"  f{fid:<3d} shipped-miss {c['translated, not shipped']:6,}  "
              f"untranslated {c['not translated']:6,}  "
              f"noise {c['not real text']:6,}")


if __name__ == "__main__":
    main()
