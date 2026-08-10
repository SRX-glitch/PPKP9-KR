#!/usr/bin/env python3
"""Gate: is the grown overlay small enough that the modes still start?

The failure this catches
------------------------
"모드 진입 자체가 안 된다" -- the match loads to a black screen and the console
stops responding. It has bitten this project three times and every time it was
found the same way: a person played to the screen and it hung.

    session 24  grow-only probes: 0x70000 plays, 0x7B000 plays, 0x8D000 hangs
    session 37  v120 at 0x7D000 -- hangs (the note said "needs a match test",
                and nobody ran one until the user reported it)
    session 39  v145 at 0x83000 -- hang reproduced here; v146 at 0x79000 plays,
                verified to the batter's box

Cause: `expand_rom.expand()` pushes the scenario heap base up by the grow, and
the match allocates from what is left. Past some point it has nowhere to run.
The size is what matters, not the content -- a zero-filled region of the shipping
size fails the same way.

Nothing checked it. `PPKP9_REGION_CAP` moves the grow by tens of KB and the build
printed the new overlay size without any opinion about it, so a build could sail
through every text gate and be unbootable in the one mode most players use.

    SAFE   <= 0x79000   measured on a SHIPPING build (v146), match verified
    UNSAFE >= 0x7D000   measured on a SHIPPING build (v120), match hangs
    the 0x7B000 "safe line" in session 24 was a grow-only probe, not a real build,
    so it is not what this gate trusts.

    python tools/verify_grow.py <built.nds>
"""
import os, sys, argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rom_census as R

OV28_FID = 25
SAFE = 0x79000          # verified playing on a shipping build
FAIL = 0x7D000          # verified hanging on a shipping build


def grow_of(path):
    """(grow, built_size, pristine_size) for overlay 28."""
    new = R.Rom(path)
    old = R.Rom()
    ns, ne = new.span(OV28_FID)
    os_, oe = old.span(OV28_FID)
    return (ne - ns) - (oe - os_), ne - ns, oe - os_


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rom")
    ap.add_argument("--safe", type=lambda x: int(x, 0), default=SAFE)
    a = ap.parse_args()

    grow, built, orig = grow_of(a.rom)
    print(f"{os.path.basename(a.rom)}: overlay 28 {orig:,} -> {built:,} B, "
          f"grow 0x{grow:X}")
    if grow <= a.safe:
        print(f"  ok   grow 0x{grow:X} <= 0x{a.safe:X} (verified playing)")
        return 0
    if grow >= FAIL:
        print(f"  FAIL grow 0x{grow:X} >= 0x{FAIL:X} -- a shipping build at this "
              f"size HANGS entering a match. Lower PPKP9_REGION_CAP.")
        return 1
    print(f"  WARN grow 0x{grow:X} is between the verified-playing 0x{a.safe:X} "
          f"and the verified-hanging 0x{FAIL:X}. Nobody has played this size; "
          f"either lower the cap or play to the batter's box before shipping.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
