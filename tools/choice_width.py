# -*- coding: utf-8 -*-
"""choice_width.py -- find choice-PREVIEW sibling groups whose widths differ.

Session 45: the fishing previews (0x50FC16 「今日の食事分は確保した。」 /
0x50FC2B 「たった今、一人釣れた。」) are consecutive `F8 F8 <text> D0` segments
drawn into ONE box as the cursor moves. The engine clears roughly the NEW
text's width, so a shorter Korean line leaves the tail of the previous one on
screen (「방금 낚였다보했다」). The fix is equal rendered widths per group.

This tool walks a BUILT ROM's dialogue files for F8 F8 preview groups, decodes
each sibling's rendered cell width (2-byte charcode = 1 cell, 1-byte charcode =
1 cell, 0x00 = 1 blank cell, escapes = UNKNOWN), and reports groups whose
sibling widths differ. Groups containing F7 escapes are listed for manual
checking (the drawn text lives in the region).

    PYTHONIOENCODING=utf-8 python tools/choice_width.py builds/PPKP9_kr_v222_fixups.nds
"""
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAMEDIR = os.path.dirname(BASE)
BUILD = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    BASE, "builds", "PPKP9_kr_v222_fixups.nds")

FIDS = (4, 8, 18, 20, 25, 27, 30)
TERM = {0xD0, 0xD1, 0xD7, 0xD8}          # segment enders seen in preview blocks


def fat_span(rom, fid):
    fat = int.from_bytes(rom[0x48:0x4C], "little")
    return (int.from_bytes(rom[fat + fid * 8:fat + fid * 8 + 4], "little"),
            int.from_bytes(rom[fat + fid * 8 + 4:fat + fid * 8 + 8], "little"))


def seg_width(buf, i, end):
    """(cells, has_escape, next_index) for one preview segment starting at i."""
    cells = 0
    esc = False
    while i < end:
        b = buf[i]
        if b in TERM or (b == 0xF8 and i + 1 < end and buf[i + 1] == 0xF8):
            return cells, esc, i
        if b == 0xF7:                      # redirect escape -- width unknowable
            esc = True
            i += 2
            continue
        if b == 0xF8:                      # other opcode: stop the segment
            return cells, esc, i
        if b >= 0xE8:                      # 2-byte charcode, one full cell
            cells += 1
            i += 2
        else:                              # 1-byte charcode / 0x00 blank
            cells += 1
            i += 1
    return cells, esc, i


def main():
    rom = open(BUILD, "rb").read()
    print(f"choice-preview width audit: {os.path.basename(BUILD)}")
    bad = manual = groups = 0
    for fid in FIDS:
        lo, hi = fat_span(rom, fid)
        i = lo
        while i < hi - 2:
            if rom[i] == 0xF8 and rom[i + 1] == 0xF8:
                # walk the whole group of consecutive F8F8 segments
                sibs = []
                j = i
                while j < hi - 2 and rom[j] == 0xF8 and rom[j + 1] == 0xF8:
                    w, esc, k = seg_width(rom, j + 2, hi)
                    sibs.append((j, w, esc))
                    # skip the terminator if present
                    if k < hi and rom[k] in TERM:
                        k += 1
                    if k <= j:
                        break
                    j = k
                i = j + 1
                if len(sibs) < 2:
                    continue
                groups += 1
                widths = [w for _o, w, _e in sibs]
                if any(e for _o, _w, e in sibs):
                    if max(widths) != min(widths):
                        manual += 1
                        print(f"  ⚠ f{fid} group@0x{sibs[0][0]:06X} "
                              f"widths={widths} (escape inside -- check manually)")
                elif max(widths) - min(widths) >= 2:
                    bad += 1
                    print(f"  ⛔ f{fid} group@0x{sibs[0][0]:06X} widths={widths}")
            else:
                i += 1
    print(f"\n{groups} preview groups scanned: {bad} width-mismatched (>=2 cells), "
          f"{manual} with escapes to check manually")


if __name__ == "__main__":
    main()
