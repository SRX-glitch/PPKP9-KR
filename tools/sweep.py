#!/usr/bin/env python3
"""Sweep a BUILT ROM for the defect classes that make the engine derail.

Session 35's lesson, paid for three times over (sessions 29/33/34 each blamed a
different innocent thing): the build's gates check **what we wrote**. The engine
reads bytes and decides for itself. Anything that changes its decision -- a
lookup table we forgot to write, a charcode that collides with an opcode lead, a
redirect that returns to a byte that is not a boundary -- is invisible to a gate
that already knows the answer.

Every check here is phrased as "what will the CPU do with these bytes", and every
one of them runs against a finished ROM, so any build can be swept without
rebuilding it:

    python tools/sweep.py rom/DS/PPKP9_kr_v79.nds

  [1] TINY_TBL is the table the builder produces (it was never written at all
      until session 35, which sent 738 redirects to the top of the script)
  [2] every redirect dispatches, and returns, the way the hook will read it
      (tools/verify_escapes.py -- replays the hook's own dispatch order)
  [3] no Hangul charcode encodes with a lead byte >= 0xF7, i.e. no glyph can be
      mistaken for an escape (0xF7) or an opcode (0xF8+)
  [4] no charcode the shipping text DRAWS is also handed out as a tiny escape
      code -- the halfwidth digits '0'-'9' are 4177-4186, i.e. `F7 51`-`F7 5A`,
      so they sit in the escape band and one stale census would swallow them
  [5] every redirect returns to a run boundary the extractor recorded, so the
      engine resumes on an opcode and not in the middle of one

Exit code is the number of failing checks.
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import redirect_hook as R
import verify_escapes as VE

BASE = os.path.join(HERE, "..")
SHIPPING = (4, 25, 27)          # files insert_extra writes
OV28_FID = 25


ORIG = os.path.join(BASE, "..", "rom", "DS",
                    "Power Pro Kun Pocket 9 (Japan).nds")
_PRIS = {}


def _pristine_lo(fid):
    """Worklist offsets are pristine-ROM offsets; shipped files have moved."""
    if fid not in _PRIS:
        _PRIS[fid] = _fat(open(ORIG, "rb").read(), fid)[0]
    return _PRIS[fid]


def _load(rom_path):
    return open(rom_path, "rb").read()


def _fat(rom, fid):
    fat = int.from_bytes(rom[0x48:0x4C], "little")
    lo = int.from_bytes(rom[fat + fid * 8:fat + fid * 8 + 4], "little")
    hi = int.from_bytes(rom[fat + fid * 8 + 4:fat + fid * 8 + 8], "little")
    return lo, hi


def check_tiny_table(rom):
    o = R.ram2rom(R.TINY_TBL)
    got, want = rom[o:o + 256], R.build_tiny_table()
    if got == want:
        print(f"[1] tiny table   OK   {want.count(0xFF)} reserved slots at "
              f"0x{R.TINY_TBL:08X}")
        return 0
    print(f"[1] tiny table   FAIL 0x{R.TINY_TBL:08X} is not build_tiny_table(): "
          f"{sum(1 for b in got if b == 0xFF)} reserved slots, expected "
          f"{want.count(0xFF)}. Every `F7 <b2>` escape mis-dispatches.")
    return 1


def check_escapes(rom_path):
    print("[2] escape decode", end=" ")
    return 1 if VE.check(rom_path, limit=6) else 0


def check_font_band():
    fm = json.load(open(os.path.join(BASE, "survey", "font", "kr_font_map.json"),
                        encoding="utf-8"))
    bad = [(ch, int(cc)) for ch, cc in fm.items()
           if int(cc) >= 231 and 232 + (int(cc) - 256) // 256 >= R.ESC_B1]
    if not bad:
        top = max(int(v) for v in fm.values())
        print(f"[3] glyph band   OK   {len(fm)} syllables, max charcode {top} "
              f"(lead 0x{232 + (top - 256) // 256:02X}, escape lead is "
              f"0x{R.ESC_B1:02X})")
        return 0
    print(f"[3] glyph band   FAIL {len(bad)} syllables encode with a lead byte "
          f">= 0x{R.ESC_B1:02X}: {bad[:8]}")
    return 1


def _recorded_runs(fid):
    """(offset, budget) for every run the extractor recorded in this file.

    ⚠ Scoping matters. Files 4/25/27 are mostly graphics and tables -- scanning
    them end to end finds ~40,000 0xF7 bytes that are simply binary data and
    ~400 "failures" that mean nothing. The engine only interprets the bytes it
    walks as TEXT, so only recorded runs may be judged.
    """
    p = os.path.join(BASE, "survey", "common", f"file{fid}_extra.tsv")
    out = []
    if os.path.exists(p):
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            f = ln.split("\t")
            if len(f) >= 2:
                try:
                    out.append((int(f[0], 16), int(f[1])))
                except ValueError:
                    pass
    return out


def check_tiny_collisions(rom):
    """No charcode the shipping text actually draws may be a tiny escape code.

    ⛔ This is the sharpest edge in the whole design and it is one stale file
    away from a disaster. `F7` is the escape lead AND the lead byte of charcodes
    4096-4351 -- which includes the **halfwidth ASCII digits**: '0' is 4177 =
    `F7 51`, '9' is 4186 = `F7 5A`. `tiny_codes()` hands out F7-band codes that
    `survey/font/global_usage.json` says the ROM never draws. If that census
    ever misses a character we go on to use, its code becomes a tiny escape and
    **every line containing that character is swallowed as a redirect** -- the
    same failure mode as the unwritten TINY_TBL, one character at a time.

    A `F7 <b2>` that dispatches to nothing is FINE: the hook falls through to
    `back` and the engine decodes it as the ordinary 2-byte charcode it is. So
    the thing to check is not "does it dispatch" but "does a code we DRAW also
    dispatch".
    """
    o = R.ram2rom(R.TINY_TBL)
    tiny = rom[o:o + 256]
    used, runs = {}, 0
    for fid in SHIPPING:
        lo, _ = _fat(rom, fid)
        delta = lo - _pristine_lo(fid)
        for off, budget in _recorded_runs(fid):
            # ⚠ Two offset conventions here: the extra worklists hold ABSOLUTE
            # pristine-ROM offsets (rebase with delta, as insert_extra does),
            # while survey/ov28/dialogue_runs.tsv holds overlay-RELATIVE ones.
            runs += 1
            i, end = off + delta, off + delta + budget
            while i < end:
                if rom[i] == R.ESC_B1:
                    got = VE.engine_decode(rom, tiny, i)
                    if got is None:                 # a plain 2-byte charcode
                        used.setdefault(rom[i + 1], (fid, off))
                        i += 2
                    else:
                        i += got[2]
                else:
                    i += 1
    clash = [(b2, w) for b2, w in used.items() if tiny[b2] != R.TINY_NONE]
    if not clash:
        print(f"[4] F7-band      OK   {len(used)} drawn F7-band codes across "
              f"{runs:,} runs, none is a tiny escape code")
        return 0
    print(f"[4] F7-band      FAIL {len(clash)} charcodes are BOTH drawn and "
          f"handed out as tiny escapes -- every line using them is swallowed:")
    for b2, (fid, off) in clash[:8]:
        print(f"      charcode {4096 + b2} (F7 {b2:02X}) -> tiny idx "
              f"{tiny[b2]}   e.g. file{fid} 0x{off:X}")
    return 1


def check_return_boundaries(rom):
    """Every redirect must resume on a byte the extractor called a boundary."""
    p = os.path.join(BASE, "survey", "ov28", "dialogue_runs.tsv")
    if not os.path.exists(p):
        print("[5] return sites  SKIP dialogue_runs.tsv missing")
        return 0
    ok = set()
    for ln in open(p, encoding="utf-8").read().splitlines():
        f = ln.split("\t")
        if len(f) >= 2:
            try:
                ok.add(int(f[0], 16) + int(f[1]))   # where the run ends
                ok.add(int(f[0], 16))
            except ValueError:
                pass
    man = json.load(open(VE.MANIFEST, encoding="utf-8"))
    lo, _ = _fat(rom, OV28_FID)
    o = R.ram2rom(R.TINY_TBL)
    tiny = rom[o:o + 256]
    tbl = lo + (R.REGION_BASE - R.OV28_RAM)
    bad = []
    for off_s, rec in man.items():
        off = int(off_s, 16)
        got = VE.engine_decode(rom, tiny, lo + off)
        if got is None or got[0] == "ret":
            continue
        ent = tbl + int.from_bytes(rom[tbl + got[1] * 4:tbl + got[1] * 4 + 4],
                                   "little")
        j = ent
        while j < ent + 400 and not (rom[j] == R.ESC_B1 and rom[j + 1] == R.RET_B2):
            j += 1
        if j >= ent + 400:
            continue
        ret = rom[j + 2] | rom[j + 3] << 8 | rom[j + 4] << 16
        if ret not in ok:
            bad.append((off, ret, rec["jp"]))
    if not bad:
        print(f"[5] return sites OK   {len(man):,} redirects resume on a "
              f"recorded run boundary")
        return 0
    print(f"[5] return sites FAIL {len(bad)} resume mid-stream:")
    for off, ret, jp in bad[:6]:
        print(f"      0x{off:06X} {jp} -> resumes at 0x{ret:06X}")
    return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rom")
    a = ap.parse_args()
    rom = _load(a.rom)
    print(f"sweep {os.path.basename(a.rom)}  ({len(rom):,} B)\n")
    fails = (check_tiny_table(rom) + check_escapes(a.rom) + check_font_band()
             + check_tiny_collisions(rom) + check_return_boundaries(rom))
    print(f"\n{fails} check(s) failed")
    sys.exit(fails)


if __name__ == "__main__":
    main()
