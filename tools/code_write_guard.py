#!/usr/bin/env python3
"""Show what an OPTIONAL pass adds, and whether it landed on ARM code.

Session 44. `PPKP9_BATCH_SITES=1` stalled the game right after the prologue, and
the reason was not "wrote into an array" (session 43's story for file 30) but
something worse: the batch corpus matched byte pairs that are **ARM instructions**
and replaced them with Hangul charcodes. Measured in file 18 / file 20 (overlays
8 and 9, which share RAM base 0x020CA020 and hold code as well as data):

    file18 rel 0x00D4C7   1a000026 BNE +0x26   ->  ea000026 B +0x26   (condition gone)
                          e3c00002 BIC R0,#2   ->  e3c00079 BIC R0,#0x79
    file20 rel 0x005EAB   0a00000c BEQ         ->  e800000c STMDA

Every existing gate was green. `verify_writes` proves a changed byte sits inside a
run **the extractor recorded**, so when the extractor records a code span as text
the proof is circular.

⛔ WHY THIS TOOL COMPARES TWO BUILDS INSTEAD OF JUDGING ONE.
The first version of this script judged a single ROM: "was the ORIGINAL word a
plausible ARM instruction?" It reported 755 hits on `v204_stdenv`, a build that
plays fine -- because a normal text write flips a 1-byte Japanese charcode to a
2-byte Hangul one (`03 00 00 1a` -> `03 00 00 eb`) and, read as a word, that is
indistinguishable from `BNE` becoming `BL`. Word-aligned decoding cannot separate
text from code on its own. What DID separate them was differential: build the
same corpus with and without the suspect flag and look only at what the flag
added. That is what this does.

    # what does BATCH_SITES add on top of a build known to play?
    python tools/code_write_guard.py builds/PPKP9_kr_v204_stdenv.nds \
                                     builds/PPKP9_kr_v205_batchonly.nds

Exit 1 if the candidate writes anything the baseline did not, so it can gate a
build once a trusted baseline exists.
"""
import argparse, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PRISTINE = os.path.join(os.path.dirname(ROOT),
                        "Power Pro Kun Pocket 9 (Japan).nds")

DEFAULT_FILES = (4, 8, 13, 18, 20, 25, 27, 30)


def fat(rom):
    off, ln = struct.unpack("<II", rom[0x48:0x50])
    return [struct.unpack("<II", rom[off + i * 8:off + i * 8 + 8])
            for i in range(ln // 8)]


# Script control bytes. A word containing one of these is text/opcode, not code:
# `F8 xx` opens and closes every run, `F7` leads our escapes, `FD/FE/FF` frame the
# records. Without this, file 8's `38 F8 08 72` (a perfectly normal run header)
# decodes as "data-processing" and the guard cries wolf on a build that plays.
SCRIPT_BYTES = frozenset((0xF7, 0xF8, 0xFD, 0xFE, 0xFF))


def arm_note(word):
    """A short human note for a word, or '' when it does not look like code.

    Only used to LABEL a difference the differential already found, never to
    decide on its own -- see the header for why that direction fails.
    """
    if any(b in SCRIPT_BYTES for b in word.to_bytes(4, "little")):
        return ""
    cond = word >> 28
    if cond == 0xF:
        return ""
    op = (word >> 25) & 0x7
    if op == 0x5:
        return "B/BL" + (" (unconditional)" if cond == 0xE else " (conditional)")
    if op in (0x0, 0x1):
        return "data-processing"
    if op in (0x2, 0x3):
        return "LDR/STR"
    if op == 0x4:
        return "LDM/STM"
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("baseline", help="a build that is known to play")
    ap.add_argument("candidate", help="the same corpus plus the suspect pass")
    ap.add_argument("--pristine", default=PRISTINE)
    ap.add_argument("--files", default=None)
    ap.add_argument("--max-report", type=int, default=16)
    a = ap.parse_args()

    fids = (tuple(int(x) for x in a.files.split(",") if x.strip())
            if a.files else DEFAULT_FILES)

    orig = open(a.pristine, "rb").read()
    base = open(a.baseline, "rb").read()
    cand = open(a.candidate, "rb").read()
    fo, fbase, fcand = fat(orig), fat(base), fat(cand)

    total, coded = 0, 0
    for fid in fids:
        so, eo = fo[fid]
        sb, eb = fbase[fid]
        sc, ec = fcand[fid]
        if (eb - sb) != (ec - sc):
            print(f"file{fid}: SKIPPED -- the two builds give it different "
                  f"lengths ({eb - sb} vs {ec - sc}); a relocated file cannot be "
                  f"compared word by word")
            continue
        length = min(eo - so, eb - sb)
        rows = []
        for w in range(0, length - 3, 4):
            if base[sb + w:sb + w + 4] == cand[sc + w:sc + w + 4]:
                continue
            ow = struct.unpack("<I", orig[so + w:so + w + 4])[0]
            bw = struct.unpack("<I", base[sb + w:sb + w + 4])[0]
            cw = struct.unpack("<I", cand[sc + w:sc + w + 4])[0]
            rows.append((w, ow, bw, cw, arm_note(ow) if ow == bw else ""))
        if not rows:
            continue
        total += len(rows)
        note_rows = [r for r in rows if r[4]]
        coded += len(note_rows)
        print(f"file{fid}: candidate changes {len(rows)} word(s) the baseline "
              f"left alone; {len(note_rows)} of them were UNTOUCHED ORIGINAL "
              f"words that decode as ARM")
        for w, ow, bw, cw, note in rows[:a.max_report]:
            tag = f"  <-- pristine {note}" if note else ""
            print(f"    rel 0x{w:06X}  orig {ow:08x}  base {bw:08x}  "
                  f"cand {cw:08x}{tag}")
        if len(rows) > a.max_report:
            print(f"    ... {len(rows) - a.max_report} more")

    name = os.path.basename(a.candidate)
    if coded:
        print(f"{name}: FAIL -- {coded} of {total} extra write(s) replaced a "
              f"pristine word that decodes as ARM. The game will take a wrong "
              f"branch. Exclude those files (see PPKP9_BATCH_EXCLUDE).")
        return 1
    if total:
        print(f"{name}: WARN -- {total} extra write(s), none on a pristine ARM "
              f"word. Plausible but unproven; play the changed screens.")
        return 0
    print(f"{name}: ok -- writes nothing the baseline did not")
    return 0


if __name__ == "__main__":
    sys.exit(main())
