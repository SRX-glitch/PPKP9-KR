#!/usr/bin/env python3
"""Find charcode-encoded Japanese text inside a RAM image (see dst_ram.py).

Answers "which buffer is this screen actually reading from" -- the question the
ROM offset alone cannot answer, because runtime-assembled strings (name+particle,
label+number+verb) exist only in RAM.

Usage:
    python3 ramfind.py <ram.bin> "このファイルではじめる" ["はい" ...]
    python3 ramfind.py <ram.bin> --hex 0a196c80
    python3 ramfind.py <ram.bin> --at 0x0223B4C0 [--len 64]     decode at address
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P

BASE = 0x02000000
CTX = 24


def enc(text):
    return b"".join(P.cc_to_bytes(P.CH2CC[c]) for c in text)


def dec(data, limit=40):
    """Decode charcode bytes back to text, stopping at an unmapped code."""
    out, i = [], 0
    while i < len(data) and len(out) < limit:
        cc, i2 = P.bytes_to_cc(data, i)
        if cc is None or i2 == i:
            break
        ch = P.CC2CH.get(cc)
        out.append(ch if ch else f"<{cc:04x}>")
        i = i2
    return "".join(out)


def main():
    ram = open(sys.argv[1], "rb").read()
    args = sys.argv[2:]
    if "--at" in args:
        a = int(args[args.index("--at") + 1], 0)
        n = int(args[args.index("--len") + 1], 0) if "--len" in args else 64
        o = a - BASE
        print(f"0x{a:08x}: {ram[o:o+n].hex()}")
        print(f"  decode: {dec(ram[o:o+n])!r}")
        return
    if "--hex" in args:
        needles = [(args[args.index("--hex") + 1], bytes.fromhex(args[args.index("--hex") + 1]))]
    else:
        needles = [(t, enc(t)) for t in args]
    for label, pat in needles:
        print(f"=== {label!r}  {pat.hex()}")
        off, n = 0, 0
        while True:
            off = ram.find(pat, off)
            if off < 0:
                break
            n += 1
            if n <= 24:
                lo = max(0, off - CTX)
                print(f"  0x{BASE+off:08x}  before={ram[lo:off].hex()}  after={ram[off+len(pat):off+len(pat)+CTX].hex()}")
                print(f"              ctx={dec(ram[lo:off+len(pat)+CTX], 60)!r}")
            off += 1
        print(f"  total {n} hit(s)")


if __name__ == "__main__":
    main()
