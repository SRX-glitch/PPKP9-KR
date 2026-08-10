#!/usr/bin/env python3
"""Check every Korean character name against the GAME'S OWN reading.

The in-game encyclopedia (file 30) stores each person as `名前（よみ）` -- the
game ships its own furigana for 56 names. That is a better authority than any
wiki: it is what this title actually calls them. `survey/common/file30_table.tsv`
already pairs each of those with the Korean we chose, so it is the canonical
spelling list, and any dialogue line that spells the same person differently is
an inconsistency the player will notice.

Found on the first run: 「ピエロ」 was 피에로 in the encyclopedia and 삐에로 in 8
dialogue lines; 「アルベルト」 was 알베르토 vs 알베르트; 「神田奈津姫（かんだなつき）」
is 칸다 나츠키 but the dialogue said 나츠히메 (which is also what the Japanese
wiki says -- the wiki is wrong for this game, the furigana is not).

    python tools/name_consistency.py            # report
    python tools/name_consistency.py --extra    # also check the extra worklists
"""
import argparse, collections, glob, os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLE = os.path.join(BASE, "survey", "common", "file30_table.tsv")
TDIR = os.path.join(BASE, "translation")
COMMON = os.path.join(BASE, "survey", "common")

# Japanese strings that are ordinary words as well as names -- a hit on these is
# almost always the word, not the person (「ムシャ」 is also 「ムシャムシャ」 eating).
AMBIGUOUS = {"ムシャ", "師匠", "番長", "主人公", "ダチョウ", "ワン公", "椿"}


def canonical():
    """name -> the Korean the encyclopedia uses, from the game's own furigana."""
    out = {}
    for line in open(TABLE, encoding="utf-8").read().splitlines():
        f = line.split("\t")
        if len(f) < 6:
            continue
        jp, ko = f[4].replace("\\0", ""), f[5].replace("\\0", "").strip()
        m = re.match(r"^(.+?)（(.+?)）$", jp)
        if not m or not ko:
            continue
        name = m.group(1).replace(" ", "")
        km = re.match(r"^(.+?)（", ko)
        out[name] = (km.group(1) if km else ko).strip()
    return out


def sources(extra):
    for p in sorted(glob.glob(os.path.join(TDIR, "*.tsv"))):
        if os.path.basename(p).startswith("worksheet"):
            continue
        yield p, 0, -1
    if extra:
        for p in sorted(glob.glob(os.path.join(COMMON, "*_extra.tsv"))):
            yield p, 4, 5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--extra", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    canon = {n: k for n, k in canonical().items() if n not in AMBIGUOUS}
    # Longest first so 「神田奈津姫」 is tried before 「神田」.
    names = sorted(canon, key=len, reverse=True)
    bad = collections.defaultdict(list)
    for p, ji, ki in sources(a.extra):
        for line in open(p, encoding="utf-8").read().splitlines():
            f = line.split("\t")
            if len(f) <= max(ji, ki if ki >= 0 else 0):
                continue
            jp, ko = f[ji].strip(), f[ki].strip()
            if not ko or jp == ko:
                continue
            for n in names:
                if n in jp:
                    if canon[n] not in ko:
                        bad[n].append((os.path.basename(p), jp, ko))
                    break            # only the longest matching name counts
    total = sum(len(v) for v in bad.values())
    print(f"encyclopedia spellings: {len(canon)}   inconsistent lines: {total}")
    for n, hits in sorted(bad.items(), key=lambda x: -len(x[1])):
        print(f"\n  {n} -> encyclopedia says 「{canon[n]}」  ({len(hits)} lines)")
        for f, jp, ko in hits[:4]:
            print(f"      {f:<20} {jp!r} -> {ko!r}")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
