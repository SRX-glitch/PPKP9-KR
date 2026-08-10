#!/usr/bin/env python3
"""Find Korean lines that were clipped to fit a budget that no longer binds.

Early batches were written under a hard inline budget, so trailing punctuation and
particles were shaved off to make lines fit. Since the redirect region exists, any
overlay-28 line whose smallest occurrence is >= 3 bytes can be **any length** -- the
4-byte escape (or the 3-byte banked one) sends it to the region. So a line that
dropped its 。！？」 to save two bytes is now needlessly clipped, and restoring the
punctuation costs nothing.

Reports only what is both wrong and fixable:
  * the Japanese ends with 。！？」 and the Korean does not
  * the line is redirectable (min budget >= 3 and not a choice option, because
    escapes are not intercepted inside a choice block)

    python tools/check_clipped.py            # counts
    python tools/check_clipped.py --list 60  # the rows, ready to edit
"""
import os, sys, glob, argparse, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE = r"C:/Users/jngji/Desktop/실험실"
PROJ = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr"
RUNS = PROJ + r"/survey/ov28/dialogue_runs.tsv"
ORIG = BASE + r"/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
TAIL = "。！？」）★"
MIN_BUDGET = 3


def batches():
    """jp -> (ko, file, lineno), text-keyed worklists only."""
    out = {}
    for fn in sorted(glob.glob(os.path.join(PROJ, "translation", "*.tsv"))):
        b = os.path.basename(fn)
        if b.startswith("worksheet") or b == "intro_lines.tsv":
            continue
        for i, ln in enumerate(open(fn, encoding="utf-8").read().splitlines()[1:], 2):
            p = ln.split("\t")
            if len(p) >= 2 and p[0].strip() and p[-1].strip():
                out.setdefault(p[0], (p[-1], b, i))
    return out


def choice_texts():
    """Japanese that appears inside a choice block -- never redirectable."""
    rom = open(ORIG, "rb").read()
    fat = int.from_bytes(rom[0x48:0x4C], "little")
    lo = int.from_bytes(rom[fat + 25 * 8:fat + 25 * 8 + 4], "little")
    hi = int.from_bytes(rom[fat + 25 * 8 + 4:fat + 25 * 8 + 8], "little")
    spans = []
    i = rom.find(b"\xf8\x15", lo, hi)
    while 0 <= i < hi - 4:
        if rom[i - 1] != 0xF8:
            end = rom.find(b"\xf8\x2d", i, i + 400)
            spans.append((i - lo, (end if end > 0 else i + 200) - lo))
        i = rom.find(b"\xf8\x15", i + 1, hi)
    return spans


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", type=int, default=0)
    a = ap.parse_args()

    tr = batches()
    spans = choice_texts()
    rows = []
    for ln in open(RUNS, encoding="utf-8").read().splitlines():
        p = ln.split("\t")
        if len(p) >= 4:
            rows.append((int(p[0], 16), int(p[1]), p[3]))

    minb = collections.defaultdict(lambda: 1 << 30)
    inchoice = set()
    for off, bud, jp in rows:
        minb[jp] = min(minb[jp], bud)
        if any(s <= off < e for s, e in spans):
            inchoice.add(jp)

    hits = []
    for jp, (ko, fn, lineno) in tr.items():
        if jp not in minb or jp in inchoice:
            continue
        if minb[jp] < MIN_BUDGET:
            continue
        want = jp[-1]
        # ⚠ Only flag a line with NO terminal mark at all. Rendering 「〜のか。」 as
        # 「〜어？」 is correct Korean -- Japanese writes questions with 。 and Korean
        # with ？ -- and demanding the same character appended 。 after ？, which is
        # wrong. That mistake was 20 of the first 46 hits.
        if want in TAIL and not any(ko.endswith(c) for c in TAIL + "～…"):
            hits.append((fn, lineno, minb[jp], jp, ko, want))

    print(f"redirectable lines whose trailing {TAIL} was clipped: {len(hits)}")
    by = collections.Counter(h[5] for h in hits)
    print(f"  by mark: {dict(by)}")
    byfile = collections.Counter(h[0] for h in hits)
    print(f"  top files: {dict(byfile.most_common(6))}")
    if a.list:
        print()
        for fn, lineno, b, jp, ko, want in sorted(hits)[:a.list]:
            print(f"{fn}:{lineno}\tb{b}\t{jp}\t{ko}\t-> {ko}{want}")


if __name__ == "__main__":
    main()
