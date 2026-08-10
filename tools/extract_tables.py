#!/usr/bin/env python3
"""Pull the non-dialogue text tables (files 13, 18, 30) into worklists.

These three hold text the `F8 6B` dialogue walk never sees, because they are not
dialogue: they are FF-terminated record tables. Each file uses its own layout,
so there is one entry per file rather than a single clever scanner -- guessing a
universal format is what produced three rounds of garbage.

  18  ability NAMES        FF-terminated, slots aligned to 8 bytes.
                           7 usable bytes => a Korean name may not exceed 3
                           syllables. This is the only hard length limit here.
  13  ability EFFECTS      FF-terminated, records aligned to 4 bytes, variable.
  30  character encyclopedia
                           FF-terminated with 00 padding inside and between
                           records, and `f7 xx` (charcode 0x10xx) icon/control
                           codes sitting between entries.

Scanning a whole file for FF is useless -- binary data is full of it. Every
extraction is therefore bounded to regions where encoded Japanese words actually
cluster, which is the one detection method that has not produced false hits.

    python tools/extract_tables.py            # write all three worklists
    python tools/extract_tables.py --file 18 --list
"""
import argparse, collections, os, sys

sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P
import untranslated as U

ORIG = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
OUT = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/common"

# Words used only to LOCATE text; they are not the extraction itself.
ANCHORS = {
    18: ["三振", "強振", "盗塁", "鉄腕", "剛球", "敬遠", "代打", "送球", "逆境", "回復"],
    13: ["ミート", "パワー", "コントロール", "スタミナ", "球速", "変化",
         "ピンチ", "チャンス", "守備", "走力", "試合中"],
    30: ["ている", "主人公", "という", "になる", "だった", "仲間", "彼女",
         "作成中", "人物", "性格"],
}
ALIGN = {18: 8, 13: 4, 30: 1}
MAXREC = {18: 8, 13: 64, 30: 0x60}


def encode(s):
    b = bytearray()
    for ch in s:
        cc = P.CH2CC.get(ch)
        if cc is None:
            return None
        b += P.cc_to_bytes(cc)
    return bytes(b)


def decode(b, skip_nul=False):
    """charcodes -> text. None if any byte is not a valid charcode."""
    out, j = [], 0
    while j < len(b):
        x = b[j]
        if x == 0 and skip_nul:          # file 30 pads inside a record
            j += 1
            continue
        if 1 <= x <= 231:
            cc, j = x - 1, j + 1
        elif 232 <= x <= 247 and j + 1 < len(b):
            cc, j = 256 + (x - 232) * 256 + b[j + 1], j + 2
        else:
            return None
        ch = P.CC2CH.get(cc)
        if ch is None:
            return None
        out.append(ch)
    return "".join(out)


def regions(rom, lo, hi, words, pad=0x400, gap=0x1000):
    a = []
    for w in words:
        p = encode(w)
        if not p:
            continue
        i = rom.find(p, lo, hi)
        while i >= 0:
            a.append(i)
            i = rom.find(p, i + 1, hi)
    if not a:
        return []
    a.sort()
    groups = [[a[0]]]
    for x in a[1:]:
        if x - groups[-1][-1] <= gap:
            groups[-1].append(x)
        else:
            groups.append([x])
    return [(max(lo, g[0] - pad), min(hi, g[-1] + pad)) for g in groups]


def _plausible(t):
    """Reject decoded binary. Two things give it away every time.

    Struct fields decode to text just as happily as text does, so 'it decoded'
    proves nothing -- what separates them is that real strings are mostly
    kana/kanji and do not repeat a two-character unit over and over (the
    `XねいYねいZねい` shape is an index array, not a sentence).
    """
    if len(t) < 2:
        return False
    if sum(1 for c in t if U.is_jp(c)) / len(t) < 0.6:
        return False
    # An index array reads as one 2-gram hammered over and over
    # (`クホねいぜハねいっィねい...` -- ねい eleven times). Real prose never
    # does that. Count the commonest 2-gram at ANY offset, not just even ones:
    # the earlier even-offset check let this exact shape through at 50%.
    if len(t) >= 8:
        grams = collections.Counter(t[i:i + 2] for i in range(len(t) - 1))
        g, n = grams.most_common(1)[0]
        if n >= 4 and n * 2 >= len(t) * 0.3:
            return False
    return True


def records(rom, fid, lo, hi):
    """Records, read the way each file actually stores them.

    File 18 needs the strictest rule and it is the reason this is per-file: its
    names live in fixed 8-byte slots, but the SAME region also holds parameter
    arrays, so scanning forward from an arbitrary offset splices struct bytes
    onto the front of a name (`おえういノビ○` instead of `ノビ○`). Demanding a
    slot-conformant record -- 8-aligned, FF inside, nothing but NUL after it --
    is what tells a name apart from the numbers packed next to it.
    """
    align, maxrec = ALIGN[fid], MAXREC[fid]
    out = []
    if fid == 18:
        for o in range(lo - lo % align, hi, align):
            k = rom.find(b"\xff", o, min(o + align, hi))
            if k < 0 or k == o:
                continue
            if any(rom[x] != 0 for x in range(k + 1, min(o + align, hi))):
                continue                    # slot tail must be pure padding
            t = decode(rom[o:k])
            if t and _plausible(t) and len(t) <= 4:
                out.append((o, t))
        return out

    skip = fid == 30
    o = lo
    while o < hi:
        if skip:
            while o < hi and rom[o] in (0x00, 0xFF):
                o += 1
            if o >= hi:
                break
        k = rom.find(b"\xff", o, min(o + maxrec, hi))
        if k < 0 or k == o:
            o += 1 if skip else align
            continue
        t = decode(rom[o:k], skip_nul=skip)
        if t and _plausible(t):
            out.append((o, t))
            o = k + 1 if skip else (k + 1 + align - 1) // align * align
        else:
            o += 1 if skip else align
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", type=int, choices=sorted(ANCHORS))
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()

    rom = open(ORIG, "rb").read()
    spans = {i: (s, e) for s, e, i in U.fat_files(rom)}
    for fid in ([a.file] if a.file else sorted(ANCHORS)):
        s, e = spans[fid]
        recs = []
        for lo, hi in regions(rom, s, e, ANCHORS[fid]):
            recs += records(rom, fid, lo, hi)
        freq = collections.Counter(t for _, t in recs)
        path = os.path.join(OUT, f"file{fid}_table.tsv")
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("n\toffset\toccurrences\tmax_syl\tjp\tko\n")
            seen, n = set(), 0
            for off, t in recs:
                if t in seen:
                    continue
                seen.add(t)
                n += 1
                # only file 18 has a hard slot; elsewhere leave it blank
                cap = 3 if fid == 18 else ""
                f.write(f"{n}\t{off:#x}\t{freq[t]}\t{cap}\t{t}\t\n")
        print(f"FAT[{fid}]  records {len(recs):5}  distinct {len(freq):5}  -> {path}")
        if a.list:
            for t, c in freq.most_common():
                print(f"   x{c:<3} {t}")


if __name__ == "__main__":
    main()
