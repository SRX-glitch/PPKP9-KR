#!/usr/bin/env python3
"""Turn off the kanji-input dictionary the patch has taken the glyphs from.

Why
---
Overlay 13 (file 28) carries a reading-indexed kanji conversion dictionary for
the サクセス name-entry keyboard -- 5,439 index entries -> 1,129 candidate lists
-> 2,768 distinct kanji. 966 of those kanji are drawn by NOTHING else in the
game, so `alloc_plan.py` reclaims them for Hangul (see survey/CENSUS_V2.md).
That is a deliberate trade, but it leaves the name-entry screen showing Hangul
where a kanji candidate should be. Measured on the shipping build: 731
occurrences across 598 charcodes.

How, and why it is a data patch rather than a code patch
-------------------------------------------------------
Each index entry is a u32 pointer to a `FFFF`-terminated u16 candidate list.
Measured on the pristine ROM:

    index table       file 0x2FAEDC - 0x3003D8, 5,439 u32 entries
    targets           all inside the dictionary span 0x2F6380-0x30DE5E
    ALREADY EMPTY     4,342 of 5,439 entries point at a list that starts FFFF

So "this reading has no kanji candidates" is not an edge case the engine might
mishandle -- it is what the engine does for 80% of readings already. Pointing
every entry at an empty list puts the whole keyboard in a state it reaches on
its own thousands of times, with no new code paths.

⚠ Checked before writing: no index entry points outside the dictionary span, and
the player-name arrays (file 28 @0x30F1D4, and the ARM9 ones) are OUTSIDE that
span -- so this cannot affect the names the lineup screen draws. That mattered:
the dictionary and the name arrays live in the same overlay.

    python tools/disable_ime.py            # report only
    python tools/disable_ime.py --verify <built.nds>
"""
import os, sys, argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rom_census as R

FILE_ID = 28
IDX_LO, IDX_HI = 0x2FAEDC, 0x3003D8          # pristine-ROM file offsets
DICT_LO, DICT_HI = 0x2F6380, 0x30DE70


def _layout(rom):
    ov = [o for o in rom.ovl if o["file"] == FILE_ID][0]
    s, _e = rom.span(FILE_ID)
    return ov["ram"], s, ov["size"]


def plan(rom):
    """-> (index_offsets, empty_target_ram) validated against this ROM."""
    b = rom.b
    base, s, size = _layout(rom)
    r2f = lambda a: a - base + s

    entries = list(range(IDX_LO, IDX_HI, 4))
    empty = None
    for off in entries:
        p = int.from_bytes(b[off:off+4], "little")
        if not (base <= p < base + size):
            raise SystemExit(f"index entry 0x{off:06X} -> 0x{p:08X} is outside "
                             f"overlay 13; the table is not what this tool assumes")
        t = r2f(p)
        if not (DICT_LO <= t < DICT_HI):
            raise SystemExit(f"index entry 0x{off:06X} points outside the "
                             f"dictionary span -- refusing to touch it")
        if empty is None and int.from_bytes(b[t:t+2], "little") == 0xFFFF:
            empty = p
    if empty is None:
        raise SystemExit("no already-empty candidate list to point at")
    return entries, empty


def apply(rom_bytes, pristine=None):
    """Point every index entry at an empty candidate list.

    `pristine` is the unmodified ROM the plan is validated against -- the build
    must not derive a patch from bytes it has already written. Returns
    (entries_changed, empty_list_ram).
    """
    src = bytes(pristine) if pristine is not None else bytes(rom_bytes)
    pr = _rom_from(src)
    entries, empty = plan(pr)
    # The offsets above are the PRISTINE file offsets. The build relocates
    # overlays 28/5/8/14/29 into the ROM's tail, so writing at them is only
    # correct while file 28 has not moved. Check rather than assume.
    if _rom_from(bytes(rom_bytes)).span(FILE_ID) != pr.span(FILE_ID):
        raise SystemExit(f"file {FILE_ID} has moved in this build "
                         f"-- disable_ime's offsets are stale")
    blob = empty.to_bytes(4, "little")
    n = 0
    for off in entries:
        if rom_bytes[off:off + 4] != blob:
            rom_bytes[off:off + 4] = blob
            n += 1
    return n, empty


def _rom_from(data):
    r = R.Rom.__new__(R.Rom)
    r.b = data
    b = data
    r.arm9 = (int.from_bytes(b[0x20:0x24], "little"),
              int.from_bytes(b[0x2C:0x30], "little"))
    r.arm7 = (int.from_bytes(b[0x30:0x34], "little"),
              int.from_bytes(b[0x3C:0x40], "little"))
    ov9 = int.from_bytes(b[0x50:0x54], "little")
    r.novl = int.from_bytes(b[0x54:0x58], "little") // 32
    r.fat = int.from_bytes(b[0x48:0x4C], "little")
    r.nfiles = int.from_bytes(b[0x4C:0x50], "little") // 8
    r.ovl = []
    for k in range(r.novl):
        e = b[ov9 + k*32: ov9 + k*32 + 32]
        r.ovl.append({"id": int.from_bytes(e[0:4], "little"),
                      "ram": int.from_bytes(e[4:8], "little"),
                      "size": int.from_bytes(e[8:12], "little"),
                      "bss": int.from_bytes(e[12:16], "little"),
                      "file": int.from_bytes(e[24:28], "little"),
                      "comp": int.from_bytes(e[28:32], "little")})
    r._spans = sorted((r.span(i)[0], r.span(i)[1], i)
                      for i in range(r.nfiles) if r.span(i)[1] > r.span(i)[0])
    r._starts = [x[0] for x in r._spans]
    return r


def report(rom):
    b = rom.b
    base, s, _size = _layout(rom)
    r2f = lambda a: a - base + s
    entries = list(range(IDX_LO, IDX_HI, 4))
    empty = 0
    for off in entries:
        p = int.from_bytes(b[off:off+4], "little")
        if int.from_bytes(b[r2f(p):r2f(p)+2], "little") == 0xFFFF:
            empty += 1
    return len(entries), empty


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify")
    a = ap.parse_args()
    if a.verify:
        rom = R.Rom(a.verify)
        tot, empty = report(rom)
        print(f"{os.path.basename(a.verify)}: {empty}/{tot} index entries have "
              f"NO kanji candidates")
        print("  kanji conversion is "
              + ("OFF (every reading empty)" if empty == tot else "still live"))
        return 0 if empty == tot else 1
    rom = R.Rom()
    tot, empty = report(rom)
    _e, target = plan(rom)
    print(f"pristine ROM: {tot} index entries, {empty} already empty "
          f"({empty/tot*100:.0f}%)")
    print(f"  would repoint all {tot} at the empty list @RAM 0x{target:08X}")


if __name__ == "__main__":
    sys.exit(main() or 0)
