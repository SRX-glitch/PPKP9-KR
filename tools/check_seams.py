#!/usr/bin/env python3
"""Find places where two adjacent runs' Korean reads badly when concatenated.

The script splits a line into runs at inline control codes, and the engine draws
them back to back with nothing between. Japanese survives that because its
punctuation rides inside the fragment: 「な、」+「なんだと」 reads 「な、なんだと」. Korean
loses it whenever the fragment is too small to hold the comma -- 「な、」 has a
2-byte budget and 「뭐、」 needs 3, so it shipped as 「뭐」 and the box drew 「뭐뭐라고」.

The fix is to move the punctuation to the FRONT of the following run, which is
usually much roomier. It is the seam that is wrong, not either translation.

    python tools/check_seams.py            # suspicious seams
    python tools/check_seams.py --all      # every seam whose JP fragment ends in 、
"""
import os, sys, glob, argparse, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"
RUNS = BASE + r"/survey/ov28/dialogue_runs.tsv"
OV = BASE + r"/survey/ov28/ov28.bin"


def in_message():
    """Offsets that live inside an `F8 6B` message, as a set of ranges.

    ⚠ Without this the seam report is meaningless. `dialogue_runs.tsv` also holds
    binary data records on an 8-byte stride whose bytes decode to kana (`み` 44
    times, `のの` 33, `むむ` 30 …). They are adjacent to each other by construction,
    so every heuristic for "adjacent runs" picks them up: the unfiltered report
    cried 891 seams, and the overwhelming majority were data no player ever sees.
    Only script reached from a message opener can appear on screen.
    """
    ov = open(OV, "rb").read()
    spans, i, n = [], 0, len(ov)
    while i < n - 3:
        if ov[i] == 0xF8 and ov[i + 1] == 0x6B:
            j = i + 3
            while j < n and ov[j] != 0 and ov[j] < 0xF8:
                j += 2 if ov[j] >= 0xE8 else 1
            spans.append((i, j))
            i = j
        else:
            i += 1
    return spans


def known():
    """Japanese -> Korean for the TEXT-KEYED worklists only.

    ⚠ `intro_lines.tsv` must be excluded. It is keyed by absolute ROM OFFSET and
    patches the cutscene region only, so folding it in here makes overlay-28
    fragments look translated when they are not: 「こ、」 has an intro row and no
    batch row, and reading the intro row made two seams look like a lost comma
    when the real defect is a bare Japanese kana glued to Korean text.
    """
    out = {}
    for fn in sorted(glob.glob(os.path.join(BASE, "translation", "*.tsv"))):
        b = os.path.basename(fn)
        if b.startswith("worksheet") or b == "intro_lines.tsv":
            continue
        for ln in open(fn, encoding="utf-8").read().splitlines()[1:]:
            p = ln.split("\t")
            if len(p) >= 2 and p[0].strip() and p[-1].strip():
                out.setdefault(p[0], p[-1])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()

    tr = known()
    rows = []
    for ln in open(RUNS, encoding="utf-8").read().splitlines():
        p = ln.split("\t")
        if len(p) >= 4:
            rows.append((int(p[0], 16), int(p[1]), p[3]))
    rows.sort()

    occ = collections.Counter(t for _, _, t in rows)
    spans = in_message()
    starts = [s for s, _ in spans]
    import bisect

    def inside(o):
        k = bisect.bisect_right(starts, o) - 1
        return k >= 0 and spans[k][0] <= o < spans[k][1]

    hits = []
    for i in range(len(rows) - 1):
        off, bud, jp = rows[i]
        noff, nbud, njp = rows[i + 1]
        if noff - off > 24:                 # not actually adjacent on screen
            continue
        if not (inside(off) and inside(noff)):
            continue                        # data record, never drawn
        # A short fragment sitting right before translated Korean. Pure
        # punctuation is skipped: 、。・！？「」 are the SAME characters in Korean, so
        # a bare 「、」 run needs no translation and flagging it buried the real
        # hits (14 of the first 37 were exactly that).
        # ⚠ 0x30FB (・) and 0x30FC (ー) sit inside the kana block but are shared
        # punctuation this project deliberately leaves alone, so a naive kana test
        # flags 「・・・？」 as untranslated Japanese. It is not; it renders identically.
        if len(jp) > 4 or not any((0x3040 <= ord(c) <= 0x30FA
                                   or 0x30FD <= ord(c) <= 0x30FF
                                   or 0x4E00 <= ord(c) <= 0x9FFF) for c in jp):
            continue
        nko = tr.get(njp)
        if nko is None:                     # follower untranslated: not a seam issue
            continue
        ko = tr.get(jp)
        if ko is None:
            kind = ("stray Japanese before Korean (budget %d -- %s)"
                    % (bud, "fixable" if bud >= 3 else "cannot hold Korean"))
        elif jp.endswith("、") and "、" not in ko:
            kind = "comma dropped"
        elif a.all:
            kind = "ok"
        else:
            continue
        hits.append((kind, off, bud, jp, ko, noff, nbud, njp, nko,
                     occ[jp], occ[njp]))

    by = collections.Counter(h[0] for h in hits)
    print(f"suspicious seams: {len(hits)}   {dict(by)}\n")
    for kind, off, bud, jp, ko, noff, nbud, njp, nko, o1, o2 in hits:
        print(f"[{kind}]")
        print(f"  0x{off:06X} b{bud} x{o1}  {jp!r} -> {ko!r}")
        print(f"  0x{noff:06X} b{nbud} x{o2}  {njp!r} -> {nko!r}")
        print(f"  on screen: {(ko or jp)}{nko}")
        print()


if __name__ == "__main__":
    main()
