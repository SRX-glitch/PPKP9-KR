#!/usr/bin/env python3
"""Locate the REAL text regions by byte-searching common Japanese words.

Each word encodes to a fixed PokeTEXT byte sequence, so a plain bytes.find over
the ROM is both fast and noise-proof: random data almost never reproduces these.
"""
import os, sys, collections, json
sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

ROM = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
OUTDIR = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font"
rom = open(ROM, "rb").read()

WORDS = ["です", "ます", "でした", "ました", "ですね", "ですか", "だろう", "だけど",
         "そうだ", "ない", "する", "った", "って", "から", "けど", "でも",
         "という", "ように", "こと", "もの", "ちょっと", "やっぱり", "ありがとう",
         "がんばれ", "おれ", "ぼく", "きみ", "みんな", "せんぱい", "かんとく"]


def enc(s):
    out = bytearray()
    for ch in s:
        cc = P.CH2CC.get(ch)
        if cc is None:
            return None
        out += P.cc_to_bytes(cc)
    return bytes(out)


hits = []
for w in WORDS:
    b = enc(w)
    if not b or len(b) < 3:
        continue
    i = rom.find(b)
    c = 0
    while i != -1:
        hits.append((i, w))
        c += 1
        i = rom.find(b, i + 1)
    print(f"{w:10s} {b.hex():16s} {c:6d} hits")

hits.sort()
print(f"\ntotal hits: {len(hits)}")

# cluster hits into regions
BUCKET = 0x10000
buckets = collections.Counter(off // BUCKET for off, _ in hits)
hot = sorted(b for b, c in buckets.items() if c >= 5)
print(f"hot 64KB buckets (>=5 hits): {len(hot)}")


def merge(bs, gap=2):
    out = []
    s = p = bs[0]
    for x in bs[1:]:
        if x - p <= gap:
            p = x; continue
        out.append((s, p)); s = p = x
    out.append((s, p))
    return out


regions = [(s * BUCKET, (e + 1) * BUCKET) for s, e in merge(hot)]
tot = sum(e - s for s, e in regions)
print(f"\nmerged text regions: {len(regions)}, total {tot/1e6:.2f} MB "
      f"({tot*100/len(rom):.1f}% of ROM)")
for s, e in regions:
    c = sum(1 for off, _ in hits if s <= off < e)
    print(f"  0x{s:07X}-0x{e:07X}  {(e-s)/1024:7.0f} KB  {c:6d} word hits")

json.dump(regions, open(os.path.join(OUTDIR, "text_regions.json"), "w"))
print("\nwrote text_regions.json")
