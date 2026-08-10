#!/usr/bin/env python3
"""What Japanese text is still in the shipped ROM, and which file owns it?

Our corpus is overlay 28 (the Nice Guy script) plus the intro region. Everything
else -- menu labels, item names, the baseball UI, other scenarios -- was never in
the worklist, so "coverage 90%" says nothing about it. This walks every `F8 6B`
text run in the ROM, decodes it with the PATCHED tables (so our Korean reads as
Korean rather than as whatever Japanese character now shares its charcode), and
reports the runs that still decode to kana/kanji, grouped by the FAT file they
land in.

    python tools/untranslated.py                    # summary by file
    python tools/untranslated.py --file 25 --list   # dump one file's strings
"""
import argparse, json, os, sys, collections

sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

BASE = r"C:/Users/jngji/Desktop/실험실"
DEPLOY = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/builds/PPKP9_kr.nds"
KRMAP = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font/kr_map.json"


def is_jp(ch):
    o = ord(ch)
    # ・ (U+30FB) and ー (U+30FC) sit in the kana block but are punctuation our
    # Korean uses too -- counting them flagged 「으음・・・뭔가」 as untranslated
    # and inflated the total by thousands.
    if o in (0x30FB, 0x30FC):
        return False
    return (0x3040 <= o <= 0x30FF          # kana
            or 0x4E00 <= o <= 0x9FFF       # kanji
            or 0x3400 <= o <= 0x4DBF)


def has_kr(s):
    return any(0xAC00 <= ord(c) <= 0xD7A3 or 0x3130 <= ord(c) <= 0x318F for c in s)


def load_rev():
    """charcode -> what it actually draws in the patched ROM."""
    rev = dict(P.CC2CH)
    m = json.load(open(KRMAP, encoding="utf-8"))
    for k, v in m["syl"].items():
        rev[int(v)] = k
    for k, v in m.get("one", {}).items():
        rev[int(v)] = k
    for k, v in m.get("mte", {}).items():   # a dictionary code draws a whole run
        rev[int(v)] = k
    return rev


def fat_files(rom):
    off = int.from_bytes(rom[0x48:0x4C], "little")
    size = int.from_bytes(rom[0x4C:0x50], "little")
    out = []
    for i in range(size // 8):
        s = int.from_bytes(rom[off + i * 8:off + i * 8 + 4], "little")
        e = int.from_bytes(rom[off + i * 8 + 4:off + i * 8 + 8], "little")
        if e > s:
            out.append((s, e, i))
    out.sort()
    return out


def owner(files, o):
    for s, e, i in files:
        if s <= o < e:
            return i
    return None


def runs(rom, rev):
    """(offset, text) for every `F8 6B` text run."""
    i, n = 0, len(rom)
    while i < n - 3:
        if rom[i] == 0xF8 and rom[i + 1] == 0x6B:
            start, j, s = i, i + 3, []
            while j < n and rom[j] != 0 and rom[j] < 0xF8:
                b = rom[j]
                if 1 <= b <= 231:
                    s.append(rev.get(b - 1, "\ufffd")); j += 1
                else:
                    cc = 256 + (b - 232) * 256 + rom[j + 1]
                    s.append(rev.get(cc, "\ufffd")); j += 2
            yield start, "".join(s)
            i = j
        else:
            i += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom", default=DEPLOY)
    ap.add_argument("--file", type=int, help="only this FAT file id")
    ap.add_argument("--list", action="store_true", help="print the strings")
    ap.add_argument("--min-jp", type=int, default=2,
                    help="a run needs this many JP chars to count (1 filters noise)")
    a = ap.parse_args()

    rom = open(a.rom, "rb").read()
    rev = load_rev()
    files = fat_files(rom)
    print(f"{os.path.basename(a.rom)}  {len(rom):,}B   FAT files: {len(files)}")

    per = collections.defaultdict(list)
    total = jp_total = 0
    for off, text in runs(rom, rev):
        total += 1
        # A run that already carries Hangul is ours -- a stray kanji in it is a
        # name or a leftover particle, not an untranslated string.
        if has_kr(text) or sum(1 for c in text if is_jp(c)) < a.min_jp:
            continue
        jp_total += 1
        per[owner(files, off)].append((off, text))

    print(f"text runs: {total:,}   still Japanese: {jp_total:,}\n")
    print(f"{'file':>6} {'runs':>6}  sample")
    for fid, items in sorted(per.items(), key=lambda kv: -len(kv[1])):
        if a.file is not None and fid != a.file:
            continue
        sample = " | ".join(t[:18] for _, t in items[:3])
        name = "ARM9/overlay-hdr" if fid is None else str(fid)
        print(f"{name:>6} {len(items):>6}  {sample}")
        if a.list:
            for off, t in items:
                print(f"         {off:#09x}  {t}")


if __name__ == "__main__":
    main()
