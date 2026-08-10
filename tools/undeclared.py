#!/usr/bin/env python3
"""Which bytes did the build change that nobody declared?  ⚠ UNFINISHED ⚠

STATUS (session 27): the idea is right, the ownership model is not. It still
reports ~281,000 "undeclared" bytes on a known-good deploy ROM, and spot checks
say those are ours: the changed bytes around ROM 0x6c000-0x6d100 decode as
charcode halfwords, i.e. the MTE dictionary storage, which session 24 placed in
"globally unused glyph RAM". alloc_plan's `dict_regions` (12 entries) clearly
does not cover all of it, and `dict_capacity` is 222.

**Do not quote its number as a finding until it reports ~0 on a good ROM.**
To finish: get the authoritative list of every byte build_kr writes -- easiest is
to have build_kr itself record each write (address, length, purpose) into a
manifest as it goes, and audit against that instead of reverse-engineering
ownership from alloc_plan. That is how PP7 does it (expected-writes.json), and
it is the only version of this that cannot drift.

PP7's build (see rom/분석보고서/) refuses to ship if a single byte changed that
was not on its expected-writes list. PPKP9 has three verifies -- text, region,
glyph -- but every one of them checks that what we *meant* to write is there.
None of them asks the opposite question: did we write something we did not mean
to? Session 27 spent a day on a regression whose byte-level cause is still
unknown, so that is the gap this closes.

    python tools/undeclared.py                        # audit the deploy ROM
    python tools/undeclared.py --rom ...PPKP9_test.nds

Declared regions (anything outside them is reported):
  * the whole relocated overlay 28 -- script, extension pages, redirect region
  * the ARM9 window holding the hooks, stub, tables and MTE dictionary
  * FAT entry 25, and the header's used-size + CRC16 fields
  * font blocks: glyph bytes for the charcodes we own
"""
import argparse, json, os, sys

sys.path.insert(0, os.path.dirname(__file__))
import fontcodec as F

BASE = r"C:/Users/jngji/Desktop/실험실"
ORIG = BASE + r"/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
DEPLOY = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/builds/PPKP9_kr.nds"


def declared_spans(orig, patched):
    """(start, end, label) byte ranges the build is allowed to touch."""
    spans = []
    # NDS header: used-ROM-size word and the CRC16 that covers it.
    spans.append((0x80, 0x84, "header used size"))
    spans.append((0x15E, 0x160, "header CRC16"))
    # FAT entry 25 = overlay 28's file span (8 bytes: start, end).
    fat = int.from_bytes(orig[0x48:0x4C], "little")
    spans.append((fat + 25 * 8, fat + 26 * 8, "FAT[25]"))
    # The relocated overlay itself, wherever expand_rom put it.
    new_start = int.from_bytes(patched[fat + 25 * 8:fat + 25 * 8 + 4], "little")
    new_end = int.from_bytes(patched[fat + 25 * 8 + 4:fat + 25 * 8 + 8], "little")
    spans.append((new_start, new_end, "overlay 28 (relocated)"))
    # The original overlay's old home is left as-is by the build; if it changed,
    # that is worth knowing, so it is NOT declared.
    # ARM9 hook/stub/table/dictionary window (redirect_hook.HOOK_ADDR area).
    try:
        import redirect_hook as R
        lo = F.ram2rom(R.HOOK_ADDR)
        spans.append((lo, lo + 0x500, "ARM9 hooks/stub"))
    except Exception:
        pass
    return spans


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom", default=DEPLOY)
    ap.add_argument("--max-report", type=int, default=25)
    a = ap.parse_args()
    orig = open(ORIG, "rb").read()
    patched = open(a.rom, "rb").read()
    print(f"original {len(orig):,}B   patched {len(patched):,}B")

    spans = declared_spans(orig, patched)
    for s, e, label in spans:
        print(f"  declared {s:#010x}-{e:#010x}  {label}")

    # Everything the allocator hands out. The font map alone is NOT enough --
    # the build also writes MTE dictionary storage, the code/store tables, the
    # stub and the hook into "globally unused glyph RAM", and auditing without
    # them reports a quarter of a megabyte of phantom undeclared writes.
    plan = json.load(open(f"{BASE}/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font/alloc_plan.json", encoding="utf-8"))
    for addr, size in plan.get("dict_regions", []):
        lo = F.ram2rom(addr)
        spans.append((lo, lo + size, "MTE dict region"))
    for key, size in (("hook", plan.get("hook_bytes", 0x500)), ("stub", 0x200),
                      ("code_tbl", 0x200), ("store_tbl", 0x200)):
        if key in plan:
            lo = F.ram2rom(plan[key])
            spans.append((lo, lo + size, key))

    owned = set()
    m = json.load(open(f"{BASE}/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font/kr_font_map.json", encoding="utf-8"))
    tbl = F.load_table(orig)
    # global_slots.json is the authoritative list of charcodes that own glyph
    # storage -- the font map is only the ones that ended up holding a syllable.
    ccs = set(m.values())
    try:
        ccs.update(json.load(open(f"{BASE}/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font/global_slots.json",
                                  encoding="utf-8")))
    except OSError:
        pass
    for lo, n in plan.get("code_ranges", []) + plan.get("ext_ranges", []):
        ccs.update(range(lo, lo + n))
    for cc in ccs:
        blk = (cc & 0x7FFF) // 64
        if blk >= len(tbl):
            continue
        base = F.ram2rom(tbl[blk])
        for row in F.glyph_map(cc):
            for b, _k in row:
                owned.add(base + b)

    def declared(i):
        if i in owned:
            return True
        for s, e, _l in spans:
            if s <= i < e:
                return True
        return False

    runs, cur = [], None
    n = min(len(orig), len(patched))
    for i in range(n):
        if orig[i] != patched[i] and not declared(i):
            if cur and i == cur[1]:
                cur[1] = i + 1
            else:
                cur = [i, i + 1]
                runs.append(cur)
    total = sum(e - s for s, e in runs)
    print(f"\nUNDECLARED byte changes: {total:,} in {len(runs)} run(s)")
    for s, e in runs[:a.max_report]:
        print(f"   {s:#010x}-{e:#010x}  {e-s}B  orig {orig[s:min(e,s+8)].hex()}"
              f" -> {patched[s:min(e,s+8)].hex()}")
    if len(runs) > a.max_report:
        print(f"   ... and {len(runs)-a.max_report} more")
    return 1 if runs else 0


if __name__ == "__main__":
    sys.exit(main())
