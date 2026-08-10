#!/usr/bin/env python3
"""Read back EVERY main-scenario run from a built ROM and say what it really holds.

The build's `text verify` checks the occurrences it wrote. A run it never wrote,
or wrote partially, or dropped at the region cap, is simply not in its list -- so
25043/25043 can be green while a line on screen is neither Korean nor Japanese:

    0x059F10 [9] ああ、そうなんだ。   want 「아、그렇구나。」
                 in the ROM:          「아、て   」

That is what "a weird conversation appears out of nowhere" looks like from the
byte side. This walks `survey/ov28/dialogue_runs.tsv` -- every run, not a
worklist -- resolves each one the way the engine does (inline, tiny, banked or
long redirect), decodes it, and sorts the result into:

    korean    the Korean we meant to ship
    japanese  the original, deliberately left (over budget, no region slot)
    MANGLED   neither -- a partial write, and a real defect

    python tools/scan_runs.py rom/DS/PPKP9_kr_v79.nds [--show 40]
"""
import argparse, glob, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import redirect_hook as R
import poketbl as P
import walk_audit as W

BASE = os.path.join(HERE, "..")
TDIR = os.path.join(BASE, "translation")
OV28_FID = 25


def _inv_map():
    km = json.load(open(os.path.join(BASE, "survey", "font", "kr_map.json"),
                        encoding="utf-8"))
    out = {}
    # ⚠ BOTH tables. `mte` maps a MULTI-syllable string to ONE charcode -- the
    # engine expands it at draw time. A reader that only knows `syl` decodes an
    # MTE code as whatever Japanese glyph that charcode used to be, which made
    # 4,523 good runs look mangled: 「오늘은、」 read back as 「み、」.
    for key in ("syl", "mte"):
        for ch, cc in km.get(key, {}).items():
            try:
                out[int(cc)] = ch
            except (TypeError, ValueError):
                pass
    return out


def _extra_worklists():
    """jp -> ko from the `file*_extra.tsv` worklists.

    ⛔ Session 35: leaving these out made `scan_runs` call 3,023 runs "never
    translated" when a large share of them ship Korean through `insert_extra`.
    Worse, it sent me off to translate 107 of them by hand -- 58 collided with a
    translation that was already there, two inserters claimed the same run, and
    the `extra verify` gate failed the build. A read-back tool has to know EVERY
    path that writes text, not just the one it was written for.
    """
    out = {}
    for p in sorted(glob.glob(os.path.join(BASE, "survey", "common",
                                           "file*_extra.tsv"))):
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            f = ln.split("	")
            if len(f) >= 6 and f[4].strip() and f[5].strip():
                out.setdefault(f[4].strip(), f[5].strip())
    return out


def _batches():
    def key(p):
        m = re.search(r"batch(\d+)", os.path.basename(p))
        return int(m.group(1)) if m else 0
    out = {}
    for p in sorted(glob.glob(os.path.join(TDIR, "batch*.tsv")), key=key):
        for ln in open(p, encoding="utf-8").read().splitlines():
            f = ln.split("\t")
            if len(f) >= 2 and f[0].strip() and f[1].strip():
                out[f[0].strip()] = f[1].strip()
    return out


def decode(rom, i, end, inv):
    o = []
    while i < end:
        b = rom[i]
        if b >= 232:
            cc = (b - 232) * 256 + rom[i + 1] + 256
            i += 2
            o.append(inv.get(cc, P.CC2CH.get(cc, "�")))
        else:
            o.append(" " if b == 0 else P.CC2CH.get(b - 1, "�"))
            i += 1
    return "".join(o)


