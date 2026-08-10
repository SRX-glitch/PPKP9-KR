#!/usr/bin/env python3
"""Gate: every side-region escape resolves the way the ENGINE will read it.

⛔ The build's `region verify` / `escape verify` only walk overlay 28. A side
region (files 4 / 27, session 38 step ③) is invisible to them, so shipping one on
their green light would repeat session 35 exactly: a region that verified fine
against the writer's own idea of the format and derailed the engine on hardware.

This starts from the BUILT ROM and mimics the hook's dispatch order:

    F7 <RET_B2>            -> return marker, not an escape
    F7 <ESC_B2> lo hi      -> long form,   index = lo | hi<<8
    F7 <b2> where TINY_TBL[b2] != 0xFF     -> TINY, and a side region must NEVER
                                              produce one (the table is global)
    F7 <BANK0_B2+k> idx    -> banked,      index = idx | k<<8

then resolves the index in that file's own region -- read out of the BUILT ROM at
the file's live FAT offset, not out of anything the build kept in memory -- and
checks the entry ends in a RET marker whose return address is the byte just past
the run the escape sits in.

    python tools/verify_side.py <built.nds> 27 [4]
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import redirect_hook as R
import expand_overlay as XO
import side_region as SR
import koenc, json


def _font_encoder():
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "survey", "font")
    fm = {k: int(v) for k, v in
          json.load(open(os.path.join(d, "kr_font_map.json"), encoding="utf-8")).items()}
    return koenc.Encoder({"syl": fm, "one": {}, "raw": {" ": "00"}})


def check(path, fid, verbose=True):
    built = open(path, "rb").read()
    fat = int.from_bytes(built[0x48:0x4C], "little")
    lo = int.from_bytes(built[fat + fid * 8:fat + fid * 8 + 4], "little")
    hi = int.from_bytes(built[fat + fid * 8 + 4:fat + fid * 8 + 8], "little")
    ov_ram = XO.overlay_of_file(built, fid)[2]
    # the region starts EXT_PAGE_BYTES past the shared base, in file space
    reg_file = lo + (R.REGION_BASE - ov_ram)
    tiny_rom = R.ram2rom(R.TINY_TBL)
    tiny = built[tiny_rom:tiny_rom + 256]

    man_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                            "survey", f"side_manifest_{fid}.json")
    if not os.path.exists(man_path):
        if verbose:
            print(f"  (no side manifest for file {fid}: nothing to verify)")
        return 0, 0
    man = json.load(open(man_path))

    ok = bad = 0
    problems = []
    for rec in man:
        i = lo + rec["rel"]
        budget = rec["budget"]
        if built[i] != R.ESC_B1:
            problems.append(f"+0x{rec['rel']:06X} is not an escape (byte {built[i]:02X})")
            bad += 1
            continue
        b2 = built[i + 1]
        # The engine's own order: RET, long, TINY, banked. A side region must
        # never land on the tiny branch -- that table is global.
        if b2 == R.RET_B2:
            problems.append(f"+0x{rec['rel']:06X} decodes as a RET marker")
            bad += 1
            continue
        if b2 == R.ESC_B2:
            # ⭐ SESSION 39: the long form is 5 bytes and its payload IS the
            # entry's region offset (base-248), so there is no table slot to
            # read. Resolving it as an index is what made this gate report
            # 456/5385 on a build whose escapes were fine.
            if R.OFFSET_ESC:
                idx = None
                # payload is RET_BASE-relative; make it region-relative
                off = R.un248(built[i + 2:i + 5]) + R.RET_BASE - R.REGION_BASE
            else:
                idx = built[i + 2] | (built[i + 3] << 8)
        elif tiny[b2] != R.TINY_NONE:
            problems.append(f"+0x{rec['rel']:06X} b2={b2:02X} hits the GLOBAL tiny "
                            f"table -- would resolve against overlay 28's indices")
            bad += 1
            continue
        elif 0 <= b2 - R.BANK0_B2 < R.BANK_COUNT:
            idx = built[i + 2] | ((b2 - R.BANK0_B2) << 8)
        else:
            problems.append(f"+0x{rec['rel']:06X} b2={b2:02X} matches no escape form")
            bad += 1
            continue
        if idx is not None:
            slot = reg_file + idx * 4
            if not (reg_file <= slot < hi - 4):
                problems.append(f"+0x{rec['rel']:06X} index {idx} points outside the region")
                bad += 1
                continue
            off = int.from_bytes(built[slot:slot + 4], "little")
        ent = reg_file + off
        if not (reg_file <= ent < hi):
            problems.append(f"+0x{rec['rel']:06X} entry offset {off:#x} leaves the region")
            bad += 1
            continue
        j, guard = ent, 0
        while j < hi - 1 and guard < 512:
            if built[j] == R.ESC_B1 and built[j + 1] == R.RET_B2:
                break
            j += 2 if built[j] >= 0xE8 else 1
            guard += 1
        if j >= hi - 1 or guard >= 512:
            problems.append(f"+0x{rec['rel']:06X} entry at {ent:#x} has no RET marker")
            bad += 1
            continue
        ret = (built[j + 2] | (built[j + 3] << 8) | (built[j + 4] << 16)) + R.RET_BASE
        want = ov_ram + (i - lo) + budget
        if ret != want:
            problems.append(f"+0x{rec['rel']:06X} returns to {ret:#010x}, "
                            f"run ends {want:#010x}")
            bad += 1
        else:
            ok += 1
    if verbose:
        name = os.path.basename(path)
        print(f"{name}: side region file {fid}: {ok}/{ok + bad} escapes resolve "
              f"and return correctly")
        for p in problems[:8]:
            print(f"  side verify MISS {p}")
    return ok, bad


if __name__ == "__main__":
    p = sys.argv[1]
    tot_bad = 0
    for f in (sys.argv[2:] or ["27"]):
        _o, b = check(p, int(f))
        tot_bad += b
    sys.exit(1 if tot_bad else 0)
