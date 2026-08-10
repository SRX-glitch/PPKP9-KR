#!/usr/bin/env python3
"""List every dialogue run in the opening-cutscene script (outside overlay 28).

Why this exists
---------------
`intro_lines.tsv` only ever held 6 lines. A boot test showed a box whose first
line was still Japanese while its second was Korean -- the run at 0x3301E8 was
simply never on the worklist. The whole prologue (the Nice Guy street fight AND
the space-federation narration) is in this region and untranslated.

Walking it needs the real opcode table, not "skip one byte past 0xF8". `F8 01`
is 2 bytes and `F8 29 <speaker>` is 3; skipping one byte leaves the operand in
the text stream, which is what turned 「こ、このガキャあ…！」 into the two bogus runs
「あこ、」 and 「るおこのガキャあ…！」. Same class of bug as the F8 15 choice-count
regression -- an opcode declared shorter than it is.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P

BASE = r"C:/Users/jngji/Desktop/실험실"
ROM = BASE + r"/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
L = json.load(open(BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/ov28/opcode_lengths.json"))
BARE = {int(k): v for k, v in L["bare"].items()}
F8 = {int(k): v for k, v in L["f8"].items() if v}

START = int(os.environ.get("SCAN_START", "0x3301C0"), 16)
END = int(os.environ.get("SCAN_END", "0x330C00"), 16)


def runs_in(rom, start, end):
    """Yield (offset, byte_len, text) for each contiguous charcode run."""
    out = []
    i, cur, st = start, [], None
    def flush():
        nonlocal cur, st
        if cur and st is not None:
            out.append((st, i - st, "".join(cur)))
        cur, st = [], None

    while i < end:
        b = rom[i]
        if b >= 0xF8:
            flush()
            if b == 0xF8:
                i += F8.get(rom[i + 1], 2)
            else:
                i += BARE.get(b, 1)
            continue
        if b == 0:
            flush()
            i += 1
            continue
        cc, nxt = P.bytes_to_cc(rom, i)
        ch = P.CC2CH.get(cc)
        if ch is None:
            flush()
            i += 1
            continue
        if st is None:
            st = i
        cur.append(ch)
        i = nxt
    flush()
    return out


def main():
    rom = open(ROM, "rb").read()
    for off, nb, s in runs_in(rom, START, END):
        if len(s) < 2:
            continue
        print("0x%06X\t%d\t%s\t%s" % (off, nb, s, rom[off:off + nb].hex(" ")))


if __name__ == "__main__":
    main()
