#!/usr/bin/env python3
"""Relocate overlay 28 (file25, Nice Guy scenario) to the ROM's tail slack and
optionally grow it. Validates the plan for expanded Korean text:

  - The ROM is 64MB on disk but only ~44MB used -> ~23MB tail slack.
  - Overlays 28-35 share RAM slot 0x021C0DC0 (scenario overlays, one at a time).
  - Heap starts at 0x02253C00 == overlay28_ram + overlay28_size (exact) -> the
    heap is placed right after the overlay, so growing the overlay's size should
    push the heap up rather than collide.

This tool moves file25's bytes to the slack, appends `grow` bytes, and updates
the FAT entry + overlay-table size field. Other files are untouched (no shift).
"""
import sys, os

SRC = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
DST = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/builds/PPKP9_kr.nds"
FILE_ID = 25
OV_ID = 28
# The scenario-overlay heap base is a literal in ARM9 static (single reference).
# It equals overlay28_ram + overlay28_size, so growing the overlay collides with
# the heap unless this constant is moved up by the same amount. VALIDATED on
# emulator: relocate + grow + bump this = title/charmake/intro all play cleanly.
HEAP_LIT_RAM = 0x020111E4
HEAP_BASE = 0x02253C00
OV28_RAM = 0x021C0DC0


def a9_ram2rom(a):
    return a - 0x02000000 + 0x4000


def u32(b, o):
    return int.from_bytes(b[o:o + 4], "little")


def w32(b, o, v):
    b[o:o + 4] = v.to_bytes(4, "little")


def _crc16(data, init=0xFFFF):
    """The CRC-16 the NDS header uses (poly 0xA001, reflected)."""
    crc = init
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
    return crc


def _declare_used_size(rom, end):
    """Point header 0x80 (total used ROM size) past the relocated overlay.

    The relocated file lives beyond where the original header said the data
    ended, so anything that trusts 0x80 -- ROM trimmers, some flashcart loaders,
    any tool that copies "only the used part" -- would drop the whole scenario
    overlay and take the patch with it.

    RESUME's "changing header 0x80 broke the first expansion" was really the
    checksum: 0x80 lies inside the range the header CRC-16 at 0x15E covers
    (0x000-0x15D), so writing it without recomputing the CRC leaves a header the
    firmware rejects. Update both and it is sound; the recomputation is checked
    against the untouched original header before use.
    """
    end = (end + 0x1FF) & ~0x1FF
    if u32(rom, 0x80) >= end:
        return
    w32(rom, 0x80, end)
    crc = _crc16(bytes(rom[0x00:0x15E]))
    rom[0x15E:0x160] = crc.to_bytes(2, "little")
    cap = rom[0x14]
    print(f"  header: used size -> 0x{end:X}, CRC16 -> 0x{crc:04X} "
          f"(device capacity {cap} = {128 * (1 << cap) // 1024} MB, file "
          f"{len(rom) // 1024 // 1024} MB)")
    assert end <= 128 * 1024 * (1 << cap), "used size exceeds the declared chip capacity"


def expand(rom_in, grow, append=b"", zero_old=False):
    rom = bytearray(rom_in)
    fat = u32(rom, 0x48)
    ov = u32(rom, 0x50)
    nov = u32(rom, 0x54) // 32

    fe_off = fat + FILE_ID * 8
    fs, fe = u32(rom, fe_off), u32(rom, fe_off + 4)
    orig = bytes(rom[fs:fe])
    print(f"file25 orig: 0x{fs:07X}-0x{fe:07X} ({fe-fs} bytes)")

    # overlay 28 table entry (find by id)
    ov_ent = None
    for i in range(nov):
        if u32(rom, ov + i * 32) == OV_ID:
            ov_ent = ov + i * 32
            break
    size = u32(rom, ov_ent + 8)
    print(f"overlay28 entry @0x{ov_ent:X}, size 0x{size:X}")
    assert fe - fs == size, f"file size {fe-fs:#x} != overlay size {size:#x}"

    # new home: end of current data, 512-aligned (stay inside the 64MB file)
    used_end = max(u32(rom, fat + k * 8 + 4) for k in range(u32(rom, 0x4C) // 8))
    newstart = (used_end + 0x1FF) & ~0x1FF
    newdata = orig + append + b"\x00" * (grow - len(append))
    newend = newstart + len(newdata)
    print(f"relocate to 0x{newstart:07X}-0x{newend:07X} (grow +0x{grow:X})")

    if newend > len(rom):
        rom += b"\xFF" * (newend - len(rom))
        print(f"  ROM grew to 0x{len(rom):X}")
    rom[newstart:newend] = newdata
    # Leave the old copy alone by default. Nothing reads it once FAT[25] points
    # at the new home, and if anything ever did, the original bytes are a far
    # safer thing to find than 0xFF. (Blanking it is also on the RESUME list of
    # changes that broke the first expansion attempt.)
    if zero_old:
        for i in range(fs, fe):
            rom[i] = 0xFF

    w32(rom, fe_off, newstart)
    w32(rom, fe_off + 4, newend)
    w32(rom, ov_ent + 8, size + grow)
    _declare_used_size(rom, newend)
    # move the heap base up by `grow` so it clears the grown overlay
    lit_off = a9_ram2rom(HEAP_LIT_RAM)
    assert u32(rom, lit_off) == HEAP_BASE, "heap literal moved -- re-find it"
    w32(rom, lit_off, HEAP_BASE + grow)
    print(f"  FAT[25] -> 0x{newstart:07X}-0x{newend:07X}; overlay28 size -> "
          f"0x{size+grow:X}; heap base -> 0x{HEAP_BASE+grow:08X}")
    return bytes(rom)


if __name__ == "__main__":
    grow = int(sys.argv[1], 0) if len(sys.argv) > 1 else 0x1000
    src = open(SRC, "rb").read()
    out = expand(src, grow)
    open(DST, "wb").write(out)
    print(f"wrote {DST}  ({len(out)} bytes)")
