#!/usr/bin/env python3
"""Follow file 30's LIVE pointer arrays in a built ROM and decode what they hit.

This is the check that was missing when the encyclopedia shipped in Japanese
twice. Both failures were the same shape: bytes written at a recorded offset
that the game no longer loads, while every build gate stayed green. A gate that
starts from the FAT, walks to the array, follows the pointer and reads the
record is the only one that can catch it -- it asks the question the console
asks.

    python tools/verify_profiles.py <rom.nds>
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P
import expand_overlay as X
import insert_profiles as IPF

NEWLINE, END = 0xFA, 0xFF


def encode_ko_bytes(ko, enc):
    return IPF.encode_ko(ko, enc)


def read_record(rom, off, limit=512):
    out, i = [], off
    while i < off + limit:
        b = rom[i]
        if b == END:
            break
        if b == NEWLINE:
            out.append("\n"); i += 1; continue
        if b == 0:
            out.append(" "); i += 1; continue
        if b >= 0xF8:
            return None
        cc, nxt = P.bytes_to_cc(rom, i)
        ch = P.CC2CH.get(cc)
        if ch is None:
            return None
        out.append(ch); i = nxt
    return "".join(out)


def main():
    path = sys.argv[1]
    rom = open(path, "rb").read()
    fat = X.u32(rom, 0x48)
    lo = X.u32(rom, fat + IPF.FID * 8)
    _, _, ram, size = X.overlay_of_file(rom, IPF.FID)
    shift = lo - IPF.ORIG_LO

    # ⚠ Do NOT decode the target and look for Hangul. Our glyphs live in slots
    # whose poketbl entry is still the ORIGINAL kanji, so a correct Korean record
    # decodes to 「云劾鉛虻 欽苅宜…」 -- reading it as failure is how this check
    # first reported a good build as broken. Compare the BYTES we meant to write.
    # The records are written with build_kr's PLAIN encoder (`enc_plain`). A
    # default Encoder applies the MTE dictionary and produces different bytes, so
    # comparing against it reports a perfectly good build as unreachable.
    import koenc
    enc = koenc.Encoder()
    enc.mte, enc._mte_sorted = {}, []
    want = {}          # old RAM address -> (expected Korean bytes, first line)
    for off, _jp, ko in IPF.rows():
        want[ram + (off - IPF.ORIG_LO)] = (encode_ko_bytes(ko, enc),
                                           ko.split("\n")[0][:34])

    live = []                                   # every pointer target, once
    stale = []
    for base, cnt in IPF.ARRAYS:
        for k in range(cnt):
            v = X.u32(rom, base + shift + k * 4)
            if v in want:                       # pointer was never moved
                stale.append((v, want[v][1]))
            elif ram <= v < ram + size:
                live.append(lo + (v - ram))

    ok, wrong = 0, []
    for kb, first in want.values():
        if any(bytes(rom[f:f + len(kb)]) == kb for f in live):
            ok += 1
        else:
            wrong.append(first)

    print(f"{os.path.basename(path)}: {ok}/{len(want)} translated records are "
          f"reachable through a live pointer")
    if stale or wrong:
        for v, t in stale[:5]:
            print(f"  !! pointer still on the ORIGINAL record: 0x{v:08X}  {t}")
        for t in wrong[:5]:
            print(f"  !! Korean bytes not reachable: {t}")
        sys.exit(1)


if __name__ == "__main__":
    main()
