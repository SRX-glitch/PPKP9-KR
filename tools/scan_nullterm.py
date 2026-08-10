#!/usr/bin/env python3
"""Find the game text that is NOT stored as `F8 6B` dialogue.

tools/untranslated.py walks the dialogue opener, which is correct for script and
useless for everything else. File 18 turned out to hold hundreds of baseball
card / ability descriptions as plain NUL-terminated charcode strings on a fixed
stride -- no opener, so the dialogue walk reported the file as clean.

The filter has to be strict or binary noise drowns the result: every byte in
1..247 decodes to some charcode, so "it decoded" means nothing. A run only
counts when it decodes with no unknown charcode, is long enough, and is mostly
kana/kanji -- real sentences pass, packed structs do not.

    python tools/scan_nullterm.py
    python tools/scan_nullterm.py --file 18 --list
"""
import argparse, os, sys

sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P
import untranslated as U

ORIG = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
DIALOGUE_FILES = {4, 8, 20, 25, 27, 1897}      # already covered by the F8 6B pass


def decode_at(buf, i, limit):
    """Decode charcodes from i until the string ends.

    A record ends at NUL *or* at any byte >= 0xF8 -- those are the engine's
    control codes, and real records are terminated by them (`f8 5a 01 f8 01 ff`
    trails the card descriptions in file 18). Treating a control byte as a
    decode failure instead of a terminator is exactly backwards: it throws away
    every genuine string while leaving binary noise, which is what hid file 18's
    text through three passes of this scan.
    """
    s, j = [], i
    while j < limit:
        b = buf[j]
        if b == 0 or b >= 0xF8:
            break
        if 1 <= b <= 231:
            cc, j = b - 1, j + 1
        elif 232 <= b <= 247 and j + 1 < limit:
            cc, j = 256 + (b - 232) * 256 + buf[j + 1], j + 2
        else:
            return None, j
        ch = P.CC2CH.get(cc)
        if ch is None:
            return None, j
        s.append(ch)
    return "".join(s), j


def quality(t, minlen):
    if len(t) < minlen:
        return False
    jp = sum(1 for c in t if U.is_jp(c))
    # mostly Japanese, and not a single repeated character (padding artefact)
    return jp >= 2 and jp / len(t) >= 0.5 and len(set(t)) >= 3


def strings(buf, lo, hi, minlen=4):
    """NUL-terminated decodable strings inside [lo, hi)."""
    i = lo
    while i < hi:
        if buf[i] == 0:
            i += 1
            continue
        t, j = decode_at(buf, i, hi)
        if t is not None and quality(t, minlen):
            yield i, t
            i = j + 1
        else:
            i += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", type=int)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--min", type=int, default=4)
    a = ap.parse_args()

    rom = open(ORIG, "rb").read()
    files = U.fat_files(rom)
    rows = []
    for s, e, i in files:
        if a.file is not None and i != a.file:
            continue
        if rom[s:s + 1] == b"\x10":
            continue                      # LZ77-packed; nothing readable raw
        found = list(strings(rom, s, e, a.min))
        if found:
            rows.append((i, e - s, found))
    rows.sort(key=lambda r: -len(r[2]))

    print(f"{'file':>6} {'size':>10} {'strings':>8}  status      sample")
    for i, size, f in rows[:25]:
        tag = "dialogue" if i in DIALOGUE_FILES else "** NEW **"
        print(f"{i:>6} {size:>10,} {len(f):>8}  {tag:11} "
              f"{' | '.join(t[:26] for _, t in f[:2])}")
        if a.list:
            for off, t in f:
                print(f"           {off:#09x}  {t}")
    new = [r for r in rows if r[0] not in DIALOGUE_FILES]
    print(f"\nNEW files (text the dialogue walk never saw): {len(new)}"
          f"   strings: {sum(len(r[2]) for r in new):,}")


if __name__ == "__main__":
    main()
