#!/usr/bin/env python3
"""Shorten choice-option translations until they fit their byte budget.

Choice options cannot be redirected -- the escape is not intercepted on that
screen, so an over-budget option has to either fit inline or stay Japanese
(build_kr excludes them from the redirect set for exactly this reason). Hand
shortening is slow and, worse, unverified: a first pass of 67 rewrites gained
only 19 fits because nothing checked them against the budget.

So this generates candidates mechanically and keeps the first that ACTUALLY
encodes within budget, using the same encoder and the same MTE-expansion slack
rule the build uses. Nothing is written that has not been verified.

Candidates, cheapest damage first:
  1. as-is
  2. drop the trailing 。
  3. drop 、 (a choice label rarely needs it)
  4. drop spaces
  5. combinations of the above
  6. plain encoding (no MTE) -- fixes the case where the text FITS but an MTE
     entry's expansion tail would be cut, which is 43 options on its own

    python tools/fit_choices.py --report
    python tools/fit_choices.py --write        # -> translation/batch126.tsv
"""
import argparse, glob, json, os, sys

sys.path.insert(0, os.path.dirname(__file__))
import koenc

BASE = r"C:/Users/jngji/Desktop/실험실"
ORIG = BASE + r"/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
OV = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/ov28"
TRANS = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/translation"
FONT = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font/kr_map.json"


def slack_ok(b, budget, expand):
    """Does every MTE expansion finish before the run ends? (see build_kr)"""
    codes, j = [], 0
    while j < len(b):
        if b[j] <= 231:
            j += 1
            continue
        cc = 256 + (b[j] - 232) * 256 + b[j + 1]
        n = expand.get(cc)
        codes.append((j + 2, (n - 1) if n else 0))
        j += 2
    for k, (end, debt) in enumerate(codes):
        if debt and budget - end < sum(d for _, d in codes[k:]):
            return False
    return True


def choice_budgets():
    rom = open(ORIG, "rb").read()
    f = int.from_bytes(rom[0x48:0x4C], "little")
    lo = int.from_bytes(rom[f + 25 * 8:f + 25 * 8 + 4], "little")
    hi = int.from_bytes(rom[f + 25 * 8 + 4:f + 25 * 8 + 8], "little")
    spans, i = [], rom.find(b"\xf8\x15", lo, hi)
    while 0 <= i < hi - 4:
        if rom[i - 1] != 0xF8:
            e = rom.find(b"\xf8\x2d", i, i + 400)
            spans.append((i - lo, (e if e > 0 else i + 200) - lo))
        i = rom.find(b"\xf8\x15", i + 1, hi)
    out = {}
    for ln in open(os.path.join(OV, "dialogue_runs.tsv"), encoding="utf-8"):
        p = ln.rstrip("\n").split("\t")
        if len(p) < 4:
            continue
        o = int(p[0], 16)
        if any(s <= o < e for s, e in spans):
            out[p[3]] = min(out.get(p[3], 1 << 30), int(p[1]))
    return out


def candidates(ko):
    """Cheapest damage first, and never at the cost of readability.

    Stripping spaces is the biggest byte win (1 each) but Korean without word
    spacing gets hard to read fast: 「오늘 쇼핑 좀 같이 안 갈래？」 collapsing to
    「오늘쇼핑좀같이안갈래？」 is technically in budget and not worth shipping. So
    space removal is only offered when the label has at most two spaces --
    enough for 「그런 걸로 해두자」, refused for a whole sentence.
    """
    seen, out = set(), []
    def add(s):
        if s and s not in seen:
            seen.add(s)
            out.append(s)
    def readable(s):
        """Reject a candidate whose Hangul runs too long without a space.

        The guard has to be on the RESULT, not the input: 「그러니까 걱정하는 거잖아」
        has only two spaces, so an input-side test lets it through, and the
        stripped 「그러니까걱정하는거잖아」 is what actually ships. Five syllables is
        about where an unspaced Korean run stops being scannable at 12px.
        """
        import re
        return max((len(r) for r in re.findall(r"[가-힣]+", s)), default=0) <= 5

    add(ko)
    a = ko.rstrip("。")
    add(a)
    # Space removal is tried BEFORE comma removal. Both save one byte, but
    # dropping 「、」 fuses two clauses into nonsense (「응、이제 괜찮아」 ->
    # 「응이제 괜찮아」) while dropping a space only tightens spacing.
    for c in (ko.replace(" ", ""), a.replace(" ", ""),
              ko.rstrip("。！？").replace(" ", "")):
        if readable(c):
            add(c)
    add(a.replace("、", ""))
    c = a.replace("、", "").replace(" ", "")
    if readable(c):
        add(c)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--out", default=os.path.join(TRANS, "batch126.tsv"))
    a = ap.parse_args()

    m = json.load(open(FONT, encoding="utf-8"))
    enc = koenc.Encoder(m)
    plain = koenc.Encoder({**m, "mte": {}})
    expand = {int(v): len(k) for k, v in m["mte"].items()}

    tr = {}
    for f in sorted(glob.glob(os.path.join(TRANS, "batch*.tsv"))):
        for ln in open(f, encoding="utf-8").read().splitlines()[1:]:
            p = ln.rstrip("\r").split("\t")
            if len(p) >= 2 and p[0] and p[1]:
                tr[p[0]] = p[1]

    fixed, already, stuck = {}, 0, []
    for jp, budget in choice_budgets().items():
        ko = tr.get(jp)
        if ko is None:
            continue
        def fits(s):
            for e in (enc, plain):
                try:
                    b = e.encode(s)
                except KeyError:
                    continue
                if len(b) <= budget and slack_ok(b, budget, expand):
                    return True
            return False
        if fits(ko):
            already += 1
            continue
        hit = next((c for c in candidates(ko) if fits(c)), None)
        if hit:
            fixed[jp] = hit
        else:
            stuck.append((budget, jp, ko))

    print(f"이미 들어가는 선택지      : {already}")
    print(f"기계적 축약으로 해결      : {len(fixed)}")
    print(f"여전히 안 되는 것         : {len(stuck)}")
    if a.report:
        for jp, ko in list(fixed.items())[:20]:
            print(f"   {jp[:22]!r:26} -> {ko!r}")
    if a.write and fixed:
        with open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write("jp\tko\n")
            for jp, ko in fixed.items():
                f.write(f"{jp}\t{ko}\n")
        print(f"\n{a.out} 에 {len(fixed)}줄 기록")


if __name__ == "__main__":
    main()
