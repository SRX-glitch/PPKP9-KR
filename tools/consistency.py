#!/usr/bin/env python3
"""Find Japanese terms that existing translations render inconsistently, and
emit the settled ones as a glossary.

Consistency is the one quality axis a reader notices immediately and that no
per-line check can catch: each line is defensible alone, but a shop called
`대촌` on one screen and `오오무라` on the next reads as a bug. With ~13k lines
registered, the settled renderings are also the fastest way to translate the
rest, so this doubles as the glossary generator.

    python tools/consistency.py                    # conflicts, worst first
    python tools/consistency.py --glossary out.tsv # settled terms -> file

Method: for each Japanese term, take the Korean lines it appears in and find the
most common Hangul stem among them. Grammatical variation shares a stem
(오늘은/오늘도/오늘의 all contain 오늘) and is ignored; a genuine conflict is
when a large share of lines contain no occurrence of the leading stem at all.
"""
import sys, io, os, re, glob, argparse, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"

# Kanji compounds and katakana words carry the names worth policing; kana-only
# strings are grammar and would drown the report in noise.
TERM = re.compile(r"[一-鿿]{2,}|[ァ-ヺー]{3,}")
HAN = re.compile(r"[가-힣]+")


def load_pairs():
    pairs = []
    names = ["common_lines"] + sorted(
        (os.path.splitext(os.path.basename(p))[0]
         for p in glob.glob(f"{BASE}/translation/batch*.tsv")),
        key=lambda n: int(n[5:]))
    for name in names:
        p = f"{BASE}/translation/{name}.tsv"
        if not os.path.exists(p):
            continue
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            q = ln.split("\t")
            if len(q) >= 2 and q[0].strip() and q[1].strip():
                pairs.append((name, q[0].strip(), q[1].strip()))
    return pairs


# Korean attaches grammar to the end of the word, so `방`, `방에`, `방이` are one
# rendering. Comparing raw n-grams instead makes every common noun look
# inconsistent and buries the handful of real conflicts.
PARTICLES = ("에서도", "에게서", "이라도", "으로는", "에게는", "한테는",
             "으로", "에게", "한테", "에서", "이라", "라도", "부터", "까지",
             "보다", "처럼", "만큼", "이나", "이야", "예요", "이다",
             "은", "는", "이", "가", "을", "를", "에", "의", "도", "로",
             "과", "와", "만", "야", "다", "요")


def stem_of(word):
    for p in PARTICLES:                    # longest first, see ordering above
        if len(word) > len(p) and word.endswith(p):
            return word[:-len(p)]
    return word


def stems(ko):
    """Content stems of the line -- the thing a rendering is recognised by."""
    return {stem_of(w) for w in HAN.findall(ko) if len(stem_of(w)) >= 1}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min", type=int, default=3, help="min lines per term")
    ap.add_argument("--show", type=int, default=25)
    ap.add_argument("--coverage", type=float, default=0.7,
                    help="below this share of lines carrying the top stem, flag it")
    ap.add_argument("--glossary", metavar="PATH",
                    help="write settled terms (coverage >= threshold) here")
    a = ap.parse_args()

    pairs = load_pairs()
    print(f"{len(pairs)} translated lines\n")

    seen = collections.defaultdict(list)
    for name, jp, ko in pairs:
        for t in set(TERM.findall(jp)):
            seen[t].append((name, jp, ko))

    # A term's rendering is the stem that is far more common inside its lines
    # than in the corpus at large. Picking the most frequent stem instead just
    # returns whatever ordinary word happened to share the sentence.
    total = len(pairs)
    background = collections.Counter()
    for _, _, ko in pairs:
        background.update(stems(ko))

    conflicts, settled = [], []
    for term, hits in seen.items():
        if len(hits) < a.min:
            continue
        tally = collections.Counter()
        for _, _, ko in hits:
            tally.update(stems(ko))
        scored = []
        for st, c in tally.items():
            if c < 2:
                continue
            lift = (c / len(hits)) / max(background[st] / total, 1e-9)
            if lift >= 3:                  # 3x over chance = plausibly the term
                scored.append((c / len(hits), lift, st, c))
        if not scored:
            continue
        scored.sort(reverse=True)
        top_cov, _, top, top_n = scored[0]
        # Renderings that are neither the leader nor a substring of it
        # (`볼`/`볼을` are one rendering; `볼`/`공` are two).
        rivals = [(cv, st, c) for cv, _, st, c in scored[1:]
                  if st not in top and top not in st]
        if top_cov >= a.coverage or not rivals:
            settled.append((len(hits), term, top, top_cov))
        else:
            conflicts.append((len(hits), top_cov, term, top, top_n, rivals, hits))

    conflicts.sort(key=lambda r: -r[0])
    print(f"{len(conflicts)} terms look inconsistent, {len(settled)} look settled\n")
    for n, cov, term, top, top_n, rivals, hits in conflicts[:a.show]:
        alts = ", ".join(f"{st}({c})" for _, st, c in rivals[:3])
        print(f"■ {term}  {n}줄 —  '{top}' {top_n}줄  vs  {alts}")
        shown = 0
        for name, jp, ko in hits:
            if shown >= 3:
                break
            if top in ko or any(st in ko for _, st, _ in rivals[:2]):
                print(f"   [{name}] {jp}  ->  {ko}")
                shown += 1
        print()

    if a.glossary:
        settled.sort(key=lambda r: -r[0])
        with open(a.glossary, "w", encoding="utf-8") as f:
            f.write("occ\tjp\tko\tcoverage\n")
            for n, term, top, cov in settled:
                f.write(f"{n}\t{term}\t{top}\t{cov:.2f}\n")
        print(f"wrote {a.glossary}: {len(settled)} settled terms")
    return 0


if __name__ == "__main__":
    sys.exit(main())
