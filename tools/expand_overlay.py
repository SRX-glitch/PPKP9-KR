#!/usr/bin/env python3
"""Grow a non-scenario overlay and repoint its string pointers into the new tail.

Why this exists
---------------
The FF-terminated tables (ability names, the encyclopedia, ability effects) can
only take Korean that fits the original record, and shortening has run out of
room. But those records are reached through a **pointer array of absolute RAM
addresses** -- for the ability names, 307 entries at ROM 0x229644 (RAM
0x02106C64), 59 of which point at name strings. Rewrite a pointer and the string
can live anywhere and be any length.

Where the new strings go: the overlay's OWN tail. Overlays that share a RAM base
are mutually exclusive, so growing one inside the group's largest size costs no
RAM at all:

    RAM 0x020CA020 group  largest 658,592 B
      ov8  (FAT[18], ability names)  265,984 B  -> 392,608 B spare
      ov9  (FAT[20], action menu)    526,912 B  -> 131,680 B spare
    RAM 0x0216C3C0 group  largest 177,568 B
      ov14 (FAT[30], encyclopedia)   126,752 B  ->  50,816 B spare

Against the ~7.7 KB the untruncated Korean needs, that is enormous headroom.

Chosen over the alternative of appending to overlay 28's redirect region: that
region IS resident on these screens (measured -- RAM 0x02257B00 matched the ROM
byte for byte while the ability screen was up), so pointing at it would work,
but every byte there also grows overlay 28 and takes it off the scenario arena,
which is already near its stress-verified limit. Growing the overlay's own tail
inside the group maximum costs nothing and does not depend on overlay 28 being
loaded.

What this does NOT touch: the heap-base literal. `expand_rom` moves it because
the scenario heap starts exactly where overlay 28 ends; these overlays are not
followed by the heap, and staying under the group maximum means nothing after
them moves.
"""
import os, sys

sys.path.insert(0, os.path.dirname(__file__))


def u32(b, o):
    return int.from_bytes(b[o:o + 4], "little")


def w32(b, o, v):
    b[o:o + 4] = v.to_bytes(4, "little")


# RAM base -> the largest overlay that loads there. Growing past this would
# start overwriting whatever follows the group, so it is a hard ceiling.
# The 0x021C0DC0 group's largest member is overlay 28 (601,664 B), and build_kr
# already grows THAT one for the redirect region while pushing the scenario heap
# up to match. Capping the group's other overlays at overlay 28's ORIGINAL size
# keeps them under the heap wherever it now sits -- growing one of them past
# that would need the same heap-base move overlay 28 gets, which is not worth it
# for the few KB of strings involved.
# ⚠ These are `ram_size + bss_size` -- the overlay's REAL RAM footprint. They used
# to be ram_size alone, which under-counted every ceiling by that group's largest
# bss and, worse, hid the bug fixed in `expand()` below.
GROUP_MAX = {0x020CA020: 664480, 0x0216C3C0: 184064,
             0x021992C0: 162560, 0x021C0DC0: 601664}


def overlay_of_file(rom, file_id):
    ov, nov = u32(rom, 0x50), u32(rom, 0x54) // 32
    for i in range(nov):
        e = ov + i * 32
        if u32(rom, e + 24) == file_id:
            return e, u32(rom, e), u32(rom, e + 4), u32(rom, e + 8)
    return None


