#!/usr/bin/env python3
"""Generate the next translation worksheet: untranslated Nice Guy lines by frequency.

Skips what is not worth a translator's time or would corrupt the build:
  - lines already translated in ANY batch (the build loader is last-wins, so a
    duplicate silently overrides the earlier translation)
  - pure punctuation / ellipsis runs, which are identical in Korean
  - parser fragments: a line the dialogue scanner cut mid-sentence has no
    standalone meaning, and they read as garbage in isolation
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from layout_audit import rows as display_rows

BASE = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"
# Auto-discover so a new batchN is never silently missed (an off-by-one in this
# range once let already-translated lines re-enter the worksheet).
import glob as _glob
BATCHES = ["common_lines"] + sorted(
    (os.path.splitext(os.path.basename(p))[0]
     for p in _glob.glob(f"{BASE}/translation/batch*.tsv")),
    key=lambda n: int(n[5:]))
PUNCT = "・。、！？～）（「」・…゛゜ー"
def KANA(c):
    """A character that carries meaning, so worth counting toward 'translatable'.

    '・' lives inside the katakana block, so the naive range test rates a line of
    pure ellipsis as 100% kana and floods the worksheet with 「・・・・・・。」.
    """
    return c not in PUNCT and (0x3040 <= ord(c) <= 0x30FF or 0x4E00 <= ord(c) <= 0x9FFF)


def done_set():
    done = set()
    for name in BATCHES:
        p = f"{BASE}/translation/{name}.tsv"
        if not os.path.exists(p):
            continue
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            if "\t" in ln:
                jp = ln.split("\t")[0].strip()
                if jp:
                    done.add(jp)
    return done


def main(out_name, want=140):
    done = done_set()
    lines = []
    for ln in open(f"{BASE}/survey/ov28/dialogue_runs.tsv", encoding="utf-8").read().splitlines():
        p = ln.split("\t")
        if len(p) >= 4:
            lines.append((int(p[0], 16), int(p[1]), p[3]))
    occ = collections.Counter(jp for _, _, jp in lines)
    budget = {}
    for off, blen, jp in lines:
        budget[jp] = min(budget.get(jp, 1 << 30), blen)

    rows = []
    for jp, n in occ.items():
        if jp in done:
            continue
        real = [c for c in jp if KANA(c)]
        if len(real) < 3:                      # symbols, ellipses, single kana
            continue
        if jp[-1] in "見投打昨喫":              # typical parser-cut endings
            continue
        if any(c in jp for c in "尅㎞"):        # gaiji / mis-decoded artifacts
            continue
        rows.append((n, budget[jp], jp))
    rows.sort(key=lambda r: (-r[0], -len(r[2])))
    out = f"{BASE}/translation/{out_name}"
    with open(out, "w", encoding="utf-8") as f:
        # `max` = how many Korean glyphs stay inside the original's display
        # lines: a box line holds 19 full-width glyphs, a page holds 3, so
        # going over costs an extra line (never lost text, just a page break).
        f.write("count\tbudget\tmax\tjp\tko\n")
        for n, b, jp in rows[:want]:
            f.write(f"{n}\t{b}\t{19 * display_rows(jp)}\t{jp}\t\n")
    print(f"{out}: {min(want,len(rows))} candidates "
          f"(untranslated pool {len(rows)}, already done {len(done)})")
    tot = sum(occ[jp] for _, _, jp in rows[:want])
    print(f"they cover {tot} occurrences")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "worksheet_batch14.tsv",
         int(sys.argv[2]) if len(sys.argv) > 2 else 140)
