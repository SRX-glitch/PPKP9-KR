#!/usr/bin/env python3
"""Prove that every byte we changed is a TEXT byte -- in every file, not just one.

The user's standing requirement after session 35: the dialogue must never take a
wrong branch again. Wrong branches come from exactly one thing -- a byte that is
not text getting overwritten. The script's flag and jump opcodes sit inches from
the text (`F8 5D`, `F8 30`, `F8 2D`, `F8 2E`, `F8 2F` all appear between two runs
of one message), so a run whose recorded length is one byte long, or an inserter
that pads past its budget, silently rewrites control flow.

`build_kr`'s opcode gate already proves this for overlay 28. **Nothing proved it
for files 4, 8, 18, 27 or 30**, which `insert_extra`, `insert_file8` and
`insert_tables` all write. This closes that hole: for each file we touch, every
differing byte must fall into one of

    run       inside a run the extractor recorded (that is what we meant to write)
    pointer   an aligned u32 whose ORIGINAL value pointed into the overlay
              (insert_file8 / insert_profiles rewrite those on purpose)
    padding   inside a >=12-byte 0x00/0xFF stretch in the PRISTINE file
              (insert_file8.apply_relocate parks records there)

and anything else is reported as a structural write -- the class that corrupts a
flag and sends the conversation somewhere else.

    python tools/verify_writes.py rom/DS/PPKP9_kr_v88.nds
"""
import argparse, io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import expand_overlay as X
import check_opcodes as CO

BASE = os.path.join(HERE, "..")
# ⛔ was BASE/../rom/DS/... -- one directory level too deep, so the whole gate
# was silently "skipped: Errno 2" on every build since the folder reshuffle.
ORIG = os.path.join(BASE, "..", "Power Pro Kun Pocket 9 (Japan).nds")
COMMON = os.path.join(BASE, "survey", "common")
OV28_RUNS = os.path.join(BASE, "survey", "ov28", "dialogue_runs.tsv")
FILES = (4, 8, 18, 20, 25, 27, 30)


def _fat(rom, fid):
    f = X.u32(rom, 0x48)
    return X.u32(rom, f + fid * 8), X.u32(rom, f + fid * 8 + 4)


def recorded_runs(fid, lo):
    """{absolute pristine offset} of every byte the extractor called text."""
    out = set()
    p = os.path.join(COMMON, f"file{fid}_extra.tsv")
    if os.path.exists(p):
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            f = ln.split("\t")
            if len(f) >= 2:
                try:
                    o, b = int(f[0], 16), int(f[1])
                except ValueError:
                    continue
                out.update(range(o, o + b))
    if fid == 25:                       # the main scenario is recorded separately
        for ln in open(OV28_RUNS, encoding="utf-8").read().splitlines():
            f = ln.split("\t")
            if len(f) >= 2:
                try:
                    o, b = int(f[0], 16), int(f[1])
                except ValueError:
                    continue
                out.update(range(lo + o, lo + o + b))
    return out


def table_slots(fid):
    """{offset: slot length} for the fixed-width tables insert_tables writes.

    ⚠ These entries are `text FF pad` in a fixed slot (file 18 = 8 B, file 30 =
    48 B). Korean is longer than katakana, so the FF terminator legitimately
    MOVES inside its own slot -- and the opcode walk, which counts that FF as an
    opcode byte, then reports it as control-flow corruption. Measured on v88: all
    20 "structural" hits were this and nothing else (file18 67/67 and file30
    137/137 still terminate inside their slot). A gate that cries wolf gets
    ignored, so teach it the shape instead of lowering the bar.
    """
    p = os.path.join(COMMON, f"file{fid}_table.tsv")
    if not os.path.exists(p):
        return {}
    offs = []
    for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
        f = ln.split("	")
        if len(f) >= 6 and f[5].strip():
            try:
                offs.append(int(f[1], 16))
            except ValueError:
                pass
    offs.sort()
    return {o: (offs[i + 1] - o if i + 1 < len(offs) else 48)
            for i, o in enumerate(offs)}


def padding(pris, lo, hi, minlen=12):
    out, n = set(), 0
    for i in range(lo, hi):
        if pris[i] in (0x00, 0xFF):
            n += 1
        else:
            if n >= minlen:
                out.update(range(i - n, i))
            n = 0
    if n >= minlen:
        out.update(range(hi - n, hi))
    return out


def check(rom_path, show=10):
    import json
    pris = open(ORIG, "rb").read()
    new = open(rom_path, "rb").read()
    _L = json.load(open(os.path.join(BASE, "survey", "ov28",
                                     "opcode_lengths.json"), encoding="utf-8"))
    BARE = {int(k): v for k, v in _L["bare"].items()}
    F8 = {int(k): v for k, v in _L["f8"].items()}
    bad_total = 0
    print(f"verify writes: {os.path.basename(rom_path)}")
    print("  (structural = a byte the opcode walk says belongs to an OPCODE, "
          "i.e. control flow, changed)")
    for fid in FILES:
        lo_o, hi_o = _fat(pris, fid)
        lo_n, _ = _fat(new, fid)
        try:
            _, _, ram, size = X.overlay_of_file(pris, fid)
        except Exception:
            ram = size = 0
        # ⭐ Independent of our own write lists: walk the PRISTINE file with the
        # opcode table and mark every byte that belongs to an opcode. "We wrote
        # it, so it is fine" is circular; "the walk says this byte is an operand
        # and it changed" is not.
        owned = CO.opcode_bytes(pris, lo_o, hi_o, BARE, F8)
        runs = recorded_runs(fid, lo_o)
        pad = padding(pris, lo_o, hi_o)
        slots = table_slots(fid)
        in_slot = set()
        for o, n in slots.items():
            seg = bytes(new[lo_n + o - lo_o: lo_n + o - lo_o + n])
            t = seg.find(0xFF)
            if 0 <= t < n:                 # still terminates inside its own slot
                in_slot.update(range(o, o + n))
        diff = [i for i in range(hi_o - lo_o)
                if pris[lo_o + i] != new[lo_n + i]]
        kinds = {"run": 0, "pointer": 0, "padding": 0, "slot": 0,
                 "STRUCTURAL": 0}
        bad = []
        for i in diff:
            a = lo_o + i
            if not owned[i]:
                kinds["run"] += 1              # the walk says this is text
            elif a in in_slot:
                kinds["slot"] += 1
            elif a in pad:
                kinds["padding"] += 1
            elif ram and ram <= X.u32(pris, (a & ~3)) < ram + size:
                kinds["pointer"] += 1
            else:
                kinds["STRUCTURAL"] += 1
                bad.append(a)
        bad_total += kinds["STRUCTURAL"]
        flag = "  " if not kinds["STRUCTURAL"] else "⛔"
        print(f" {flag} file{fid:<3} {len(diff):7,} bytes changed  "
              f"text {kinds['run']:,} / pointer {kinds['pointer']:,} / "
              f"padding {kinds['padding']:,} / slot {kinds['slot']:,} / "
              f"**STRUCTURAL {kinds['STRUCTURAL']:,}**")
        for a in bad[:show]:
            print(f"        0x{a:06X}  {pris[a-4:a+6].hex(' ')}  ->  "
                  f"{new[lo_n + a - lo_o - 4:lo_n + a - lo_o + 6].hex(' ')}")
    print(f"\n{bad_total} structural byte(s) changed across {len(FILES)} files")
    return bad_total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rom")
    ap.add_argument("--show", type=int, default=6)
    a = ap.parse_args()
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.exit(1 if check(a.rom, a.show) else 0)


if __name__ == "__main__":
    main()
