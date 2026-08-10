#!/usr/bin/env python3
"""Try several encodings for a string against a memory/ROM image.

Q6 ("which consumer draws the ability-panel labels") stalled because the census
only knows the game's own charcode table.  A label that is real text but stored
in some other encoding is invisible to that search, so before concluding
"graphics" this asks the cheap question first: is it just a different encoding?

Usage:
    python3 encscan.py <image.bin> "マニュアル" [more...] [--base 0x02000000]
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P

CODECS = ["shift_jis", "euc_jp", "utf-16-le", "utf-16-be", "utf-8", "cp932", "iso2022_jp"]


def variants(text):
    out = []
    for c in CODECS:
        try:
            out.append((c, text.encode(c)))
        except Exception:
            pass
    try:
        out.append(("charcode", b"".join(P.cc_to_bytes(P.CH2CC[ch]) for ch in text)))
    except Exception:
        pass
    # charcode as raw 16-bit LE / BE indices (no cc_to_bytes packing)
    try:
        cc = [P.CH2CC[ch] for ch in text]
        out.append(("cc_u16le", b"".join(v.to_bytes(2, "little") for v in cc)))
        out.append(("cc_u16be", b"".join(v.to_bytes(2, "big") for v in cc)))
        out.append(("cc_u8", bytes(v & 0xFF for v in cc)))
    except Exception:
        pass
    return out


def main():
    img = open(sys.argv[1], "rb").read()
    args = [a for a in sys.argv[2:] if not a.startswith("--")]
    base = 0x02000000
    if "--base" in sys.argv:
        base = int(sys.argv[sys.argv.index("--base") + 1], 0)
    for text in args:
        print(f"=== {text!r}")
        for name, pat in variants(text):
            if not pat:
                continue
            hits, off = [], 0
            while len(hits) < 8:
                off = img.find(pat, off)
                if off < 0:
                    break
                hits.append(off)
                off += 1
            if hits:
                print(f"  {name:10} {pat.hex()[:32]:34} -> " +
                      " ".join(f"0x{base+h:08x}" for h in hits))
        print()


if __name__ == "__main__":
    main()
