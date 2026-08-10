#!/usr/bin/env python3
"""Gate: does every redirect come BACK to where it left?

The invariant, and why it needs its own gate
--------------------------------------------
A redirect escape replaces a run in the script. The region entry it points at
ends with a return marker holding the address the engine resumes from. That
address must land just past the run it left -- `site + budget`, a handful of
bytes ahead. If it points anywhere else the engine carries on reading somewhere
it was never supposed to be, and the player gets a different scene spliced into
the middle of the one they were reading. The user has reported exactly that:
"아예 다른 이벤트가 중간에 출몰".

`verify_escapes` already checks this -- but only for the sites in
`survey/redirect_manifest.json`, which the build REWRITES every run. So it can
only ever validate the NEWEST ROM; point it at an older build and it compares
that ROM against a manifest describing a different one.

⚠ And that is not the only build-relative assumption to trip over. This gate
decodes the escape payload, so it is only valid for a ROM built with the CURRENT
`redirect_hook` constants. Session 39 changed the offset base from 248 to 232 and
then ran this gate against ROMs built at base 248: it reported 1,725 of 18,963
escapes "broken" and the shipping candidate was declared dead. Both ROMs were
fine -- decoded with the base each was built with, every one of the 18,963
passes. If a gate reports a catastrophe on an OLD build, suspect the gate first.

This gate needs no manifest. It walks the built ROM, finds the escapes itself,
resolves each through the region, and checks the one property that cannot be
build-relative:

    site + 2  <=  return address  <=  site + MAX_RUN

    python tools/verify_return.py <built.nds>
"""
import os, sys, argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import redirect_hook as R
import rom_census as RC
import verify_escapes as VE

OV28_FID = 25
MAX_RUN = 64            # no dialogue run is anywhere near this long


def check(path, fid=OV28_FID, limit=10, verbose=True):
    rom = RC.Rom(path)
    b = rom.b
    lo, hi = rom.span(fid)
    ov_ram = [o for o in rom.ovl if o["file"] == fid][0]["ram"]
    tbl = lo + (R.REGION_BASE - ov_ram)
    t_off = R.ram2rom(R.TINY_TBL)
    tiny = b[t_off:t_off + 256]

    region_lo = tbl
    ok = bad = 0
    problems = []
    i = lo
    while i < hi - 6:
        j = b.find(bytes([R.ESC_B1]), i, hi - 6)
        if j < 0:
            break
        got = VE.engine_decode(b, tiny, j)
        if got is None:
            i = j + 1
            continue
        form, val, used = got
        if form == "ret" or j >= region_lo:
            i = j + used            # inside the region itself, not a call site
            continue
        # resolve the entry
        if form == "long" and R.OFFSET_ESC:
            # payload = entry address - RET_BASE (main RAM), so it names a region
            # in ANY overlay's tail, not just the one at REGION_BASE.
            ent = lo + (val + R.RET_BASE - ov_ram)
        else:
            slot = tbl + val * 4
            if not (tbl <= slot < hi - 4):
                problems.append((j, form, "index outside the region"))
                bad += 1
                i = j + used
                continue
            ent = tbl + int.from_bytes(b[slot:slot + 4], "little")
        if not (tbl <= ent < hi - 5):
            problems.append((j, form, f"entry 0x{ent:X} outside the region"))
            bad += 1
            i = j + used
            continue
        # walk to the return marker
        k, guard = ent, 0
        while k < hi - 5 and guard < 512:
            if b[k] == R.ESC_B1 and b[k + 1] == R.RET_B2:
                break
            k += 2 if b[k] >= 0xE8 else 1
            guard += 1
        if guard >= 512 or k >= hi - 5:
            problems.append((j, form, "no return marker in the entry"))
            bad += 1
            i = j + used
            continue
        # marker holds `addr - RET_BASE`; this gate works in file-relative
        # offsets, so shift by where the file's overlay sits in main RAM.
        ret = int.from_bytes(b[k + 2:k + 5], "little") - (ov_ram - R.RET_BASE)
        site = j - lo
        delta = ret - site
        if 2 <= delta <= MAX_RUN:
            ok += 1
        else:
            bad += 1
            problems.append((j, form,
                             f"returns to +0x{ret:06X}, site +0x{site:06X}, "
                             f"delta {delta:+d}"))
        i = j + used

    if verbose:
        print(f"return verify: {ok}/{ok + bad} escapes resume within "
              f"[site+2, site+{MAX_RUN}]")
        for j, form, why in problems[:limit]:
            print(f"   +0x{j - lo:06X} {form:5s} {why}")
        if len(problems) > limit:
            print(f"   ... and {len(problems) - limit} more")
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rom")
    ap.add_argument("--fid", type=int, default=OV28_FID)
    a = ap.parse_args()
    sys.exit(1 if check(a.rom, a.fid) else 0)


if __name__ == "__main__":
    main()
