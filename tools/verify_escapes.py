#!/usr/bin/env python3
"""Decode every redirect escape THE WAY THE ENGINE DOES, not the way we wrote it.

Why this exists (session 35, found from a user's photo of the first event):

`region verify` walks escape -> text -> return marker -> terminator and passed
17504/17504 on a build that was visibly broken on hardware. It passed because it
knows which form each escape was written in. **The engine does not.** It decides
at runtime, in this order (tools/redirect_hook.py, label `esc:`):

    b2 == RET_B2  -> return marker
    b2 == ESC_B2  -> long form,   4 bytes, index = u16
    TINY_TBL[b2] != 0xFF -> TINY form, 2 bytes, index = TINY_TBL[b2]
    BANK0_B2 <= b2 < BANK0_B2+BANK_COUNT -> banked form, 3 bytes, index = b3 + bank<<8
    otherwise -> not an escape

`TINY_TBL` is a 256-byte table in the hook block. It was never written -- the
builder had `build_tiny_table()` and nothing called it -- so it held untouched
ARM9 data with ZERO 0xFF bytes, and **every banked escape was taken as a tiny
escape with a garbage index**. `F7 A4 E4` (banked, 「어머？」) became tiny index 0
= 「아～」, whose return address is 0x002346, so the engine carried on from the top
of the script; and it consumed 2 bytes of a 3-byte escape, desyncing the stream
into the screenful of garbage the user photographed.

So this gate reads TINY_TBL **out of the built ROM** and checks, per occurrence:
  * the form the engine picks is the form the budget says we wrote
  * the region entry's return address == run offset + the bytes the engine ate
Both are structural, so there is no encoding ambiguity to argue about.

    python tools/verify_escapes.py rom/DS/PPKP9_kr_v79.nds
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import redirect_hook as R

BASE = os.path.join(HERE, "..")
MANIFEST = os.path.join(BASE, "survey", "redirect_manifest.json")
OV28_FID = 25


def _fat_lo(rom, fid):
    fat = int.from_bytes(rom[0x48:0x4C], "little")
    return int.from_bytes(rom[fat + fid * 8:fat + fid * 8 + 4], "little")


def engine_decode(rom, tiny_tbl, at):
    """(form, index_or_offset, consumed) exactly as the ARM hook dispatches.

    ⭐ SESSION 39: the long form is 5 bytes and its payload is the entry's region
    OFFSET in base-248, not a table index -- so what comes back for "long" is an
    offset. Callers that need an index must use the manifest.
    """
    if rom[at] != R.ESC_B1:
        return None
    b2 = rom[at + 1]
    if b2 == R.RET_B2:
        return ("ret", None, 5)
    if b2 == R.ESC_B2:
        if R.OFFSET_ESC:
            return ("long", R.un248(rom[at + 2:at + 5]), 5)
        return ("long", rom[at + 2] | rom[at + 3] << 8, 4)
    if tiny_tbl[b2] != R.TINY_NONE:
        return ("tiny", tiny_tbl[b2], 2)
    if R.BANK0_B2 <= b2 < R.BANK0_B2 + R.BANK_COUNT:
        return ("bank", rom[at + 2] + ((b2 - R.BANK0_B2) << 8), 3)
    return None


def intended_form(budget):
    if budget == R.TINY_BUDGET:
        return "tiny"
    # Budget 4 moved from the long form to the banked one when the long form grew
    # to 5 bytes (session 39) -- banked is 3 B so it still fits, and it keeps
    # those 797 occurrences instead of stranding them.
    return "bank" if budget < R.LONG_BUDGET else "long"


def check(rom_path, limit=12):
    rom = open(rom_path, "rb").read()
    man = json.load(open(MANIFEST, encoding="utf-8"))
    lo = _fat_lo(rom, OV28_FID)
    t_off = R.ram2rom(R.TINY_TBL)
    tiny_tbl = rom[t_off:t_off + 256]
    tbl = lo + (R.REGION_BASE - R.OV28_RAM)

    want_tbl = R.build_tiny_table()
    if bytes(tiny_tbl) != want_tbl:
        print(f"  !! TINY_TBL at 0x{R.TINY_TBL:08X} is NOT the table the builder "
              f"produces ({sum(1 for b in tiny_tbl if b == 0xFF)} of 256 free "
              f"slots, expected {want_tbl.count(0xFF)}). Every `F7 <b2>` escape "
              f"is mis-dispatched -- redirect_hook.install() must write it.")

    bad, n = [], 0
    for off_s, rec in man.items():
        off = int(off_s, 16)
        got = engine_decode(rom, tiny_tbl, lo + off)
        n += 1
        if got is None:
            bad.append((off, rec, "engine sees no escape here", None))
            continue
        form, idx, used = got
        want = intended_form(rec["budget"])
        if form != want:
            bad.append((off, rec, f"engine reads it as {form}, we wrote {want}", idx))
            continue
        # tiny/banked carry an index and resolve through the table; the long
        # form carries the offset itself, so there is nothing to look up.
        if form == "long" and R.OFFSET_ESC:
            # ⭐ SESSION 39: the long payload is the entry's address minus
            # RET_BASE (main RAM), not an offset from REGION_BASE -- that is what
            # lets an overlay keep its region in its own tail. `tbl` is where
            # this file's region starts, so shift by the gap between the two.
            ent = tbl + (idx + R.RET_BASE - R.REGION_BASE)
        else:
            ent = tbl + int.from_bytes(rom[tbl + idx * 4:tbl + idx * 4 + 4], "little")
        j = ent
        while j < ent + 400 and not (rom[j] == R.ESC_B1 and rom[j + 1] == R.RET_B2):
            j += 1
        if j >= ent + 400:
            bad.append((off, rec, "no return marker in the region entry", idx))
            continue
        # The return marker skips the WHOLE original run, not just the escape --
        # a 4-byte long escape in a 5-byte run is padded and returns to off+5.
        # So the invariant is off+budget, and `used` only has to be <= budget.
        # ⭐ SESSION 39: the marker stores `addr - RET_BASE` (main RAM), not
        # `addr - OV28_RAM`. Overlays 8/9/14 load BELOW overlay 28, so a return
        # into them cannot be expressed relative to it. Convert to the
        # file-relative offset this gate compares against.
        ret = (rom[j + 2] | rom[j + 3] << 8 | rom[j + 4] << 16)             - (R.OV28_RAM - R.RET_BASE)
        if used > rec["budget"]:
            bad.append((off, rec,
                        f"engine eats {used}B of a {rec['budget']}B run", idx))
        elif ret != off + rec["budget"]:
            bad.append((off, rec,
                        f"returns to 0x{ret:06X}, should be "
                        f"0x{off + rec['budget']:06X}", idx))

    print(f"escape verify: {n - len(bad)}/{n} occurrences dispatch and return "
          f"the way the engine will read them")
    for off, rec, why, idx in bad[:limit]:
        print(f"  0x{off:06X} [{rec['budget']}] {rec['jp']} -> {rec['ko']}"
              f"   idx={idx}  {why}")
    if len(bad) > limit:
        print(f"  ... and {len(bad) - limit} more")
    return len(bad)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rom", nargs="?",
                    default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "builds", "PPKP9_kr.nds"))
    a = ap.parse_args()
    sys.exit(1 if check(a.rom) else 0)


if __name__ == "__main__":
    main()
