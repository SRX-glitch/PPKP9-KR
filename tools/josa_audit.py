#!/usr/bin/env python3
"""Find runs whose opening particle disagrees with the run before it.

The engine prints consecutive runs with no gap, and a sentence is routinely split
across them -- often with a NAME slot in the middle. So a run that starts with a
Korean particle has to agree with the last syllable of the *previous* run, and
nothing in the pipeline ever checked that:

    0x059E8D  おせっかい野郎 -> 오지랖 넓은 놈      (ends on a batchim)
    0x059E98  だな。         -> 로군。             (the vowel form)
    on screen: 「오지랖 넓은 놈로군。」             <- 「놈이로군。」

This is not a byte problem -- the offsets, the budgets and the escapes are all
correct, which is exactly why every existing gate is silent about it. It is only
visible if you know Korean morphology, so encode the morphology.

Adjacency comes from `survey/ov28/dialogue_runs.tsv` read in OFFSET order, the
same ground truth session 34 used for the batch120 shift. The shipped Korean is
`translation/batch*.tsv` with later batches overriding earlier ones.

    python tools/josa_audit.py            # list the disagreements
    python tools/josa_audit.py --fixes    # print jp<TAB>ko lines to paste
"""
import argparse, glob, io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "..")
RUNS = os.path.join(BASE, "survey", "ov28", "dialogue_runs.tsv")
TDIR = os.path.join(BASE, "translation")

# (form used after a final consonant, form used after a vowel).
# Only pairs where BOTH spellings are real words on their own would be ambiguous;
# these are all unambiguous sentence-openers.
PAIRS = [("은", "는"), ("이", "가"), ("을", "를"), ("과", "와"),
         ("으로", "로"), ("이라", "라"), ("이랑", "랑"), ("이야", "야"),
         ("이다", "다"), ("이군", "군"), ("이네", "네"), ("이지", "지"),
         ("이에요", "예요"), ("이여", "여"), ("이란", "란"), ("이든", "든"),
         # Copula endings need the WHOLE ending as the pair, not just 이/-, or the
         # "particle stands alone" filter below throws them away: 「로군。」 has 군
         # after 로, so the pair has to be ("이로군", "로군").
         ("이로군", "로군"), ("이구나", "구나"), ("이었", "였"),
         ("이라고", "라고"), ("이겠", "겠"), ("이네요", "네요")]
HANGUL = re.compile(r"[가-힣]")
# Japanese particles a continuation run opens with. If the source does not start
# with one of these, the Korean run is not a particle continuation at all.
JP_PARTICLE = ("は", "が", "を", "に", "で", "と", "の", "も", "や", "へ",
               "だ", "です", "から", "まで", "より", "って", "という")
TAIL_OK = "。！？、）」・~～… "


def has_batchim(ch):
    return (ord(ch) - 0xAC00) % 28 != 0


def _batches():
    """jp -> ko, later batch numbers overriding earlier ones."""
    def key(p):
        m = re.search(r"batch(\d+)", os.path.basename(p))
        return int(m.group(1)) if m else 0
    out = {}
    for p in sorted(glob.glob(os.path.join(TDIR, "batch*.tsv")), key=key):
        for ln in open(p, encoding="utf-8").read().splitlines():
            f = ln.split("\t")
            if len(f) >= 2 and f[0].strip() and f[1].strip():
                out[f[0].strip()] = f[1].strip()
    return out


def _runs():
    out = []
    for ln in open(RUNS, encoding="utf-8").read().splitlines():
        f = ln.split("\t")
        if len(f) >= 4:
            try:
                out.append((int(f[0], 16), int(f[1]), f[3]))
            except ValueError:
                pass
    out.sort()
    return out


def audit():
    tr, runs = _batches(), _runs()
    hits = []
    for (o1, b1, jp1), (o2, b2, jp2) in zip(runs, runs[1:]):
        # only judge runs the engine really prints back to back
        if o2 - o1 > 64:
            continue
        ko1, ko2 = tr.get(jp1, ""), tr.get(jp2, "")
        if not ko1 or not ko2:
            continue
        prev = ko1.rstrip()
        if not prev or not HANGUL.match(prev[-1]):
            continue                       # ends on punctuation: nothing to agree with
        if prev[-1] in "。！？、）」":
            continue
        # Two filters, without which this drowns in false positives: 「이 가게는」
        # and 「가르쳐」 and 「이라서」 all *start* with a particle spelling but are
        # ordinary words. A real case has (a) Japanese that opens with a particle
        # too, and (b) the Korean particle standing alone -- next char is a space,
        # punctuation, or the end of the run.
        if not jp2.startswith(JP_PARTICLE):
            continue
        for cons, vow in PAIRS:
            want = cons if has_batchim(prev[-1]) else vow
            other = vow if want is cons else cons
            if not ko2.startswith(other) or ko2.startswith(want):
                continue
            rest = ko2[len(other):]
            if rest and not (rest[0].isspace() or rest[0] in TAIL_OK):
                continue
            hits.append((o1, jp1, ko1, o2, jp2, ko2, other, want))
            break
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixes", action="store_true")
    a = ap.parse_args()
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    hits = audit()
    print(f"# {len(hits)} runs open with the wrong particle for the run before them\n")
    for o1, jp1, ko1, o2, jp2, ko2, got, want in hits:
        if a.fixes:
            print(f"{jp2}\t{want + ko2[len(got):]}")
        else:
            print(f"0x{o1:06X} {jp1} -> {ko1}")
            print(f"0x{o2:06X} {jp2} -> {ko2}"
                  f"      reads 「{ko1}{ko2}」, wants 「{want}…」")
            print()


if __name__ == "__main__":
    main()
