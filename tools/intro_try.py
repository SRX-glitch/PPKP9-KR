#!/usr/bin/env python3
"""Score candidate intro wordings against the CURRENT MTE dictionary.

Polishing the opening is a search for wordings that read naturally AND fit an
in-place budget. Two costs matter and they are not the same:

  plain  -- bytes with no dictionary help (2 B per Hangul syllable)
  mte    -- bytes using the entries the dictionary ALREADY has, which are free:
            no slot is consumed, nothing is evicted

A wording that fits on `mte` alone is the cheapest possible outcome. One that
needs a NEW entry costs a dictionary slot (222 total, code-limited), so it has
to earn it -- and a substring that recurs across several lines earns it far more
easily than a one-off.

    python tools/intro_try.py 0x330785 "지금 우주엔"      # score one candidate
    python tools/intro_try.py --audit                     # every current line
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import koenc

BASE = r"C:/Users/jngji/Desktop/실험실"
ROM = BASE + r"/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
TSV = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/translation/intro_lines.tsv"
FONT = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font/kr_font_map.json"
KRMAP = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font/kr_map.json"


def load():
    fontmap = json.load(open(FONT, encoding="utf-8"))
    mte = json.load(open(KRMAP, encoding="utf-8")).get("mte", {})
    base = {"syl": fontmap, "one": {}, "raw": {" ": "00"}}
    return koenc.Encoder(base), koenc.Encoder({**base, "mte": mte}), mte


def budgets():
    """offset -> (byte budget, jp, current ko), budget measured from the ROM."""
    import poketbl as P
    rom = open(ROM, "rb").read()
    out = {}
    for ln in open(TSV, encoding="utf-8").read().splitlines()[1:]:
        p = ln.split("\t")
        if len(p) < 3 or not p[0].strip():
            continue
        off, jp, ko = int(p[0], 16), p[1].strip(), p[2].strip()
        n = 0
        for ch in jp:
            n += 1 if P.CH2CC[ch] < 231 else 2
        out[off] = (n, jp, ko)
    return out


def hits(mte, s):
    """Which existing dictionary entries this string would use."""
    got, i = [], 0
    for sub in sorted(mte, key=len, reverse=True):
        pass
    order = sorted(mte, key=len, reverse=True)
    while i < len(s):
        h = next((x for x in order if s.startswith(x, i)), None)
        if h:
            got.append(h)
            i += len(h)
        else:
            i += 1
    return got


def score(plain, enc, mte, budget, ko):
    p, m = len(plain.encode(ko)), len(enc.encode(ko))
    tag = "OK " if m <= budget else "OVER"
    return f"{tag} {m:2d}/{budget:2d}B (plain {p:2d}) {ko!r} via {hits(mte, ko)}"


def main():
    plain, enc, mte = load()
    b = budgets()
    if len(sys.argv) > 1 and sys.argv[1] == "--audit":
        for off in sorted(b):
            n, jp, ko = b[off]
            print(f"0x{off:06X} {score(plain, enc, mte, n, ko)}  <- {jp}")
        return
    off = int(sys.argv[1], 16)
    n, jp, cur = b[off]
    print(f"0x{off:06X} budget {n}B  jp={jp!r}")
    print(f"  now: {score(plain, enc, mte, n, cur)}")
    for cand in sys.argv[2:]:
        print(f"  try: {score(plain, enc, mte, n, cand)}")


if __name__ == "__main__":
    main()
