#!/usr/bin/env python3
"""Extract the runs that are STILL JAPANESE ON SCREEN and have no Korean yet.

Why a new extractor
-------------------
`survey/common/file*_runs.tsv` reads 5,712/5,712 and 1,539/1,539 translated, and
`file*_extra.tsv` has been worked for sessions -- yet `jp_breakdown` still finds
1,683 untranslated dialogue runs in the built ROM. Every session that has hit
this wall found the same shape of answer: the WALKER missed them, not the
translator (session 30's 111 intro lines, session 35's `F8 15` choice blocks,
session 38's collapsed duplicate sites). So the worksheet has to start from the
walk that PROVES a run is drawn -- `rom_census.src_dialogue`, the same one
`japanese_left`/`jp_breakdown` count with -- rather than from either worklist.

What it emits, per distinct Japanese string:
    occ      how many sites draw it
    budget   the SMALLEST byte span among those sites (the binding constraint;
             `insert_extra` refuses anything longer, and only over-budget rows
             with budget >= redirect_hook.LONG_BUDGET can take the 5-byte escape)
    where    which worklist already owns the site, so the Korean has somewhere
             to go:  extra = file<fid>_extra.tsv row exists (offset path)
                     runs  = file<fid>_runs.tsv row exists (text path)
                     NONE  = nothing owns it -- translating it ships nothing
                             until an extraction pass adds it

⚠ Read `where` before writing any Korean. A NONE row is an extraction bug, and
translating it is work thrown away until that is fixed.

    python tools/untranslated_worksheet.py <built.nds> --fid 4 --n 300 \
           --out translation/f4_s41a.tsv
"""
import os, sys, csv, glob, argparse, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P
import rom_census as R
import walk_file as W
import jp_breakdown as JB

PROJ = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"
COMMON = PROJ + "/survey/common"
ORIG = (r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/"
        r"Power Pro Kun Pocket 9 (Japan).nds")


def fat_lo(b, fid):
    fat = int.from_bytes(b[0x48:0x4C], "little")
    return int.from_bytes(b[fat + fid * 8:fat + fid * 8 + 4], "little")


def extra_offsets(fid):
    """pristine offset -> budget, from file<fid>_extra.tsv (translated or not)."""
    p = f"{COMMON}/file{fid}_extra.tsv"
    out = {}
    if not os.path.exists(p):
        return out
    for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
        f = ln.split("\t")
        if len(f) >= 2:
            out[int(f[0], 16)] = int(f[1])
    return out


def runs_texts(fid):
    """Japanese strings file<fid>_runs.tsv knows about."""
    p = f"{COMMON}/file{fid}_runs.tsv"
    if not os.path.exists(p):
        return set()
    return {r[2] for r in list(csv.reader(open(p, encoding="utf-8"),
                                          delimiter="\t"))[1:]
            if len(r) >= 3 and r[2]}


SOURCES = {"dialogue": R.src_dialogue, "array": R.src_array,
           "packed": R.src_packed}


def _still_japanese(runs, keep, esc):
    """(offset, text, byte length) for runs the build left drawing Japanese.

    The two filters are `jp_breakdown`'s and are not optional -- `keep` stops our
    own Hangul being read back as the kanji those charcodes used to mean, and
    `esc` drops the redirect escape bytes a text walker decodes as characters.
    Generalised here from `JB.jp_runs`, which hard-codes `src_dialogue`.
    """
    out = []
    for off, (t, ccs) in runs.items():
        if off in esc:
            continue
        live = [c for c in ccs if c not in keep]
        if not live:
            continue                       # every charcode is ours -> Korean
        txt = "".join(P.CC2CH.get(c, "") for c in live)
        if any(W.is_jp(c) for c in txt):
            out.append((off, t, sum(1 if c < 231 else 2 for c in ccs)))
    return out


def collect(rom, pristine, fid, tr, keep, esc, sources=("dialogue",)):
    """[(jp, occ, min budget, where, sample pristine offset)] for one file."""
    lo, hi = rom.span(fid)
    if hi <= lo:
        return []
    delta = fat_lo(rom.b, fid) - fat_lo(pristine, fid)
    owned = extra_offsets(fid)
    known = runs_texts(fid)

    runs = {}

    def hit(cc, source, off, text):
        e = runs.setdefault(off, [text, []])
        e[1].append(cc)

    for s in sources:
        SOURCES[s](rom, lo, hi, hit)
    runs = {o: (v[0], v[1]) for o, v in runs.items()}

    agg = collections.defaultdict(lambda: [0, 1 << 30, set(), None])
    for off, t, nb in _still_japanese(runs, keep, esc):
        if not W.looks_like_text(t) or t.strip() in tr:
            continue
        pri = off - delta
        e = agg[t]
        e[0] += 1
        if nb and nb < e[1]:
            e[1] = nb
        e[2].add("extra" if pri in owned else
                 "runs" if t in known else "NONE")
        if e[3] is None:
            e[3] = pri
    out = []
    for t, (occ, nb, where, pri) in agg.items():
        w = "extra" if "extra" in where else "runs" if "runs" in where else "NONE"
        out.append((t, occ, nb if nb < (1 << 30) else 0, w, pri))
    out.sort(key=lambda r: (-r[1], -r[2]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rom")
    ap.add_argument("--fid", type=int, action="append", default=None)
    ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--skip", type=int, default=0)
    ap.add_argument("--out", default=None)
    ap.add_argument("--where", default="extra,runs",
                    help="comma list of owners to emit; add NONE to see the gaps")
    ap.add_argument("--source", default="dialogue",
                    help="census sources to walk: dialogue,array,packed (or all)")
    a = ap.parse_args()
    srcs = (tuple(SOURCES) if a.source == "all"
            else tuple(s for s in a.source.split(",") if s in SOURCES))

    rom = R.Rom(a.rom)
    pristine = open(ORIG, "rb").read()
    tr = JB.translations()
    import japanese_left as JL
    keep = JL.reassigned()
    esc = JL._skip_escapes(rom)
    want = set(a.where.split(","))

    rows, tally = [], collections.Counter()
    for fid in (a.fid or [25, 4, 27, 20, 13, 30, 18, 8]):
        for t, occ, nb, w, pri in collect(rom, pristine, fid, tr, keep, esc, srcs):
            tally[(fid, w)] += occ
            if w in want:
                rows.append((fid, t, occ, nb, w, pri))
    rows.sort(key=lambda r: (-r[2], -r[3]))

    print(f"untranslated, by file and owner (occurrences):")
    for (fid, w), n in sorted(tally.items(), key=lambda kv: -kv[1]):
        print(f"  f{fid:<3d} {w:6s} {n:6,}")

    picked = rows[a.skip:a.skip + a.n]
    out = a.out or f"{PROJ}/translation/untranslated_worksheet.tsv"
    if not os.path.isabs(out):
        out = os.path.join(PROJ, out)
    with open(out, "w", encoding="utf-8", newline="") as f:
        f.write("fid\tocc\tbudget\tmax\twhere\toffset\tjp\tko\n")
        for fid, t, occ, nb, w, pri in picked:
            f.write(f"{fid}\t{occ}\t{nb}\t{nb // 2}\t{w}\t0x{pri:06X}\t{t}\t\n")
    print(f"\n{out}: {len(picked)} rows of {len(rows)} eligible "
          f"(owners {sorted(want)})")


if __name__ == "__main__":
    main()
