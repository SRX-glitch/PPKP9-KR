#!/usr/bin/env python3
"""Pull the shared/system text (menus, prompts, baseball UI) into a worklist.

Overlay 28 (FAT 25) is the Nice Guy script and is what the project translated.
The strings the player sees between scenes -- 「何をしようかな」, 「戻ります」,
「セーブ」, the pennant-race messages -- live in OTHER files and were never in
the corpus. tools/untranslated.py found them; this extracts them.

Decoding uses the ORIGINAL ROM and the ORIGINAL table on purpose. Our Hangul was
allocated over charcodes that used to draw Japanese, so reading these files with
the patched map would hand back Korean syllables that the file never contained.

The same fact raises a question this script also answers (--collide): the font
allocation was scenario-scoped. If a shared file draws a charcode we handed to a
Hangul syllable or to an MTE code, then that menu is ALREADY broken in the
shipped ROM -- rendered as Korean, or expanded as a dictionary entry.

    python tools/extract_common.py --file 27          # worklist for file 27
    python tools/extract_common.py --file 27 --collide
"""
import argparse, json, os, sys, collections

sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P
import untranslated as U

BASE = r"C:/Users/jngji/Desktop/실험실"
ORIG = BASE + r"/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
OUT = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/common"


def orig_runs(rom, lo, hi):
    """(offset, text, [charcodes]) for each `F8 6B` run inside [lo, hi)."""
    i = lo
    while i < hi - 3:
        if rom[i] == 0xF8 and rom[i + 1] == 0x6B:
            start, j, s, ccs = i, i + 3, [], []
            while j < hi and rom[j] != 0 and rom[j] < 0xF8:
                b = rom[j]
                if 1 <= b <= 231:
                    cc = b - 1; j += 1
                else:
                    cc = 256 + (b - 232) * 256 + rom[j + 1]; j += 2
                ccs.append(cc)
                s.append(P.CC2CH.get(cc, "\ufffd"))
            yield start, "".join(s), ccs
            i = j
        else:
            i += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", type=int, default=27)
    ap.add_argument("--collide", action="store_true")
    ap.add_argument("--min-jp", type=int, default=1)
    a = ap.parse_args()

    rom = open(ORIG, "rb").read()
    span = next(((s, e) for s, e, i in U.fat_files(rom) if i == a.file), None)
    if not span:
        sys.exit(f"no FAT entry {a.file}")
    lo, hi = span
    print(f"FAT[{a.file}]  {lo:#x}-{hi:#x}  {hi-lo:,}B")

    items = [(o, t, c) for o, t, c in orig_runs(rom, lo, hi)
             if sum(1 for ch in t if U.is_jp(ch)) >= a.min_jp]
    freq = collections.Counter(t for _, t, _ in items)
    print(f"runs with Japanese: {len(items):,}   distinct: {len(freq):,}")

    if a.collide:
        m = json.load(open(f"{BASE}/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font/kr_map.json", encoding="utf-8"))
        taken = {int(v) for v in m["syl"].values()} | {int(v) for v in m.get("one", {}).values()}
        sys.path.insert(0, os.path.dirname(__file__))
        import mte_hook as M
        codes = {cc for b, c in M.CODE_RANGES for cc in range(b, b + c)}
        used = collections.Counter(cc for _, _, ccs in items for cc in ccs)
        hit_syl = {cc: n for cc, n in used.items() if cc in taken}
        hit_mte = {cc: n for cc, n in used.items() if cc in codes}
        print(f"\ndistinct charcodes this file draws: {len(used):,}")
        print(f"  reassigned to a Hangul syllable: {len(hit_syl)}  "
              f"({sum(hit_syl.values()):,} draws)")
        print(f"  inside an MTE code range:        {len(hit_mte)}  "
              f"({sum(hit_mte.values()):,} draws)")
        for cc, n in sorted(hit_syl.items(), key=lambda kv: -kv[1])[:12]:
            print(f"    syl  {cc:#06x} {P.CC2CH.get(cc,'?')!r} x{n}")
        for cc, n in sorted(hit_mte.items(), key=lambda kv: -kv[1])[:12]:
            print(f"    mte  {cc:#06x} {P.CC2CH.get(cc,'?')!r} x{n}")
        return

    os.makedirs(OUT, exist_ok=True)
    path = f"{OUT}/file{a.file}_runs.tsv"
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("n\toccurrences\tjp\tko\n")
        for i, (t, n) in enumerate(freq.most_common(), 1):
            f.write(f"{i}\t{n}\t{t}\t\n")
    print(f"wrote {path}")
    for t, n in freq.most_common(20):
        print(f"  x{n:<4} {t[:56]}")


if __name__ == "__main__":
    main()