def read_run(rom, lo, off, budget, inv, tiny=None):
    """(text, how) for one run, resolved the way the engine resolves it.

    ⚠ All THREE escape forms have to be handled, in the hook's own order. An
    earlier cut of this scanner skipped the 2-byte TINY form and decoded those
    runs as raw charcodes, which made 4,726 perfectly good redirects look like
    byte corruption -- 「아～」 read back as 「ｱ」. If a read-back tool does not
    know a form the engine knows, its "corruption" is its own.
    """
    b = rom[lo + off:lo + off + 5]
    if b[0] == R.ESC_B1:
        if b[1] == R.ESC_B2:
            idx = b[2] | b[3] << 8
        elif tiny is not None and tiny[b[1]] != R.TINY_NONE:
            idx = tiny[b[1]]
        elif R.BANK0_B2 <= b[1] < R.BANK0_B2 + R.BANK_COUNT:
            idx = b[2] + ((b[1] - R.BANK0_B2) << 8)
        else:
            idx = None
        if idx is not None:
            tbl = lo + (R.REGION_BASE - R.OV28_RAM)
            a = tbl + int.from_bytes(rom[tbl + idx * 4:tbl + idx * 4 + 4], "little")
            j = a
            while j < a + 400 and not (rom[j] == R.ESC_B1 and rom[j + 1] == R.RET_B2):
                j += 1
            return decode(rom, a, j, inv), "redirect"
    return decode(rom, lo + off, lo + off + budget, inv), "inline"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rom")
    ap.add_argument("--show", type=int, default=30)
    a = ap.parse_args()
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

    rom = open(a.rom, "rb").read()
    lo = W.fat_lo(rom, OV28_FID)
    inv, runs = _inv_map(), W.load_runs()
    # ⚠ A run can be claimed by EITHER path -- `insert_extra` writes the worklist
    # value inline, the main-scenario pass writes the batch value (usually via the
    # redirect, so it can be longer). Which one wins depends on the build order,
    # so accept either: picking one as "the" answer reported 1,919 fake manglings.
    ex, ba = _extra_worklists(), _batches()
    tr = dict(ex)
    tr.update(ba)
    t_off = R.ram2rom(R.TINY_TBL)
    tiny = rom[t_off:t_off + 256]

    n = {"korean": 0, "korean_other": 0, "japanese": 0,
         "untranslated": 0, "mangled": 0}
    bad = []
    for off, budget, jp in runs:
        got, how = read_run(rom, lo, off, budget, inv, tiny)
        g, want = got.strip(), tr.get(jp, "").strip()
        alt = {v.strip() for v in (ex.get(jp), ba.get(jp)) if v}
        if g in alt:
            n["korean"] += 1
        elif g == jp.strip():
            n["japanese" if want else "untranslated"] += 1
        elif not want and g and all(
                ("가" <= c <= "힣") or c in " 。、！？（）「」～・.…?!0123456789"
                for c in g):
            # Korean in the ROM that our batch map does not know: it was written
            # through another path (survey worklists, the intro inserter, the
            # choice pass). Not a defect -- only OUR ignorance of its source.
            n["korean_other"] = n.get("korean_other", 0) + 1
        else:
            n["mangled"] += 1
            bad.append((off, budget, jp, want, got, how))

    tot = len(runs)
    print(f"scan {os.path.basename(a.rom)}: {tot:,} runs")
    print(f"  {n['korean']:,} Korean as intended")
    print(f"  {n['korean_other']:,} Korean from another insertion path")
    print(f"  {n['japanese']:,} left Japanese although translated "
          f"(over budget / no region slot)")
    print(f"  {n['untranslated']:,} never translated")
    print(f"  {n['mangled']:,} MANGLED -- neither the Korean nor the Japanese\n")
    for off, budget, jp, want, got, how in bad[:a.show]:
        print(f"  0x{off:06X} [{budget}] {how}")
        print(f"      jp   {jp}")
        print(f"      want {want or '(no translation)'}")
        print(f"      got  {got!r}")
    if len(bad) > a.show:
        print(f"  ... and {len(bad) - a.show} more")
    return 1 if n["mangled"] else 0


if __name__ == "__main__":
    sys.exit(main())
