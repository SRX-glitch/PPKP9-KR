#!/usr/bin/env python3
"""Plan an EXT_RANGES -> CODE_RANGES trade and print the two lists to paste.

More MTE codes can only come out of the extension glyph slots -- the alias
charcode space is full, so it is a split, not a choice of both. Doing the split
by hand is where the mistakes live: the ranges must stay ascending and
non-overlapping, must not exceed the 31-range tables, and (unless the page count
is deliberately being changed) every extension page must keep at least one
charcode, because `len(EXT_BLOCKS)` feeds redirect_hook.EXT_PAGE_BYTES and
REGION_BASE.

    python tools/plan_ext_trade.py 200          # move 200 more codes, keep 7 pages
    python tools/plan_ext_trade.py 200 --pages 5  # allow the page count to drop

Takes from the TOP: build_fontpack fills `extra` in ascending charcode order from
a priority-ordered syllable list, so the highest extension slots hold the
lowest-priority KS X 1001 filler.
"""
import os, sys, argparse, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mte_hook as M

FONT = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font"


def runs(codes):
    """sorted charcodes -> [(base, count)] contiguous runs."""
    out = []
    for cc in sorted(codes):
        if out and cc == out[-1][0] + out[-1][1]:
            out[-1][1] += 1
        else:
            out.append([cc, 1])
    return [(b, c) for b, c in out]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("move", type=int, help="how many more codes to hand over")
    ap.add_argument("--pages", type=int, default=len(M.EXT_BLOCKS),
                    help="extension pages to keep non-empty (default: current)")
    a = ap.parse_args()

    ext = sorted(M.EXT_CODES)
    keep_blocks = sorted({cc // 64 for cc in ext})[:a.pages]
    # one anchor per page we intend to keep: its LOWEST charcode, so the slots we
    # give away stay the contiguous top of the space
    anchors = set()
    for blk in keep_blocks:
        inblk = [cc for cc in ext if cc // 64 == blk]
        if inblk:
            anchors.add(min(inblk))

    give, spare = [], [cc for cc in ext if cc not in anchors]
    for cc in reversed(spare):              # from the top
        if len(give) >= a.move:
            break
        give.append(cc)
    new_ext = [cc for cc in ext if cc not in set(give)]
    new_code = sorted(set(give) | {cc for b, c in M.CODE_RANGES
                                   for cc in range(b, b + c)})

    er, cr = runs(new_ext), runs(new_code)
    used = 0
    p = os.path.join(FONT, "kr_font_map.json")
    if os.path.exists(p):
        used = len(json.load(open(p, encoding="utf-8")))
    plain = 1238                            # ARM9-resident slots, unchanged

    print(f"moved {len(give)} codes  (asked {a.move})")
    print(f"EXT  {len(M.EXT_CODES)} -> {len(new_ext)} slots, {len(er)} ranges "
          f"(table holds 31), pages {sorted({cc//64 for cc in new_ext})}")
    print(f"CODE {M.CODE_CAP} -> {len(new_code)} codes, {len(cr)} ranges, "
          f"store cap {M.STORE_CAP} -> MAX_ENTRIES "
          f"{min(len(new_code), M.STORE_CAP)}")
    print(f"font free {plain + len(new_ext)} vs {used} syllables currently mapped")
    if len(er) > 31 or len(cr) > 31:
        print("  ⛔ range table overflow (31 max per table)")
    if plain + len(new_ext) < 1300:
        print("  ⚠ font free is getting close to what real translations use")
    print()
    print("EXT_RANGES = [")
    for i in range(0, len(er), 5):
        print("    " + " ".join(f"(0x{b:04X}, {c})," for b, c in er[i:i + 5]))
    print(f"]  # {len(new_ext)} slots")
    print("CODE_RANGES = [")
    for i in range(0, len(cr), 5):
        print("    " + " ".join(f"(0x{b:04X}, {c})," for b, c in cr[i:i + 5]))
    print(f"]  # {len(new_code)} MTE codes")


if __name__ == "__main__":
    main()
