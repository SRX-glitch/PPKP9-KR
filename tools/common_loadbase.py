#!/usr/bin/env python3
"""Find where the shared dialogue files (4, 8, 20, 27) are loaded in RAM.

Why this is needed
------------------
The redirect region ends every entry with a *return marker* carrying an absolute
u32 RAM address -- where to put the script cursor back. For overlay 28 that is
`OV28_RAM + file_offset`, a constant, because the overlay loads to a fixed
address. The shared dialogue files are separate FAT files, so their RAM address
is not known statically, and without it a redirect escape placed in one of them
has nowhere to return to. That is the single blocker between the 6,519 already
translated shared-file runs and the ROM.

How to measure
--------------
1. Get the game to a scene that is showing shared dialogue, then, on the live
   emulator, search main RAM for one of the ANCHORS below:

       find_pattern(memory_type="main", hex=<anchor hex>, start=0, length=131072)

   `find_pattern` scans 131,072 bytes per call regardless of `length`, so walk
   `start` in 0x20000 steps until it hits.

2. Feed the hit back in:

       python tools/common_loadbase.py --found 4 0x21ab3c0

   It prints the implied load base and writes survey/common/load_bases.json.

3. **Repeat in a different scene.** If the base moves, these files live in a
   heap allocation and the absolute-return design cannot be used at all -- the
   hook would have to save and restore the cursor itself instead of reading a
   baked address. Record whichever answer you get; do not assume stability.

Anchors are runs that occur exactly ONCE in the whole ROM, so a hit is
unambiguous. File 27 has none -- every one of its strings also appears in
FAT[1897], the embedded download-play image -- so it uses a two-hit anchor and
the base has to be confirmed by which hit is inside the loaded region.
"""
import argparse, json, os, sys

sys.path.insert(0, os.path.dirname(__file__))
import extract_common as EC
import untranslated as U

OUT = os.path.join(os.path.dirname(__file__), "..", "survey", "common",
                   "load_bases.json")

# (file id) -> list of (offset within the FAT file, hex bytes, the Japanese)
ANCHORS = {
    4: [(0x015bdd, "0101d12434 4c28edf71f", "ああ、やっぱり生まれ故郷は落ちつくなぁ。"),
        (0x015e91, "ebaef06f1a f1aaf38415", "今日は平和な一日だったな。")],
    20: [(0x07ed26, "f06ff225e8 4b161a152a", "日本一にはなれませんでした。")],
    8: [(0x00ae0c, "029427 1a02bc3e1a02", "いヂらはい…")],
    # 27: see the module docstring -- needs a two-hit anchor, filled in when measured
}


def spans():
    rom = open(EC.ORIG, "rb").read()
    return {i: (s, e) for s, e, i in U.fat_files(rom)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--anchors", action="store_true",
                    help="print the hex to paste into find_pattern")
    ap.add_argument("--found", nargs=2, metavar=("FILE", "RAM_OFFSET"),
                    help="record a hit: file id and the main-memory offset it was found at")
    a = ap.parse_args()

    sp = spans()
    if a.anchors or not a.found:
        for fid, lst in ANCHORS.items():
            s, e = sp[fid]
            print(f"\nFAT[{fid}]  ROM {s:#x}~{e:#x}  ({e - s:,}B)")
            for rel, hx, jp in lst:
                print(f"  파일내 +{rel:#08x}  {jp[:24]}")
                print(f"    hex={hx.replace(' ', '')}")
        print("\n찾은 뒤:  python tools/common_loadbase.py --found <파일id> <0x오프셋>")
        return

    fid = int(a.found[0])
    hit = int(a.found[1], 0)
    if fid not in ANCHORS:
        sys.exit(f"FAT[{fid}] 앵커가 없다")
    # main memory in this adapter is offset-based from 0x02000000
    rel = ANCHORS[fid][0][0]
    base_off = hit - rel
    base_ram = 0x02000000 + base_off
    print(f"FAT[{fid}] 앵커가 main+{hit:#x} 에서 발견")
    print(f"  → 로드 베이스  main+{base_off:#x}   RAM {base_ram:#010x}")
    data = {}
    if os.path.exists(OUT):
        data = json.load(open(OUT, encoding="utf-8"))
    prev = data.get(str(fid))
    if prev and prev["ram"] != base_ram:
        print(f"  ⚠ 이전 측정과 다르다 ({prev['ram']:#010x}). 이 파일들은 힙에 올라가고")
        print(f"    절대 복귀 주소 방식은 쓸 수 없다 — 훅이 커서를 직접 저장/복원해야 한다.")
    data[str(fid)] = {"ram": base_ram, "main_off": base_off, "anchor_rel": rel}
    json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"  기록: {OUT}")
    print("  ⚠ 반드시 다른 장면에서 한 번 더 측정해 값이 같은지 확인할 것.")


if __name__ == "__main__":
    main()
