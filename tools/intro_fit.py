#!/usr/bin/env python3
"""Budget-check translation/intro_lines.tsv without running a whole build.

The intro is patched in place at absolute ROM offsets -- no redirect region is
reachable from the cutscene walker -- so every line has a hard budget equal to
the original Japanese run's byte length. build_kr reports overruns, but only
after several minutes of font and overlay work; this does the same check in a
second so the wording can be iterated.

Also re-verifies the Japanese bytes at each offset, which is what catches an
entry whose offset drifted onto an opcode operand.

⚠ The numbers here are ADVISORY, not authoritative. The MTE dictionary is trained
during the build from the worklist itself, so this can only score against the
PREVIOUS build's `kr_map.json`. A line that reads OVER here may well fit once the
trainer mints an entry for it -- that is exactly what the `hard` priority in
build_kr's train_mte exists to do. build_kr's own `INTRO OVER` report is the
authority. Scoring without MTE at all, though, is simply wrong: 「그래」 ships as
one 2-byte code, not four bytes.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import koenc

BASE = r"C:/Users/jngji/Desktop/실험실"
ROM = BASE + r"/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
TSV = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/translation/intro_lines.tsv"
FONTMAP = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font/kr_font_map.json"
KRMAP = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font/kr_map.json"
SPACE_BYTES = "00"


def main():
    rom = open(ROM, "rb").read()
    fontmap = json.load(open(FONTMAP, encoding="utf-8"))
    mte = {}
    if os.path.exists(KRMAP):
        mte = json.load(open(KRMAP, encoding="utf-8")).get("mte", {})
    enc = koenc.Encoder({"syl": fontmap, "one": {}, "mte": mte,
                         "raw": {" ": SPACE_BYTES}})

    over = bad = ok = 0
    for ln in open(TSV, encoding="utf-8").read().splitlines()[1:]:
        p = ln.split("\t")
        if len(p) < 3 or not p[0].strip():
            continue
        off, jp, ko = int(p[0], 16), p[1].strip(), p[2].strip()
        want = koenc.encode_jp(jp) if hasattr(koenc, "encode_jp") else None
        if want is None:
            import poketbl as P
            want = bytearray()
            for ch in jp:
                cc = P.CH2CC[ch]
                if cc < 231:
                    want.append(cc + 1)
                else:
                    want += bytes([232 + (cc - 256) // 256, (cc - 256) % 256])
            want = bytes(want)
        got = rom[off:off + len(want)]
        if got != want:
            print(f"MISMATCH 0x{off:06X} {jp!r}\n  rom={got.hex()}\n  exp={want.hex()}")
            bad += 1
            continue
        b = enc.encode(ko)
        if len(b) > len(want):
            print(f"OVER     0x{off:06X} {len(b)}B > {len(want)}B  {jp!r} -> {ko!r}")
            over += 1
        else:
            ok += 1
    print(f"\nintro_lines: {ok} fit, {over} over budget, {bad} offset mismatch")
    return 1 if (over or bad) else 0


if __name__ == "__main__":
    sys.exit(main())
