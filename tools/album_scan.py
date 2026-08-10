#!/usr/bin/env python3
"""Extract file 30's `No`-header album records and report their translation state.

Why this exists: the sound album showed entirely Japanese on screen even though
file30's other text was translated. `gap_report.py` could not see it, because that
tool anchors on the `F8 6B` message opener and these are **FF-terminated table
records** -- a structurally different container. The lesson is that "untranslated"
has to be asked once per container type, not once per ROM.

Record shape (from the hex at 0x322B34):

    f7 68  f7 8c  00 00  <num 2B>  00*6  <title>  00*  ff 00
    `--- "No" ---'       `track #'            `-- generous slack --'

The stride between records is NOT constant (16..160 B), so walking a fixed step
stops early -- the first pass found 27 records and there are 358.

    python tools/album_scan.py            # summary
    python tools/album_scan.py --list     # every untranslated record
"""
import os, sys, json, argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P
import koenc

BASE = r"C:/Users/jngji/Desktop/실험실"
ORIG = BASE + r"/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
KR = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font/kr_map.json"
HEADER = bytes([0xF7, 0x68, 0xF7, 0x8C])       # the charcodes that draw "No"
LO, HI = 0x320000, 0x333000
MAXREC = 128


def decode(rom, o, lim):
    s, i = [], o
    while i < lim:
        b = rom[i]
        if b == 0 or b >= 0xF8:
            break
        cc, nxt = P.bytes_to_cc(rom, i)
        ch = P.CC2CH.get(cc)
        if ch is None:
            break
        s.append(ch)
        i = nxt
    return "".join(s), i - o


def records(rom):
    """(header_off, number, title_off, title, budget) for each album record."""
    i = rom.find(HEADER, LO, HI)
    while i >= 0:
        num, _ = decode(rom, i + 6, i + 12)
        # the title is the next decodable run after the number's zero padding
        j = i + 8
        while j < i + 40 and rom[j] == 0:
            j += 1
        title, tl = decode(rom, j, j + 40)
        if title:
            ff = rom.find(b"\xff", j, j + MAXREC)
            yield i, num, j, title, (ff - j if ff >= 0 else -1)
        i = rom.find(HEADER, i + 1, HI)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()

    rom = open(ORIG, "rb").read()
    m = json.load(open(KR, encoding="utf-8"))
    enc, plain = koenc.Encoder(m), koenc.Encoder({**m, "mte": {}})
    patched = open(BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/builds/PPKP9_mte.nds", "rb").read()

    todo, done = [], 0
    for hoff, num, toff, title, bud in records(rom):
        # translated == the patched ROM no longer holds the Japanese there
        want = bytearray()
        for ch in title:
            cc = P.CH2CC[ch]
            want += (bytes([cc + 1]) if cc < 231
                     else bytes([232 + (cc - 256) // 256, (cc - 256) % 256]))
        if patched[toff:toff + len(want)] != bytes(want):
            done += 1
        else:
            todo.append((toff, num, title, bud))

    print(f"album `No` records with a title: {done + len(todo)}")
    print(f"  already translated: {done}")
    print(f"  still Japanese:     {len(todo)}")
    if todo:
        b = [x[3] for x in todo if x[3] > 0]
        print(f"  their budgets: min {min(b)}B  max {max(b)}B  (FF-terminated)")
    if a.list:
        print()
        for toff, num, title, bud in todo:
            print(f"0x{toff:06X}\t{bud}\t{num}\t{title}")


if __name__ == "__main__":
    main()
