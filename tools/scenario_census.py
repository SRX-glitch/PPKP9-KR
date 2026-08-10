#!/usr/bin/env python3
"""Nice Guy scenario census: charcode usage counting ONLY the text the Nice Guy
Success scenario actually renders (file25 / overlay 28, plus the intro cutscene
file). Charcodes used only by OTHER scenarios (file4 space, file27/1897 martial
arts) are free to repurpose -- when playing Nice Guy they never render.

Outputs:
  survey/font/scenario_usage.json   {charcode: count}  (Nice Guy only)
  survey/font/scenario_slots.json   safe 12px glyph slots (<0xC00), rarest-first
  survey/font/scenario_free.json    {code_runs, store_regions} for mte_hook
"""
import os, sys, json, collections
sys.path.insert(0, os.path.dirname(__file__))
import fontcodec as F

ROM = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
OUT = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font"
rom = open(ROM, "rb").read()

# Nice Guy scenario text lives in file25 (overlay 28) + the intro cutscene file.
SCENARIO_REGIONS = [(0x04CC000, 0x055EE40), (0x00320000, 0x00340000)]


def census(regions):
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
    used = census(SCENARIO_REGIONS)
    print(f"Nice Guy scenario: distinct charcodes used = {len(used)}")

    tbl = F.load_table(rom)
    seen = {}
    alias = set()
    for i, p in enumerate(tbl):
        if p in seen:
            alias.add(i)
        else:
            seen[p] = i

    # glyph slots: unused-by-scenario, non-alias block, 12px (<0x1000), and
    # <0xC00 to stay on the stub's fast-reject path (proven-safe rendering).
    slots = [cc for cc in range(4352)
             if cc not in used and cc // 64 not in alias and cc < 0xC00]
    slots.sort(reverse=True)
    print(f"safe 12px glyph slots (<0xC00): {len(slots)}")

    # free MTE-code runs: contiguous charcodes unused by scenario, valid (<0x1100)
    unused = [cc for cc in range(0x100, 0x1100) if cc not in used]
    runs = []
    s = p = None
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

    # free glyph-storage regions (RAM) for the dict: a 16-charcode aligned group
    # whose charcodes are ALL unused-by-scenario and non-alias -> its 576 B is free.
    free_regions = []
    for base in range(0, 4352, 16):
        blk = base // 64
        if blk in alias:
            continue
        if all(cc not in used for cc in range(base, base + 16)):
            ram = tbl[blk] + ((base & 0x30) >> 4) * 576
            free_regions.append((base, ram))
    # merge into contiguous RAM runs
    free_regions.sort(key=lambda r: r[1])
    store = []
    cur = None
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
    for s, e in store[:8]:
        print(f"  RAM 0x{s:08X}-0x{e:08X}  {(e-s)//8} slots")

    json.dump({str(k): v for k, v in used.items()},
              open(os.path.join(OUT, "scenario_usage.json"), "w"))
    json.dump(slots, open(os.path.join(OUT, "scenario_slots.json"), "w"))
    json.dump({"code_runs": runs, "store_runs": store},
              open(os.path.join(OUT, "scenario_free.json"), "w"))
    print("wrote scenario_usage.json, scenario_slots.json, scenario_free.json")


main()
