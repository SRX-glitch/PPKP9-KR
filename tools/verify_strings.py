#!/usr/bin/env python3
"""Does a given Japanese string still DRAW as Japanese in a built ROM?

The question every screenshot raises, answered without an emulator. Gates prove
"the bytes we wrote are where we put them"; this proves the complementary thing --
that a string the player reported is no longer readable as its original Japanese
at any live site, and that Korean sits there instead.

    python tools/verify_strings.py <built.nds> 商店街 レストラン 「（そして・・・）」

For each string it walks every FAT file, finds the pristine ROM's occurrences of
the encoded Japanese, maps them through the built ROM's own FAT (files move), and
reports what is actually there now.

⚠ Reports SITES, not rows. A worklist row can be "translated" and still leave
nine other sites Japanese -- that is the session-38 bug this tool exists to see.
"""
import os, sys, re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P

ORIG = (r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/"
        r"Power Pro Kun Pocket 9 (Japan).nds")


def encode_jp(s):
    b = bytearray()
    for ch in s:
        cc = P.CH2CC[ch]
        if cc < 231:
            b.append(cc + 1)
        else:
            b += bytes([232 + (cc - 256) // 256, (cc - 256) % 256])
    return bytes(b)


def fat(b):
    off = int.from_bytes(b[0x48:0x4C], "little")
    n = int.from_bytes(b[0x4C:0x50], "little") // 8
    return [(int.from_bytes(b[off + i * 8:off + i * 8 + 4], "little"),
             int.from_bytes(b[off + i * 8 + 4:off + i * 8 + 8], "little"))
            for i in range(n)]


def main():
    new = open(sys.argv[1], "rb").read()
    o = open(ORIG, "rb").read()
    fo, fn = fat(o), fat(new)
    for s in sys.argv[2:]:
        pat = encode_jp(s)
        rows = []
        for fid, (lo, hi) in enumerate(fo):
            if hi <= lo or fid >= len(fn):
                continue
            nlo, nhi = fn[fid]
            if nhi <= nlo:
                continue
            for m in re.finditer(re.escape(pat), o[lo:hi]):
                a = nlo + m.start()
                if a + len(pat) > nhi:
                    continue
                cur = new[a:a + len(pat)]
                if cur == pat:
                    state = "일본어 그대로"
                elif cur[:1] == b"\xf7":
                    state = "리다이렉트 이스케이프"
                else:
                    state = "덮어써짐(한국어)"
                rows.append((fid, m.start() + lo, state))
        bad = sum(1 for _f, _o, st in rows if st == "일본어 그대로")
        print(f"{s!r}: {len(rows)} sites, {bad} still Japanese")
        by = {}
        for fid, off, st in rows:
            by.setdefault((fid, st), []).append(off)
        for (fid, st), offs in sorted(by.items()):
            mark = "  ⛔" if st == "일본어 그대로" else "  ✅"
            print(f"{mark} f{fid:<4d} {st:<12s} {len(offs):4d}  "
                  f"{' '.join(f'0x{x:06X}' for x in offs[:4])}")


main()
