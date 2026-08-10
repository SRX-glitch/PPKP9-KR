#!/usr/bin/env python3
"""Is there Japanese text we have not found yet?

tools/untranslated.py walks the game's own dialogue opener (`F8 6B`). That is
the right scanner for script, but it has two blind spots:

  * COMPRESSED files. NDS files are routinely LZ77/LZ11 packed. Text inside one
    does not decode raw at all, so a byte scan reports nothing and the file
    looks clean when it is not.
  * Text with no `F8 6B` opener -- fixed-width UI labels, item names, anything
    the renderer is handed directly rather than through the dialogue walker.

This scans for both: it flags files whose first byte looks like an LZ header,
and it finds runs of consecutive valid charcodes regardless of how they start.

    python tools/deep_scan.py
    python tools/deep_scan.py --file 27 --list
"""
import argparse, collections, os, sys

sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P
import untranslated as U

ORIG = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
COVERED = {4, 8, 20, 25, 27, 1897}      # translated, or a duplicate of one


def lz_kind(buf):
    """NDS compression header, if this looks like one."""
    if len(buf) < 8:
        return None
    t = buf[0]
    size = int.from_bytes(buf[1:4], "little")
    if t == 0x10 and 0 < size < 0x400000:
        return "LZ77"
    if t == 0x11 and 0 < size < 0x400000:
        return "LZ11"
    if t == 0x24 or t == 0x28:
        return "Huff"
    if t == 0x30 and 0 < size < 0x400000:
        return "RLE"
    return None


def free_runs(buf, lo, hi, minlen=4):
    """Runs of >=minlen consecutive decodable charcodes, no opener required.

    This is deliberately looser than the `F8 6B` walk: menu labels are handed to
    the renderer directly, so requiring the dialogue opener would miss them.
    """
    i, n = lo, hi
    while i < n:
        j, s = i, []
        while j < n:
            b = buf[j]
            if 1 <= b <= 231:
                cc, nxt = b - 1, j + 1
            elif 232 <= b <= 247 and j + 1 < n:
                cc, nxt = 256 + (b - 232) * 256 + buf[j + 1], j + 2
            else:
                break
            ch = P.CC2CH.get(cc)
            if ch is None:
                break
            s.append(ch)
            j = nxt
        text = "".join(s)
        if len(text) >= minlen and sum(1 for c in text if U.is_jp(c)) >= 2:
            yield i, text
        i = j + 1 if j > i else i + 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", type=int)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--min-runs", type=int, default=3)
    a = ap.parse_args()

    rom = open(ORIG, "rb").read()
    files = U.fat_files(rom)
    print(f"FAT files: {len(files)}")

    comp = collections.Counter()
    for s, e, i in files:
        k = lz_kind(rom[s:e])
        if k:
            comp[k] += 1
    print(f"compressed-looking files: {dict(comp) or 'none'}")

    hits = []
    for s, e, i in files:
        if a.file is not None and i != a.file:
            continue
        if lz_kind(rom[s:e]):
            continue                     # cannot read text without unpacking
        runs = list(free_runs(rom, s, e))
        if len(runs) >= a.min_runs:
            hits.append((i, e - s, runs))
    hits.sort(key=lambda h: -len(h[2]))

    print(f"\n{'file':>6} {'size':>10} {'runs':>6}  status   sample")
    for i, size, runs in hits[:40]:
        tag = "COVERED" if i in COVERED else "** NEW **"
        sample = " | ".join(t[:22] for _, t in runs[:3])
        print(f"{i:>6} {size:>10,} {len(runs):>6}  {tag:9} {sample}")
        if a.list:
            for off, t in runs:
                print(f"          {off:#09x}  {t}")
    new = [h for h in hits if h[0] not in COVERED]
    print(f"\nfiles with text NOT already covered: {len(new)}")


if __name__ == "__main__":
    main()
