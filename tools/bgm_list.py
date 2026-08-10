#!/usr/bin/env python3
"""Dump the sound-album BGM name list and say which entries we translated.

Context: the album is known to be uncompletable in the retail game because BGM 68
「バトルンルン」 is an unused Another-Success track left in as dummy data, so it can
never be unlocked. The question for this patch is narrower: does that dummy entry
sit in a record we WRITE to, and does our translation change anything about it.
"""
import os, sys, glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P

BASE = r"C:/Users/jngji/Desktop/실험실"
ROM = BASE + r"/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
TABLE = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/common/file30_table.tsv"

START = int(os.environ.get("BGM_START", "0x322500"), 16)
END = int(os.environ.get("BGM_END", "0x323200"), 16)


def decode(rom, o, limit):
    s, i = [], o
    while i < limit:
        b = rom[i]
        if b == 0 or b >= 0xF8:
            break
        cc, nxt = P.bytes_to_cc(rom, i)
        ch = P.CC2CH.get(cc)
        if ch is None:
            break
        s.append(ch)
        i = nxt
    return "".join(s), i


def worklist():
    """offset -> (jp, ko) for every row of the file-30 table worklist."""
    out = {}
    for ln in open(TABLE, encoding="utf-8").read().splitlines()[1:]:
        p = ln.split("\t")
        if len(p) >= 5 and p[1].strip():
            out[int(p[1], 16)] = (p[4], p[5] if len(p) > 5 else "")
    return out


def main():
    rom = open(ROM, "rb").read()
    wl = worklist()
    i, n = START, 0
    while i < END:
        if rom[i] == 0 or rom[i] >= 0xF8:
            i += 1
            continue
        text, nxt = decode(rom, i, END)
        if len(text) >= 2:
            n += 1
            jp, ko = wl.get(i, (None, None))
            mark = "  <- NOT IN WORKLIST" if jp is None else f"  ko={ko!r}"
            print(f"{n:3d}  0x{i:06X} {nxt - i:3d}B  {text}{mark}")
            i = nxt
        else:
            i += 1


if __name__ == "__main__":
    main()
