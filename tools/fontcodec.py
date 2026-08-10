#!/usr/bin/env python3
"""PPKP9 font codec — EXACT, derived from ARM9 disassembly (session 7).

render_char @0203CCE8 / render_glyph @0203CECC / codec @0203CFA4.

Glyph = 12 wide x 12 tall, 2bpp (0=transparent, 1=ink-colour "faint", 2=full ink).
36 bytes per glyph, but NOT contiguous: 16 charcodes share a 576-byte region and
their bytes are interleaved (even/odd + a +0xB8/+0xC0 split for the lower rows).

For charcode cc:
    block  = (cc & 0x7FFF) >> 6      -> FONT_TABLE[block] = region base
    within = cc & 0x3F
    P = base + (within & 0x30)*0x24 + (0xC8 if within & 8 else 0)
             + (0x60 if within & 4 else 0) + [0,0x11,0x30,0x41][within & 3]
    column sources: A=P, B=P+(1 if (within&3) in (0,2) else 0xF), C=P+0x10
    (column C only exists for cc < 0x1000 -> 12px wide; otherwise 8px wide)
    per column, flag = 1 if within & 8 else 0:
        flag 0: rows 0-7  = S+0,2,..14      rows 8-11  = S+0xC0+0,2,4,6
        flag 1: rows 0-3  = S+0,2,4,6       rows 4-11  = S+0xB8+0,2,..14
Each source byte holds 4 horizontal pixels; pixel k (left->right) = bits (2k, 2k+1).
  bit(2k+1) set -> full ink (4bpp 0xF);  bit(2k) set -> ink colour;  00 -> transparent.
"""

K_TABLE = [0, 0x11, 0x30, 0x41]
FONT_TABLE_RAM = 0x0208EFC8
FONT_TABLE_ROM = 0x92FC8
NBLOCK = 68  # entries 68.. are not pointers


def ram2rom(a):
    return a - 0x02000000 + 0x4000


def char_width(cc):
    return 8 if (cc & 0x7FFF) >= 0x1000 else 12


def glyph_map(cc):
    """-> list of 12 rows x width entries, each (byte_offset_within_region, pixel_index).

    Offsets are relative to FONT_TABLE[block]."""
    cc &= 0x7FFF
    within = cc & 0x3F
    flag = 1 if (within & 8) else 0
    P = ((within & 0x30) * 0x24
         + (0xC8 if flag else 0)
         + (0x60 if (within & 4) else 0)
         + K_TABLE[within & 3])
    cols = [P, P + (1 if (within & 3) in (0, 2) else 0x0F)]
    if cc < 0x1000:
        cols.append(P + 0x10)

    def row_src(S, r):
        if flag == 0:
            return S + 2 * r if r < 8 else S + 0xC0 + 2 * (r - 8)
        return S + 2 * r if r < 4 else S + 0xB8 + 2 * (r - 4)

    grid = []
    for r in range(12):
        row = []
        for S in cols:
            b = row_src(S, r)
            for k in range(4):
                row.append((b, k))
        grid.append(row)
    return grid


def decode_glyph(region, cc):
    """region: 0x900 bytes of the block -> 12 rows of width values (0/1/2/3)."""
    out = []
    for row in glyph_map(cc):
        vals = []
        for b, k in row:
            bits = (region[b] >> (k * 2)) & 3
            # bit(2k+1)=high=full ink(2), bit(2k)=low=faint(1)
            vals.append({0: 0, 1: 1, 2: 2, 3: 3}[bits])
        out.append(vals)
    return out


def encode_glyph(region, cc, bitmap):
    """Write bitmap (12 rows x width, values 0/1/2) into a mutable region bytearray."""
    for r, row in enumerate(glyph_map(cc)):
        for c, (b, k) in enumerate(row):
            v = bitmap[r][c] if c < len(bitmap[r]) else 0
            bits = {0: 0b00, 1: 0b01, 2: 0b10}[v]
            region[b] = (region[b] & ~(0b11 << (k * 2))) & 0xFF | (bits << (k * 2))
    return region


def load_table(rom):
    return [int.from_bytes(rom[FONT_TABLE_ROM + i * 4:FONT_TABLE_ROM + i * 4 + 4], "little")
            for i in range(NBLOCK)]


def block_region(rom, tbl, block):
    o = ram2rom(tbl[block])
    return bytearray(rom[o:o + 0x900])


def verify_no_overlap():
    """Every one of the 16 charcodes in a region must own disjoint bytes, covering 576."""
    used = {}
    for within in range(16):
        for row in glyph_map(within):
            for b, k in row:
                key = (b, k)
                assert key not in used, f"overlap {key}: {within} vs {used[key]}"
                used[key] = within
    return len(used)


if __name__ == "__main__":
    n = verify_no_overlap()
    print(f"16 charcodes -> {n} pixel slots = {n // 4} bytes (expect 576)")
