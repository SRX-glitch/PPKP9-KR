#!/usr/bin/env python3
"""Walk the whole script with the opcode table and see where we lose the thread.

Three times now this project has shipped a wrong opcode WIDTH -- `F8 15` (blank
choice boxes, 106 of 206 blocks), `F8 23` (every file-8 record rejected), and
`F8 01`/`F8 29` (the entire 111-line opening read as one broken run). Each time
the symptom was the same shape: the extractor's idea of where a run starts and
how long it is drifts from the engine's, so Korean gets written over an opcode
operand and the VM jumps somewhere it was never meant to go. That is exactly what
"a completely different conversation appears out of nowhere" looks like.

So: walk the PRISTINE overlay from the first recorded run to the last, stepping
opcodes by the table and charcodes by their own width, and compare the run
boundaries the walk produces against `survey/ov28/dialogue_runs.tsv`.

  * a recorded run the walk never lands on  -> our offset is wrong there
  * a run whose walked length differs       -> our budget is wrong there
  * an opcode the table does not know       -> we are guessing its width

Any of those is a place where writing Korean can move an opcode operand.

    python tools/walk_audit.py            # summary
    python tools/walk_audit.py --show 40  # first 40 divergences
"""
import argparse, io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "..")
RUNS = os.path.join(BASE, "survey", "ov28", "dialogue_runs.tsv")
OPLEN = os.path.join(BASE, "survey", "ov28", "opcode_lengths.json")
ORIG = os.path.join(BASE, "..", "rom", "DS",
                    "Power Pro Kun Pocket 9 (Japan).nds")
OV28_FID = 25


def fat_lo(rom, fid):
    fat = int.from_bytes(rom[0x48:0x4C], "little")
    return int.from_bytes(rom[fat + fid * 8:fat + fid * 8 + 4], "little")


def load_runs():
    out = []
    for ln in open(RUNS, encoding="utf-8").read().splitlines():
        f = ln.split("\t")
        if len(f) >= 4:
            try:
                out.append((int(f[0], 16), int(f[1]), f[3]))
            except ValueError:
                pass
    out.sort()
    return out


def load_ops():
    raw = json.load(open(OPLEN, encoding="utf-8"))
    return ({int(k): int(v) for k, v in raw["f8"].items()},
            {int(k): int(v) for k, v in raw["bare"].items()})


def walk(buf, start, stop, f8, bare):
    """Yield (kind, offset, length). kind is 'op' or 'text'."""
    i = start
    while i < stop:
        b = buf[i]
        if b == 0xF8:
            w = f8.get(buf[i + 1])
            if w is None:
                yield ("unknown", i, 2)
                i += 2
                continue
            yield ("op", i, w)
            i += w
        elif b > 0xF8:
            w = bare.get(b)
            if w is None:
                yield ("unknown", i, 1)
                i += 1
                continue
            yield ("op", i, w)
            i += w
        else:
            j = i
            while j < stop and buf[j] < 0xF8:
                j += 2 if buf[j] >= 232 else 1
            yield ("text", i, j - i)
            i = j


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", type=int, default=25)
    a = ap.parse_args()
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

    rom = open(ORIG, "rb").read()
    lo = fat_lo(rom, OV28_FID)
    runs = load_runs()
    f8, bare = load_ops()
    start, stop = runs[0][0], runs[-1][0] + runs[-1][1]
    buf = rom[lo:lo + stop + 64]

    starts, lens, unknown = set(), {}, {}
    for kind, off, ln in walk(buf, start, stop, f8, bare):
        if kind == "text":
            starts.add(off)
            lens[off] = ln
        elif kind == "unknown":
            k = buf[off + 1] if buf[off] == 0xF8 else buf[off]
            tag = f"F8 {k:02X}" if buf[off] == 0xF8 else f"{k:02X}"
            unknown[tag] = unknown.get(tag, 0) + 1

    missing = [r for r in runs if r[0] not in starts]
    wrong = [(o, b, jp, lens[o]) for o, b, jp in runs
             if o in starts and lens[o] != b]
    print(f"walk audit: {len(runs):,} recorded runs over "
          f"0x{start:X}-0x{stop:X}")
    print(f"  {len(missing):,} the walk never lands on   "
          f"(our offset disagrees with the opcode table)")
    print(f"  {len(wrong):,} landed on but a different length "
          f"(our budget disagrees)")
    print(f"  {sum(unknown.values()):,} bytes the table has no width for: "
          f"{dict(sorted(unknown.items(), key=lambda kv: -kv[1])[:10])}")
    if missing:
        print("\n-- never reached --")
        for o, b, jp in missing[:a.show]:
            print(f"  0x{o:06X} [{b}] {jp}")
    if wrong:
        print("\n-- length disagrees --")
        for o, b, jp, got in wrong[:a.show]:
            print(f"  0x{o:06X} recorded {b}, walked {got}   {jp}")
    return 1 if (missing or wrong or unknown) else 0


if __name__ == "__main__":
    sys.exit(main())
