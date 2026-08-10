#!/usr/bin/env python3
"""Insert table text by REPOINTING, so length stops mattering.

`insert_tables` writes Korean inside the record's own bytes, which caps every
label at the original's byte count and forces heavy abbreviation -- the ability
names are limited to three syllables that way. But those records are reached
through an array of absolute RAM pointers, so the alternative is simply:

    put the Korean in the overlay's grown tail, then point at it

and the original record length becomes irrelevant. The pointer array for the
ability names is 307 entries at ROM 0x229644 (RAM 0x02106C64); 59 of them point
at name strings. Whatever a pointer used to reach, it now reaches our string.

Records with no pointer are left to `insert_tables`' in-place path -- they are
still bounded, but they are the minority.

    python tools/insert_pointered.py --report
    python tools/insert_pointered.py --out ROM.nds
"""
import argparse, csv, os, sys

sys.path.insert(0, os.path.dirname(__file__))
import expand_overlay as X
import koenc

ORIG = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
COMMON = os.path.join(os.path.dirname(__file__), "..", "survey", "common")

# Extra worklist keyed by the JAPANESE STRING rather than a ROM offset. The
# offset-based list only holds names of 4 characters or fewer -- the extractor
# dropped longer ones because they could never fit in place -- and those long
# names (パワーヒッター, レーザービーム, ポーカーフェイス, チャンスメーカー ...) are
# exactly what repointing unlocks. 65 of them, translated in file18_pointered.tsv.
EXTRA = {18: ["file18_pointered.tsv"],
         # ⛔ file30_ptr.tsv is NOT wired in yet -- see the warning below.
         30: ["file30_album.tsv", "file30_entries.tsv"],
         13: ["file13_pointered.tsv"],
         4: ["file4_pointered.tsv"]}

# file id -> (worklist, pointer-array ROM offset, entry count)
# The array was located by scanning the file for runs of u32 that land inside the
# overlay's RAM span; 0x229644 is the only run long enough to be a table and it
# is the one that covers the names.
TABLES = {
    18: ("file18_table.tsv", [(0x229644, 307)]),
    # The encyclopedia has ten pointer runs; these two are the ones that matter.
    # 0x32E1FC is the ALBUM TITLE list -- and through a pointer the strings read
    # cleanly as `No01「StaffRoll」`, which is what the in-place extractor could
    # never see: it locked two bytes late and produced 「エ「心の旅」」-shaped junk.
    # Two arrays: album titles and the entry list. Both are reached the same way.
    30: ("file30_table.tsv", [(0x32E1FC, 101), (0x32ECEC, 483)]),
    # Ability effects. In place these are useless -- the records are sentence
    # FRAGMENTS the game concatenates (「手に強く、」), only 1 of 50 fits, and a
    # half-Korean sentence reads worse than the original. Through the pointer
    # array they are COMPLETE strings: 「左打者に強く、球速＋２変化＋１」. Same data,
    # and the difference is entirely which path you read it by.
    13: ("file13_table.tsv", [(0x13C778, 194)]),
    # Item names, shop prompts, stat/pitch boosts -- the strings the shop and
    # equipment screens are made of.
    4: (None, [(0x5707A8, 166)]),
}


def rows(fid):
    name = TABLES[fid][0]
    if name is None:            # pointer-only file: everything comes from EXTRA
        return
    with open(os.path.join(COMMON, name), encoding="utf-8") as f:
        for r in list(csv.reader(f, delimiter="\t"))[1:]:
            if len(r) >= 6 and r[5].strip():
                yield int(r[1], 16), r[4], r[5].strip()


def _decode(rom, off, limit=32):
    """The Japanese at a pointer target, or None if it is not text."""
    import poketbl as P
    out, j = [], off
    while j < off + limit:
        b = rom[j]
        if b == 0xFF:
            break
        if b == 0:
            j += 1
            continue
        if b <= 231:
            cc, j = b - 1, j + 1
        else:
            cc, j = 256 + (b - 232) * 256 + rom[j + 1], j + 2
        c = P.CC2CH.get(cc)
        if c is None:
            return None
        out.append(c)
    return "".join(out) or None


def plan(rom, fid):
    """(pointer ROM offset -> (target, jp, ko)) for every entry we can translate.

    Matching is by the DECODED JAPANESE at the pointer target, not by offset.
    Offsets only cover the short names the extractor kept; going through the
    string lets the same pass pick up the long ones from EXTRA.
    """
    spec = TABLES[fid][1]
    arrays = spec if isinstance(spec, list) else [(spec, TABLES[fid][2])]
    fat = X.u32(rom, 0x48)
    fs = X.u32(rom, fat + fid * 8)
    _, _, ram, size = X.overlay_of_file(rom, fid)
    tr = {jp: ko for _, jp, ko in rows(fid)}
    for name in EXTRA.get(fid, []):
        extra = os.path.join(COMMON, name)
        if not os.path.exists(extra):
            continue
        for ln in open(extra, encoding="utf-8").read().splitlines()[1:]:
            f = ln.rstrip(chr(13)).split(chr(9))
            if len(f) >= 2 and f[0] and f[1]:
                tr.setdefault(f[0], f[1])
    hit, miss = {}, []
    for arr, n in arrays:
        for k in range(n):
            p = arr + 4 * k
            v = X.u32(rom, p)
            if not (ram <= v < ram + size):
                continue
            jp = _decode(rom, fs + (v - ram))
            if jp is None:
                continue
            ko = tr.get(jp)
            if ko:
                hit[p] = (v, jp, ko)
            else:
                miss.append(jp)
    return hit, miss


def apply(rom_in, fid, enc, verbose=True):
    rom = bytearray(rom_in)
    hit, miss = plan(rom, fid)
    # one blob entry per DISTINCT string, so repeats share bytes
    blob, at = bytearray(), {}
    for p, (tgt, jp, ko) in sorted(hit.items()):
        if ko in at:
            continue
        at[ko] = len(blob)
        try:
            blob += enc.encode(ko) + b"\xff"
        except KeyError:
            del at[ko]
    rom, base, _ = X.expand(bytes(rom), fid, bytes(blob))
    rom = bytearray(rom)
    n = 0
    for p, (tgt, jp, ko) in sorted(hit.items()):
        if ko not in at:
            continue
        X.w32(rom, p, base + at[ko])
        n += 1
    if verbose:
        print(f"  repointed {n} entries, blob {len(blob):,}B, "
              f"{len(miss)} records have no pointer (left to in-place)")
    return bytes(rom), n, len(miss)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args()
    rom = open(ORIG, "rb").read()
    enc = koenc.Encoder()
    if a.report:
        for fid in TABLES:
            hit, miss = plan(bytearray(rom), fid)
            print(f"FAT[{fid}]: 번역 가능한 포인터 {len(hit)}개, 미번역 대상 {len(miss)}개")
            for p, (tgt, jp, ko) in list(sorted(hit.items()))[:8]:
                print(f"   ptr@{p:#x} → {jp!r} => {ko!r}")
        return
    if not a.out:
        sys.exit("--report 또는 --out")
    out = rom
    for fid in TABLES:
        out, n, m = apply(out, fid, enc)
    open(a.out, "wb").write(out)
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
