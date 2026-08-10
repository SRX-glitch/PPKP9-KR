#!/usr/bin/env python3
"""Nice Guy scenario charcode census, rebuilt on the corrected corpus.

The original scenario_census.py counted charcodes with the same `F8 6B` scanner
that text_budget.py used: it stopped a line at the first byte >= 0xF8 or 0x00 and
resumed only at the next `F8 6B`. Characters that appeared only in the dropped
tails were therefore judged "unused", and the MTE hook handed their glyph storage
to the dictionary -- clobbering 41 characters that really do render.

This version counts from `dialogue_runs.tsv` (the validated opcode walk) and
unions in the old scanner's result for both regions, so the "used" set is a
strict superset of what the previous census produced. Same three output files.
"""
import os, sys, json, collections
sys.path.insert(0, os.path.dirname(__file__))
import fontcodec as F
import poketbl as P

BASE = r"C:/Users/jngji/Desktop/실험실"
ROM = f"{BASE}/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
OUT = f"{BASE}/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font"
RUNS = f"{BASE}/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/ov28/dialogue_runs.tsv"
rom = open(ROM, "rb").read()

SCENARIO_REGIONS = [(0x04CC000, 0x055EE40), (0x00320000, 0x00340000)]


def old_scanner(regions):
    """The previous census, kept only as a safety union."""
    used = collections.Counter()
    for lo, hi in regions:
        i = lo
        while i < hi - 2:
            if rom[i] == 0xF8 and rom[i + 1] == 0x6B:
                j = i + 3
                while j < hi and rom[j] != 0 and rom[j] < 0xF8:
                    b = rom[j]
                    if 1 <= b <= 231:
                        used[b - 1] += 1
                        j += 1
                    elif 232 <= b <= 247:
                        used[256 + (b - 232) * 256 + rom[j + 1]] += 1
                        j += 2
                    else:
                        j += 1
                i = j
                continue
            i += 1
    return used


def main():
    used = old_scanner(SCENARIO_REGIONS)
    before = len(used)

    # the real corpus: every charcode of every walked run in overlay 28
    n_runs = 0
    for ln in open(RUNS, encoding="utf-8").read().splitlines():
        p = ln.split("\t")
        if len(p) < 4:
            continue
        n_runs += 1
        for ch in p[3]:
            cc = P.CH2CC.get(ch)
            if cc is not None:
                used[cc] += 1

    print(f"old scanner alone      : {before} distinct charcodes")
    print(f"+ {n_runs} walked runs  : {len(used)} distinct charcodes "
          f"(+{len(used) - before} newly seen)")

    tbl = F.load_table(rom)
    seen, alias = {}, set()
    for i, p in enumerate(tbl):
        if p in seen:
            alias.add(i)
        else:
            seen[p] = i

    slots = [cc for cc in range(4352)
             if cc not in used and cc // 64 not in alias and cc < 0xC00]
    slots.sort(reverse=True)
    print(f"safe 12px glyph slots (<0xC00): {len(slots)}")

    unused = [cc for cc in range(0x100, 0x1100) if cc not in used]
    runs, s, p = [], None, None
    for cc in unused:
        if s is None:
            s = p = cc
        elif cc == p + 1:
            p = cc
        else:
            runs.append((s, p - s + 1))
            s = p = cc
    if s is not None:
        runs.append((s, p - s + 1))
    runs.sort(key=lambda r: -r[1])
    print("largest unused code runs:", [(hex(a), n) for a, n in runs[:6]])

    free_regions = []
    for base in range(0, 4352, 16):
        if base // 64 in alias:
            continue
        if all(cc not in used for cc in range(base, base + 16)):
            free_regions.append((base, tbl[base // 64] + ((base & 0x30) >> 4) * 576))
    free_regions.sort(key=lambda r: r[1])
    store, cur = [], None
    for base, ram in free_regions:
        if cur and ram == cur[1]:
            cur[1] += 576
        else:
            if cur:
                store.append(cur)
            cur = [ram, ram + 576]
    if cur:
        store.append(cur)
    store.sort(key=lambda r: -(r[1] - r[0]))
    total_store = sum((e - s) // 8 for s, e in store)
    print(f"free glyph-storage RAM runs: {len(store)}, total {total_store} dict slots")
    for s_, e_ in store[:8]:
        print(f"  RAM 0x{s_:08X}-0x{e_:08X}  {(e_-s_)//8} slots")

    json.dump({str(k): v for k, v in used.items()},
              open(os.path.join(OUT, "scenario_usage.json"), "w"))
    json.dump(slots, open(os.path.join(OUT, "scenario_slots.json"), "w"))
    json.dump({"code_runs": runs, "store_runs": store},
              open(os.path.join(OUT, "scenario_free.json"), "w"))
    print("wrote scenario_usage.json, scenario_slots.json, scenario_free.json")


if __name__ == "__main__":
    main()
