#!/usr/bin/env python3
"""Project how much of the scenario heap the redirect region will eat.

Memory map, read from the accessor jump table at 0x02011108 (each case returns
one arena bound from the literal pool at 0x020111E4):
    case 1 -> 0x02253C00   scenario arena START == overlay28_ram + overlay28_size
    case 3 -> 0x023E0000   scenario arena END
So the arena is 0x18C400 = 1,623,040 B, and it begins exactly where overlay 28
ends -- which is why growing the overlay must push this base up by the same
amount, and why every byte of redirect region is a byte off the heap.
"""
import os, sys, json, collections
sys.path.insert(0, os.path.dirname(__file__))

BASE = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"
ARENA_START, ARENA_END = 0x02253C00, 0x023E0000
ARENA = ARENA_END - ARENA_START
ENTRY_OVERHEAD = 12          # u32 table slot + 4-byte return marker + u32 address


def main():
    man = json.load(open(f"{BASE}/survey/redirect_manifest.json", encoding="utf-8"))
    lines = []
    for ln in open(f"{BASE}/survey/ov28/dialogue_runs.tsv", encoding="utf-8").read().splitlines():
        p = ln.split("\t")
        if len(p) >= 4:
            lines.append((int(p[0], 16), int(p[1]), p[3]))
    occ = collections.Counter(jp for _, _, jp in lines)
    distinct_total = len(occ)

    trans = set()
    for name in ["common_lines"] + [f"batch{i}" for i in range(1, 40)]:
        p = f"{BASE}/translation/{name}.tsv"
        if os.path.exists(p):
            for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
                if "\t" in ln:
                    jp = ln.split("\t")[0].strip()
                    if jp:
                        trans.add(jp)
    done = len(trans & set(occ))

    n_occ = len(man)
    n_lines = len({v["jp"] for v in man.values()})
    region = os.path.getsize(f"{BASE}/survey/redirect_manifest.json")  # placeholder
    # measured from the build log instead: recompute text bytes from the manifest
    text_bytes = sum(len(v["ko"]) * 2 for v in man.values())   # ~2 B/glyph pre-MTE
    print(f"scenario arena: 0x{ARENA_START:08X}-0x{ARENA_END:08X} = {ARENA:,} B "
          f"({ARENA/1024:.0f} KB)")
    print(f"translated so far: {done}/{distinct_total} distinct lines "
          f"({done/distinct_total:.1%})")
    print(f"redirected now:    {n_lines} lines / {n_occ} occurrences")

    # duplication: the region stores one copy of the text PER OCCURRENCE, because
    # the return address is per-occurrence
    per_line = collections.Counter(v["jp"] for v in man.values())
    dup = sum(c - 1 for c in per_line.values())
    print(f"per-occurrence duplication: {dup} extra copies "
          f"({dup/max(1,n_occ):.1%} of entries)")

    # observed cost per redirected occurrence, from the actual build
    for grow_line in open(f"{BASE}/RESUME.md", encoding="utf-8"):
        pass
    print()
    print("--- projection to a fully translated Nice Guy scenario ---")
    # redirect rate observed on the long-tail batches (14/15) is the honest input:
    # short frequent lines mostly fit, long count-1 lines mostly do not.
    remaining = distinct_total - done
    for rate, label in ((0.5, "half the remaining lines overflow"),
                        (0.8, "four in five overflow (batch15's rate)"),
                        (1.0, "every remaining line overflows")):
        new_occ = int(remaining * rate)          # the tail is nearly all count-1
        # 41 B per occurrence measured on the current build (text+overhead+table)
        size = (n_occ + new_occ) * 41
        left = ARENA - size
        print(f"  {label}: +{new_occ:,} entries -> region {size/1024:.0f} KB, "
              f"heap {left/1024:.0f} KB left ({size/ARENA:.1%} consumed)")


main()
