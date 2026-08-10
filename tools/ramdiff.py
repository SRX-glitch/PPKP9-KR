#!/usr/bin/env python3
"""Diff two RAM images and report the changed words, grouped into runs.

Used to isolate "what variable holds this UI state" without knowing the code:
capture a savestate, change exactly one thing on screen (move the cursor one
step), capture again, and whatever moved is a very small set.

Usage:
    python3 ramdiff.py a.bin b.bin [--max 80] [--u32]
"""
import sys, struct

BASE = 0x02000000


def main():
    a = open(sys.argv[1], "rb").read()
    b = open(sys.argv[2], "rb").read()
    n = min(len(a), len(b))
    maxrun = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 80

    runs = []
    i = 0
    while i < n:
        if a[i] != b[i]:
            j = i
            while j < n and a[j] != b[j]:
                j += 1
            # merge runs separated by <=3 equal bytes
            if runs and i - runs[-1][1] <= 3:
                runs[-1] = (runs[-1][0], j)
            else:
                runs.append((i, j))
            i = j
        else:
            i += 1

    print(f"{len(runs)} changed run(s), {sum(j-i for i, j in runs)} bytes total")
    for i, j in runs[:maxrun]:
        size = j - i
        av, bv = a[i:j], b[i:j]
        extra = ""
        if size <= 4:
            pa = int.from_bytes(av.ljust(4, b"\0"), "little")
            pb = int.from_bytes(bv.ljust(4, b"\0"), "little")
            extra = f"   {pa} -> {pb}"
        print(f"  0x{BASE+i:08x} +{size:<4} {av.hex()[:32]:34} -> {bv.hex()[:32]:34}{extra}")
    if len(runs) > maxrun:
        print(f"  ... {len(runs)-maxrun} more")


if __name__ == "__main__":
    main()