def expand(rom_in, file_id, blob):
    """Append `blob` to file_id's overlay; returns (rom, ram_base_of_blob).

    The overlay is relocated to the ROM tail so no other file's offsets move --
    the same trick expand_rom uses for overlay 28.
    """
    rom = bytearray(rom_in)
    fat = u32(rom, 0x48)
    ent = fat + file_id * 8
    fs, fe = u32(rom, ent), u32(rom, ent + 4)
    info = overlay_of_file(rom, file_id)
    if info is None:
        raise SystemExit(f"FAT[{file_id}] has no overlay-table entry")
    ov_ent, oid, ram, size = info
    bss = u32(rom, ov_ent + 12)
    if fe - fs != size:
        raise SystemExit(f"FAT[{file_id}] size {fe-fs:#x} != overlay size {size:#x}")

    grow = len(blob)
    ceiling = GROUP_MAX.get(ram)
    if ceiling is None:
        raise SystemExit(f"overlay {oid} loads at {ram:#x}, which has no recorded "
                         f"group maximum -- measure it before growing")
    if size + bss + grow > ceiling:
        raise SystemExit(f"overlay {oid} would grow to {size+bss+grow:,}B "
                         f"(data+bss+blob), past its group maximum {ceiling:,}B "
                         f"-- that would overwrite whatever follows in RAM")

    # ⛔⛔⛔ SESSION 36 -- THE MATCH CRASH.
    # The NDS overlay loader copies `ram_size` bytes to `ram_address` and then
    # ZEROES `bss_size` bytes at `ram_address + ram_size`. So the overlay's .bss
    # begins exactly at the old data end -- which is precisely where this function
    # used to drop the Korean blob, while leaving `bss_size` alone. Two faults at
    # once, on every build ever shipped:
    #   1. the blob lands ON TOP of the overlay's .bss variables, and
    #   2. the zero-fill moves UP by `grow`, so it wipes `bss` bytes of whatever
    #      lives above the overlay instead of the variables it was meant to clear.
    # Measured on v100: fid13 buried 1,746 B of a 9,728 B bss, fid18 505 of 7,776,
    # and fid30/fid4 overran their bss ENTIRELY and ran 35,163 / 1,671 bytes past
    # its end. The scenario survived it; the match did not.
    # The fix: put the blob ABOVE the bss and let the file's own zeros initialise
    # the bss. `ram_size` becomes data+bss+blob and `bss_size` becomes 0, so the
    # loader still writes zeros over every .bss byte on every load -- it just does
    # it by copying instead of by memset. RAM footprint grows by `grow` and not a
    # byte more, and every .bss address the overlay's code was linked against
    # keeps its meaning.
    used_end = max(u32(rom, fat + k * 8 + 4) for k in range(u32(rom, 0x4C) // 8))
    newstart = (used_end + 0x1FF) & ~0x1FF
    newdata = bytes(rom[fs:fe]) + b"\x00" * bss + blob
    newend = newstart + len(newdata)
    if newend > len(rom):
        rom += b"\xFF" * (newend - len(rom))
    rom[newstart:newend] = newdata
    w32(rom, ent, newstart)
    w32(rom, ent + 4, newend)
    w32(rom, ov_ent + 8, size + bss + grow)
    w32(rom, ov_ent + 12, 0)
    blob_ram = ram + size + bss
    print(f"  overlay {oid} (FAT[{file_id}]): {size:,} -> {size+bss+grow:,}B "
          f"(data {size:,} + bss {bss:,} + blob {grow:,}; group max {ceiling:,}), "
          f"relocated to {newstart:#x}-{newend:#x}, blob at RAM {blob_ram:#010x} "
          f"(ABOVE the bss)")
    return rom, blob_ram, newstart


def expand_to(rom_in, file_id, ram_target, blob, heap_base):
    """Pad an overlay out to `ram_target` and append `blob` there.

    ⭐⭐ SESSION 38, step ③. Files 4 and 27 hold 6,369 translated lines that do
    not fit inline, and they have no redirect region -- the region lives in
    overlay 28's tail and those overlays are mutually exclusive with it.

    The way out is that overlays 28, 29 (file 4) and 30 (file 27) all load at the
    SAME RAM base 0x021C0DC0 (measured from the overlay table). So each of them
    can carry its OWN region at ONE shared RAM address: pad the file out to that
    address, then append. The escape hook only ever knows `REGION_BASE`, so it
    needs no change at all, and neither does the return-offset arithmetic --
    those offsets are already relative to that same shared base.

    ⭐ The RAM high-water mark does not move: overlay 28 is still the largest of
    the three and the heap literal was already bumped past it by `expand_rom`.
    That is why this is affordable at all, and why `heap_base` is a required
    argument rather than a constant -- pass the ALREADY-BUMPED value so the
    assertion below is checked against reality.

    ⚠ `GROUP_MAX` is deliberately not consulted. That ceiling is overlay 28's
    retail size, and this whole operation is about overlays that must exceed it,
    exactly as overlay 28 itself already does. The heap is the real ceiling.
    """
    rom = bytearray(rom_in)
    fat = u32(rom, 0x48)
    ent = fat + file_id * 8
    fs, fe = u32(rom, ent), u32(rom, ent + 4)
    info = overlay_of_file(rom, file_id)
    if info is None:
        raise SystemExit(f"FAT[{file_id}] has no overlay-table entry")
    ov_ent, oid, ram, size = info
    bss = u32(rom, ov_ent + 12)
    if fe - fs != size:
        raise SystemExit(f"FAT[{file_id}] size {fe-fs:#x} != overlay size {size:#x}")
    # Same bss rule as `expand`: the blob goes ABOVE the bss and bss_size becomes
    # 0, so the loader still zeroes every .bss byte -- by copying, not memset.
    pad = ram_target - (ram + size + bss)
    if pad < 0:
        raise SystemExit(f"overlay {oid} already reaches {ram+size+bss:#x}, past "
                         f"the shared region base {ram_target:#x}")
    end_ram = ram_target + len(blob)
    if end_ram > heap_base:
        raise SystemExit(f"overlay {oid} would end at {end_ram:#x}, past the "
                         f"heap base {heap_base:#x} -- the region does not fit")
    used_end = max(u32(rom, fat + k * 8 + 4) for k in range(u32(rom, 0x4C) // 8))
    newstart = (used_end + 0x1FF) & ~0x1FF
    newdata = bytes(rom[fs:fe]) + b"\x00" * (bss + pad) + blob
    newend = newstart + len(newdata)
    if newend > len(rom):
        rom += b"\xFF" * (newend - len(rom))
    rom[newstart:newend] = newdata
    w32(rom, ent, newstart)
    w32(rom, ent + 4, newend)
    w32(rom, ov_ent + 8, len(newdata))
    w32(rom, ov_ent + 12, 0)
    print(f"  overlay {oid} (FAT[{file_id}]): {size:,} -> {len(newdata):,}B "
          f"(data {size:,} + bss {bss:,} + pad {pad:,} + region {len(blob):,}); "
          f"region at RAM {ram_target:#010x}, ends {end_ram:#010x} "
          f"(heap {heap_base:#010x})")
    return rom, newstart, newend


def declared_end(rom):
    fat = u32(rom, 0x48)
    return max(u32(rom, fat + k * 8 + 4) for k in range(u32(rom, 0x4C) // 8))


if __name__ == "__main__":
    rom = open(r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/"
               r"Power Pro Kun Pocket 9 (Japan).nds", "rb").read()
    for fid in (18, 20, 30):
        e, oid, ram, size = overlay_of_file(rom, fid)
        cap = GROUP_MAX.get(ram)
        print(f"FAT[{fid}] -> overlay {oid}  RAM {ram:#010x}  size {size:,}B  "
              f"group max {cap:,}B  spare {cap - size:,}B")
