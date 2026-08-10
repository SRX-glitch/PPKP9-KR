#!/usr/bin/env python3
"""Decompress every LZ77 file in the ROM and look for game text inside.

The session-31 sweep skipped 1,992 of the 2,030 FAT entries because they start
with an LZ77 header (0x10) -- their raw bytes decode to convincing nonsense, so
they were dismissed as assets. That is an assumption, not a measurement: a
compressed file can hold text just as easily as a bitmap, and the whole point of
the sweep was to stop assuming.

This decompresses each one (NDS LZ77 type 0x10) and runs the same strict text
test the uncompressed sweep used.

    python tools/scan_compressed.py [--list N]
"""
import argparse, collections, io, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P
import expand_overlay as X

ORIG = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
BAD = ("さい", "ぜを", "ペ￥", "プ㎏", "ゼ㎏", "ァ％", "ふい", "ほい", "へい",
       "ミま", "ァＲ", "ペ）", "そい", "ズか", "Ｒ意", "ペて", "ヴＭ")


def lz77(data):
    """NDS LZ77 (type 0x10). Returns None if the stream is malformed."""
    if not data or data[0] != 0x10:
        return None
    size = int.from_bytes(data[1:4], "little")
    if size == 0 or size > 8 << 20:
        return None
    out = bytearray()
    i = 4
    try:
        while len(out) < size:
            flags = data[i]
            i += 1
            for bit in range(8):
                if len(out) >= size:
                    break
                if flags & (0x80 >> bit):
                    b0, b1 = data[i], data[i + 1]
                    i += 2
                    n = (b0 >> 4) + 3
                    disp = (((b0 & 0xF) << 8) | b1) + 1
                    if disp > len(out):
                        return None
                    for _ in range(n):
                        out.append(out[-disp])
                else:
                    out.append(data[i])
                    i += 1
    except IndexError:
        return None
    return bytes(out)


def runs(buf):
    """Charcode runs: 1-byte codes < 0xE8, 2-byte leads 0xE8-0xF7, any other
    byte ends the run. Same decode the opcode walker uses, without the opcodes."""
    out, cur, i = [], [], 0
    while i < len(buf):
        b = buf[i]
        if b >= 0xF8 or b == 0:
            if len(cur) >= 4:
                out.append("".join(cur))
            cur = []
            i += 1
            continue
        if b >= 0xE8:
            if i + 1 >= len(buf):
                break
            cc = 256 + (b - 232) * 256 + buf[i + 1]
            i += 2
        else:
            cc = b - 1
            i += 1
        ch = P.CC2CH.get(cc)
        if ch is None:
            if len(cur) >= 4:
                out.append("".join(cur))
            cur = []
            continue
        cur.append(ch)
    if len(cur) >= 4:
        out.append("".join(cur))
    return out


def real(s):
    if any(p in s for p in BAD):
        return False
    c = collections.Counter(s[i:i + 2] for i in range(len(s) - 1))
    if c and max(c.values()) >= 2 and len(s) >= 6:
        return False
    kanji = re.search(r"[\u4E00-\u9FFF]", s)
    kana = re.search(r"[\u3040-\u30FF]", s)
    if kanji and kana and len(s) >= 4:
        return True
    if kana and len(s) >= 10 and any(p in s for p in "。、！？「」"):
        return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", type=int, default=6)
    a = ap.parse_args()
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

    rom = open(ORIG, "rb").read()
    fat = X.u32(rom, 0x48)
    n = X.u32(rom, 0x4C) // 8
    tried = ok = withtext = 0
    hits = []
    for fid in range(n):
        lo = X.u32(rom, fat + fid * 8)
        hi = X.u32(rom, fat + fid * 8 + 4)
        if hi <= lo or hi > len(rom) or rom[lo] != 0x10:
            continue
        tried += 1
        buf = lz77(rom[lo:hi])
        if buf is None:
            continue
        ok += 1
        t = [s for s in runs(buf) if real(s)]
        if len(t) >= 5:
            withtext += 1
            hits.append((len(t), fid, hi - lo, len(buf), t))
    hits.sort(reverse=True)
    print(f"LZ77 files: {tried} tried, {ok} decompressed, {withtext} with >=5 "
          f"text-looking runs")
    for cnt, fid, csz, dsz, t in hits[:20]:
        print(f"  file {fid:<5} {csz:>7} -> {dsz:>8} B   text runs {cnt}")
        for s in t[:a.list]:
            print(f"        {s[:56]!r}")


if __name__ == "__main__":
    main()
