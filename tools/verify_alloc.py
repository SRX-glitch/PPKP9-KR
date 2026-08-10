#!/usr/bin/env python3
"""Gate: does anything the patch writes into glyph storage sit on a DRAWN glyph?

Why this exists
---------------
Session 39 found the baseball lineup corrupted in three independent ways, and
only one of them was the census. The other two were placements:

    redirect_hook.TINY_TBL  0x02087D8C  ->  ﾏ ﾐ ﾑ ﾒ ...   (5 drawn charcodes)
    mte_hook.DICT_REGIONS   9 of 12     ->  ｸ ｻ ｯ ｬ ﾀ ﾄ ﾊ ﾋ 廣 　 ... (46 total)

Those are the halfwidth katakana and the fullwidth padding space that the ARM9
player-name array draws -- 「ｸﾛｰﾊｰ」「ﾀﾙﾋｯｼｭ」「野球ﾏｽｸ」「鈴木　」「廣瀬」. The
MTE dictionary was writing its entries straight over them. That is why the
user's screenshot showed 「セギノール (깨짐)」 and a whole screen of tile garbage
rather than just the four wrong kanji the census bug explains.

TINY_TBL was hand-picked by eye in session 38; DICT_REGIONS came from an
alloc_plan run against the old dialogue-only census. Neither had anything
checking it afterwards.

Every byte of glyph storage the patch claims must be checked against the SAME
census the slots come from, and it must be checked at build time -- not by
whoever remembers to look.

    python tools/verify_alloc.py          # exits nonzero if any placement is unsafe
"""
import os, sys, json, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fontcodec as F
import poketbl as P
import rom_census as R

PROJ = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"
OUT = PROJ + "/survey/font"


def drawn_charcodes(keep_ime=False):
    """charcodes some consumer really draws, under the reclamation policy."""
    raw = {int(k): v for k, v in json.load(open(f"{OUT}/census_v2_usage.json")).items()}
    if keep_ime:
        return set(raw)
    return {cc for cc, s in raw.items() if set(s) - {"ime"}}


def provenance():
    p = {}
    path = f"{OUT}/census_v2_prov.tsv"
    if os.path.exists(path):
        for ln in open(path, encoding="utf-8").read().splitlines()[1:]:
            q = ln.split("\t")
            if len(q) >= 6:
                p[int(q[0])] = (q[2], q[4], q[5])
    return p


def placements():
    """Every (name, addr, nbytes) the patch writes into glyph storage.

    Read from the CONSTANTS the build actually assembles with, not from
    alloc_plan.json -- the point is to catch a constant that drifted away from
    the plan, which is exactly how TINY_TBL went bad.
    """
    import mte_hook as M
    import redirect_hook as RH
    out = [("redirect_hook.HOOK_ADDR", RH.HOOK_ADDR, 1152),
           ("redirect_hook.TINY_TBL", RH.TINY_TBL, 256),
           ("mte_hook.STUB", M.STUB, M.STUB_MAX),
           ("mte_hook.CODE_TBL", M.CODE_TBL, 8 * 64),
           ("mte_hook.STORE_TBL", M.STORE_TBL, 8 * 24)]
    for i, (a, n) in enumerate(M.DICT_REGIONS):
        out.append((f"mte_hook.DICT_REGIONS[{i}]", a, n * 8))
    return out


def main():
    rom = R.Rom()
    tbl = F.load_table(rom.b)
    drawn = drawn_charcodes()
    prov = provenance()

    def span(cc):
        base = tbl[cc >> 6]
        offs = [b for row in F.glyph_map(cc) for b, _ in row]
        return base + min(offs), base + max(offs) + 1

    spans = [(cc, *span(cc)) for cc in range(4352)]
    bad = 0
    for name, addr, nb in placements():
        clash = [cc for cc, s, e in spans
                 if cc in drawn and not (e <= addr or s >= addr + nb)]
        if clash:
            bad += 1
            print(f"FAIL {name} 0x{addr:08X}+{nb} overwrites {len(clash)} drawn glyphs")
            for cc in clash[:6]:
                src, owner, sample = prov.get(cc, ("?", "?", ""))
                print(f"       cc{cc:<5d} {P.CC2CH.get(cc, ''):2s} {src:8s} "
                      f"{owner:>6}  {sample[:36]}")
        else:
            print(f"ok   {name} 0x{addr:08X}+{nb}")

    # the Hangul slots themselves
    if os.path.exists(f"{OUT}/global_slots.json"):
        slots = json.load(open(f"{OUT}/global_slots.json"))
        clash = [c for c in slots if c in drawn]
        if clash:
            bad += 1
            print(f"FAIL global_slots.json: {len(clash)} slots are drawn glyphs")
            for cc in clash[:6]:
                src, owner, sample = prov.get(cc, ("?", "?", ""))
                print(f"       cc{cc:<5d} {P.CC2CH.get(cc, ''):2s} {src:8s} "
                      f"{owner:>6}  {sample[:36]}")
        else:
            print(f"ok   global_slots.json: {len(slots)} slots, none drawn")

    print(f"\nalloc verify: {'FAIL' if bad else 'PASS'} ({bad} unsafe placements)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
