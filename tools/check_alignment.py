#!/usr/bin/env python3
"""Flag worklist rows whose ROM text starts inside a control code's operands.

Session 29 traced the blank-choice-box regression to rows extracted one or two
bytes late: the scan began on a control code's operand instead of on the first
real charcode, so the "Japanese" it captured was partly engine parameters
(`ははカーブ` -- the two は are F8's operands, the string is `カーブ`). Patching
such a row writes the redirect escape `F7 2E` + index OVER the control code, and
the engine then draws nothing at all. No crash, just an empty box.

The tell is cheap to check: find the row's bytes in the ORIGINAL rom and look at
what precedes them. A genuine run never begins inside `F8/FB/FD/FE <a> <b>`.

    python tools/check_alignment.py translation/batch120.tsv
    python tools/check_alignment.py --all          # every worklist under survey/

⚠ This is a REVIEW LIST, not a hard gate. Four rounds of tightening took the
batch120 sweep from 3,113 rows to 176 (2.4%), and the remainder still mixes real
scars (`う追い払う。`) with ordinary interjections (`ああ、わかった！`). It cannot go
further, because `F8` is context-dependent in width: the pitch-name records prove
three bytes, while the text after a name insert (`<name>の営業成績が…`) proves two.
So "a lead byte sits just before the string" describes correct cuts as often as
broken ones, and only the front-of-string scar separates them. Read the output;
do not wire it into the build as pass/fail.

Exit status is 1 when anything is flagged, so a caller can gate on it if it ever
becomes precise enough -- today, treat a non-zero exit as "go look".
"""
import argparse, csv, glob, os, sys

sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

ORIG = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"

# Widths confirmed in session 29 by byte-distribution over 0x500000-0x560000:
# operands cluster (low entropy), text does not. FA is deliberately absent --
# its histogram is flat, which means most 0xFA hits are the second byte of a
# 2-byte charcode rather than a real code, so treating it as a lead would fire
# on ordinary text.
WIDTH = {0xF8: 3, 0xFB: 3, 0xFD: 3, 0xFE: 3}


def encode(s):
    b = bytearray()
    for ch in s:
        cc = P.CH2CC.get(ch)
        if cc is None:
            return None
        b += P.cc_to_bytes(cc)
    return bytes(b)


# ・(U+30FB) and ー(U+30FC) live in the kana block but are punctuation. Counting
# them as kana makes `・・・幸せ。` look like a doubled-kana scar -- the same trap
# untranslated.py hit when `으음・・・뭔가` read as untranslated.
KANA = lambda c: 0x3040 <= ord(c) <= 0x30FF and c not in "・ー"
# Kana that legitimately begin a run because a name was inserted just before.
PARTICLES = set("のがはもにをとでへやかねよさぞだなねりるっしてた")


def signature(jp):
    """Does the string LOOK like it swallowed operand bytes?

    The backward peek on its own is not a usable gate. Sweeping batch120 with it
    flagged 2,661 of 7,191 rows, and the flagged ones are mostly legitimate:
    `さん・・・・・・。` / `君・・・・・。` are the text right after a name-insert code, i.e.
    `F8` behaves as TWO bytes there while the pitch-name records prove it is
    THREE elsewhere. Width is context-dependent, so "a lead sits at -1/-2" can
    describe a perfectly cut run.

    What the genuine cases share is a visible scar at the FRONT of the string:
      - a doubled kana that is really two operand bytes (`ははカーブ` -> `カーブ`)
      - a single leading kana in front of otherwise complete text
        (`いＯＫだ。`, `い再挑戦だ！`, `いまあ、やってみるか。`)
    Session 25 logged these as "menu index markers"; same observation, wrong
    explanation. Requiring the scar is what keeps this tool honest -- without it
    the output is 40% noise and unusable as a build gate.
    """
    if len(jp) >= 3 and KANA(jp[0]) and jp[0] == jp[1]:
        return True                       # ははカーブ
    # A leading kana in front of non-kana is the second signature -- but a run
    # that continues after a NAME INSERT starts with a particle by construction
    # (`<name>の営業成績が悪すぎる。`), and those are correctly cut. Excluding the
    # particles is what separates `い再挑戦だ！` from `の営業成績が…`; without it
    # this rule alone flags 521 rows of batch120, essentially all of them seams.
    if len(jp) >= 2 and KANA(jp[0]) and not KANA(jp[1]) and jp[0] not in PARTICLES:
        return True                       # いＯＫだ。 / い再挑戦だ！
    # A third rule -- "kana followed by ・/ー/～" -- would catch `うーーーーん？`,
    # but it also fires on ordinary `えーと・・・？` and on every line that simply
    # opens with an ellipsis, and those are 260 of batch120's rows. A gate that
    # cries wolf gets switched off, so precision wins here: the FB-preceded
    # long-vowel rows are listed in survey/common/translation_notes.tsv for
    # manual review instead of being detected.
    return False


