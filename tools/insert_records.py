#!/usr/bin/env python3
"""Rewrite whole FF-terminated records so the line budget becomes a RECORD budget.

`insert_extra` writes each text run back into its own byte span, which is why the
ending epilogues came out 232-of-264 over budget: a Japanese line packs meaning
into kanji worth 2 bytes each, and the Korean for that one line simply does not
fit that one line's bytes.

But the line boundary is not a real constraint. An epilogue is ONE record --
`run FA run FA run … FF` -- and the game re-flows it as it draws. Measured on
file 30's endings: per line, 32 of 264 fit; **per record, 63 of 65 fit**, with
159 bytes of slack on average. So rebuild the record instead:

  * every byte that is not a recorded text run is copied through untouched
    (FA newlines, F8 xx colour/size opcodes, the terminator)
  * each run is replaced by its Korean, which may be any length
  * the leftover is padded with 0x00 before the terminator, so the record keeps
    its exact original size and nothing after it moves

A record is refused unless every one of its runs re-encodes to the recorded
Japanese, and unless the rebuild still fits the original span.

    python tools/insert_records.py --report 30
"""
import argparse, collections, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P
import koenc

BASE = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"
COMMON = BASE + r"/survey/common"
END = 0xFF
MAXREC = 600
SHIP = ()   # file 30 은 insert_extra 인플레이스로 처리(레코드 재조립은 포인터를 민다)


def encode_jp(s):
    b = bytearray()
    for ch in s:
        if ch == " ":
            b.append(0)
            continue
        cc = P.CH2CC[ch]
        b += (bytes([cc + 1]) if cc < 231
              else bytes([232 + (cc - 256) // 256, (cc - 256) % 256]))
    return bytes(b)


def rows(fid):
    p = os.path.join(COMMON, f"file{fid}_extra.tsv")
    if not os.path.exists(p):
        return
    for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
        f = ln.split("\t")
        if len(f) >= 6 and f[5].strip():
            yield int(f[0], 16), int(f[1]), f[4], f[5].strip()


def span(rom, off, lo):
    """(start, terminator) of the FF-terminated record holding `off`."""
    i = off
    while i > lo and off - i < MAXREC:
        if rom[i - 1] == END:
            break
        i -= 1
    j = off
    while j < len(rom) and j - off < MAXREC:
        if rom[j] == END:
            return i, j
        j += 1
    return i, -1


def apply(rom, fid, enc=None, verbose=True):
    import expand_overlay as X
    enc = enc or koenc.Encoder()
    lo = X.u32(rom, X.u32(rom, 0x48) + fid * 8)

    groups = collections.defaultdict(list)
    for off, blen, jp, ko in rows(fid):
        s, t = span(rom, off, lo)
        if t < 0:
            continue
        groups[(s, t)].append((off, blen, jp, ko))

    written = skipped = 0
    for (s, t), items in sorted(groups.items()):
        items.sort()
        if any(bytes(rom[o:o + b]) != encode_jp(jp) for o, b, jp, _k in items):
            skipped += 1
            continue                      # a run drifted; never rebuild blind
        out, cur, bad = bytearray(), s, False
        for o, b, _jp, ko in items:
            out += bytes(rom[cur:o])      # opcodes / separators, untouched
            try:
                out += enc.encode(ko)
            except KeyError:
                bad = True
                break
            cur = o + b
        if bad:
            skipped += 1
            continue
        out += bytes(rom[cur:t])
        if len(out) > t - s:
            skipped += 1
            continue
        rom[s:t] = bytes(out) + b"\x00" * (t - s - len(out))
        written += 1

    if verbose:
        print(f"  records file {fid}: {written} rebuilt, {skipped} refused")
    return {"written": written, "skipped": skipped}


def apply_all(rom, enc=None, verbose=True, files=SHIP):
    tot = {"written": 0, "skipped": 0}
    for fid in files:
        r = apply(rom, fid, enc, verbose)
        for k in tot:
            tot[k] += r[k]
    return tot


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fid", type=int, nargs="?", default=30)
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    rom = bytearray(open(r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/"
                         r"Power Pro Kun Pocket 9 (Japan).nds", "rb").read())
    print(apply(rom, a.fid))


if __name__ == "__main__":
    main()
