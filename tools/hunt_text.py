#!/usr/bin/env python3
"""Hunt for game text ANYWHERE in the ROM, on a calibrated Japanese-likeness score.

Earlier sweeps kept producing garbage because the "is this text?" test was a
hand-written blacklist of digraphs. Charcode-decoded graphics data will always
find new ways to look like kana, so the test has to be positive, not negative:
score a string by how much of it is common Japanese function kana plus whether it
contains real grammatical fragments.

Calibrated on known-good and known-junk strings from this ROM:

    real  0.40 - 1.65      junk  0.00 - 0.27      threshold 0.35

Covers the three places earlier passes skipped:
  * LZ77-compressed FAT files (1,992 of 2,030 -- the biggest blind spot)
  * the ARM9 / ARM7 static binaries, which are not FAT entries at all
  * raw charcode runs, i.e. text that is not introduced by any opcode

    python tools/hunt_text.py
"""
import collections, io, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import expand_overlay as X
import scan_compressed as S

import re

COMMON = set("のにはをがでとかもらてたしますないるれこそあうきっよじだ")
WORDS = ("する", "します", "です", "ます", "だった", "という", "ている", "ことが",
         "ものが", "ません", "ください", "だろう", "しない", "なって", "ました",
         "できる", "けど", "だけ", "ながら", "から", "ので", "たい", "よう")
# charcode-decoded graphics love these; real dialogue almost never has them
# mid-sentence, and they were what kept scoring 0.4-0.5 as false positives.
SYM = set("￥％㎏♀♂★◎↑←→÷×』『〓")
FW = re.compile(r"[Ａ-Ｚａ-ｚ]")
THRESHOLD = 0.45          # calibrated: real 0.41-1.65, junk 0.00-0.40


def jscore(s):
    """Positive test, not a blacklist. Graphics data always finds a new way to
    look like kana, so score how much of the string is common Japanese function
    kana plus real grammatical fragments, and reject repetition and symbol soup."""
    if len(s) < 8:
        return 0.0
    if len(set(s)) / len(s) < 0.55:          # repetition is not language
        return 0.0
    if any(c in SYM for c in s):
        return 0.0
    if len(FW.findall(s)) / len(s) > 0.12:
        return 0.0
    if not re.search(r"[一-鿿]", s) and not any(w in s for w in WORDS):
        return 0.0
    return (sum(1 for c in s if c in COMMON) / len(s)
            + 0.5 * sum(1 for w in WORDS if w in s))


def scan(buf):
    return [s for s in S.runs(buf) if jscore(s) >= THRESHOLD]


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    rom = open(S.ORIG, "rb").read()
    fat = X.u32(rom, 0x48)
    n = X.u32(rom, 0x4C) // 8

    print("=== ARM9 / ARM7 static binaries (never in the FAT) ===")
    for name, off_o, len_o in (("arm9", 0x20, 0x2C), ("arm7", 0x30, 0x3C)):
        off, ln = X.u32(rom, off_o), X.u32(rom, len_o)
        hits = scan(rom[off:off + ln])
        print(f"  {name}: {ln} B -> {len(hits)} scoring runs")
        for s in hits[:8]:
            print(f"      {jscore(s):.2f} {s[:60]!r}")

    print("\n=== FAT files ===")
    plain, comp = [], []
    for fid in range(n):
        lo, hi = X.u32(rom, fat + fid * 8), X.u32(rom, fat + fid * 8 + 4)
        if hi <= lo or hi > len(rom):
            continue
        raw = rom[lo:hi]
        if raw[:1] == b"\x10":
            buf = S.lz77(raw)
            if buf is None:
                continue
            hits = scan(buf)
            if hits:
                comp.append((len(hits), fid, hits))
        else:
            hits = scan(raw)
            if hits:
                plain.append((len(hits), fid, hits))
    plain.sort(reverse=True)
    comp.sort(reverse=True)
    print(f"  uncompressed with text: {len(plain)}   compressed with text: {len(comp)}")
    for tag, lst in (("UNCOMPRESSED", plain), ("COMPRESSED", comp)):
        print(f"  -- {tag} top 12 --")
        for cnt, fid, hits in lst[:12]:
            print(f"     file {fid:<5} runs {cnt}")
            for s in hits[:3]:
                print(f"         {jscore(s):.2f} {s[:60]!r}")


if __name__ == "__main__":
    main()