def offenders(rom, hit):
    """Control leads whose operand span covers `hit`.

    A lead at hit-1 or hit-2 means the string starts on operand 1 or 2. Looking
    only at hit-1 misses half the cases -- `ははカーブ` starts two bytes into
    `F8 1a 1a`, and that one is the whole reason this check exists.
    """
    out = []
    for back in (1, 2):
        lead = rom[hit - back]
        if WIDTH.get(lead, 0) > back:
            out.append((back, lead))
    return out


def check(rom, path, limit=None):
    with open(path, encoding="utf-8") as f:
        rows = list(csv.reader(f, delimiter="\t"))
    if not rows:
        return []
    body = rows[1:] if rows[0] and rows[0][0] in ("jp", "n") else rows
    flagged = []
    for r in body:
        jp = next((c for c in r if c and any(ord(x) > 0x2000 for x in c)), None)
        if not jp:
            continue
        pat = encode(jp)
        if not pat or len(pat) < 4:
            continue                      # too short to locate unambiguously
        hits, i = [], rom.find(pat)
        while i >= 0 and len(hits) < 32:
            hits.append(i)
            i = rom.find(pat, i + 1)
        if not hits:
            continue
        bad = [(h, offenders(rom, h)) for h in hits]
        bad = [(h, o) for h, o in bad if o]
        # A backward peek alone over-fires badly: the SECOND byte of a 2-byte
        # charcode can be 0xF8, so ordinary text preceded by such a charcode
        # looks like it sits on an operand. Sweeping batch120 that way flagged
        # 3,113 of 7,191 rows (43%) -- names like 夏菜/城田/霧生, which are fine.
        # A genuinely misaligned row is a single mis-cut run: it occurs once or
        # twice and EVERY occurrence is covered. Requiring that drops the noise.
        if bad and len(bad) == len(hits) and len(hits) <= 2 and signature(jp):
            flagged.append((jp, len(hits), bad))
            if limit and len(flagged) >= limit:
                break
    return flagged


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()

    paths = list(a.paths)
    if a.all:
        paths += sorted(glob.glob("survey/common/*_runs.tsv")) + \
                 sorted(glob.glob("survey/common/*_table.tsv"))
    if not paths:
        sys.exit("아무 파일도 안 줬다. 경로를 주거나 --all 을 써라.")

    rom = open(ORIG, "rb").read()
    total = 0
    for p in paths:
        flagged = check(rom, p)
        total += len(flagged)
        mark = "⚠" if flagged else "✅"
        print(f"{mark} {p}  어긋난 행 {len(flagged)}")
        for jp, n, bad in flagged:
            where = ", ".join(f"{h:#x}(+{b}, {l:#04x})" for h, o in bad for b, l in o)
            print(f"     {jp[:30]!r}  출현{n}  →  {where}")
    print(f"\n합계 어긋난 행: {total}")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
