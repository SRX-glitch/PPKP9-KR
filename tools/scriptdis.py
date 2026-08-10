#!/usr/bin/env python3
"""Readable listing of the PPKP9 script VM stream.

Walks a byte range the way the engine does (0x020C0858 dispatch): >=0xFA is a
bare opcode, F8/F9 take a subcode byte and then that handler's arguments.
Widths come from survey/ov28/opcode_lengths.json -- which is a STATIC estimate,
so a listing that turns to garbage mid-way is itself evidence the width for the
last opcode is wrong.

Usage:
    python3 scriptdis.py <image.bin> <addr> [count] [--base 0x02000000]
    python3 scriptdis.py --rom <romoffset> [count]
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P

HERE = os.path.dirname(os.path.abspath(__file__))
LEN = json.load(open(os.path.join(HERE, "..", "survey", "ov28", "opcode_lengths.json")))
F8LEN = {int(k): v for k, v in LEN["f8"].items()}
BARE = {int(k): v for k, v in LEN["bare"].items()}
ROM = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"


def listing(data, addr):
    out = []
    i = 0
    text = []

    def flush():
        if text:
            out.append(f"  {addr+start:08x}  TEXT  {''.join(text)!r}")
            text.clear()

    start = 0
    while i < len(data):
        b = data[i]
        if b >= 0xF8:
            flush()
            if b in (0xF8, 0xF9):
                sub = data[i + 1] if i + 1 < len(data) else 0
                n = F8LEN.get(sub, 2)
                args = data[i + 2:i + n]
                out.append(f"  {addr+i:08x}  {b:02X} {sub:02X}  "
                           f"{'len=%d' % n:8} {args.hex()}")
                i += n
            else:
                n = BARE.get(b, 1)
                out.append(f"  {addr+i:08x}  {b:02X}     "
                           f"{'len=%d' % n:8} {data[i+1:i+n].hex()}")
                i += n
            start = i
            continue
        try:
            cc, i2 = P.bytes_to_cc(data, i)
        except IndexError:
            cc, i2 = None, i          # 2-byte charcode truncated by the window
        if cc is None or i2 == i:
            flush()
            out.append(f"  {addr+i:08x}  ?? {b:02X}")
            i += 1
            start = i
            continue
        if not text:
            start = i
        text.append(P.CC2CH.get(cc) or f"<{cc:04x}>")
        i = i2
    flush()
    return "\n".join(out)


if __name__ == "__main__":
    a = sys.argv
    if "--rom" in a:
        off = int(a[a.index("--rom") + 1], 0)
        n = int(a[a.index("--rom") + 2], 0) if len(a) > a.index("--rom") + 2 else 0x80
        data = open(ROM, "rb").read()[off:off + n]
        print(listing(data, off))
    else:
        img = open(a[1], "rb").read()
        base = int(a[a.index("--base") + 1], 0) if "--base" in a else 0x02000000
        addr = int(a[2], 0)
        n = int(a[3], 0) if len(a) > 3 and not a[3].startswith("--") else 0x80
        o = addr - base
        print(listing(img[o:o + n], addr))
