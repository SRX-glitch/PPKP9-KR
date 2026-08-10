#!/usr/bin/env python3
"""DeSmuME savestate (.dst) -> raw memory regions.

Why this exists: the emucap NDS adapter's `dump_memory` times out, and
`read_memory` moves only ~8KB per MCP round trip, so a 4MB RAM image would be
hundreds of calls.  The GDB stub would be ideal but accepts a single client and
the emucap bridge already holds it.  A savestate, however, stores every region
uncompressed -- so `save_state` + this parser is the cheap way to get a full
RAM image at any observation point.

Chunk stream (DeSmuME 0.9.x): 4cc id | u32 version | u32 size | payload.
Rather than parse the whole stream (the leading CPU chunks use a different
field order), locate regions by their 4cc directly:

    WRAM  0x400000  main RAM      -> RAM base 0x02000000
    ITCM  0x008000                -> 0x01000000
    DTCM  0x004000

Usage:
    python3 dst_ram.py <state.dst> --list
    python3 dst_ram.py <state.dst> [--region WRAM] [--out out.bin]
"""
import sys, struct, os

REGIONS = {
    "WRAM": (0x400000, 0x02000000),
    "ITCM": (0x008000, 0x01000000),
    "DTCM": (0x004000, 0x00000000),
}


def find_region(buf, name):
    """Return (payload_offset, size, ram_base) for a 4cc region chunk."""
    want, base = REGIONS[name]
    key = name.encode()
    off = 0
    while True:
        off = buf.find(key, off)
        if off < 0:
            raise SystemExit(f"{name} chunk not found")
        ver, size = struct.unpack_from("<II", buf, off + 4)
        if size == want and ver < 0x100 and off + 12 + size <= len(buf):
            return off + 12, size, base
        off += 1


def load(path, name="WRAM"):
    buf = open(path, "rb").read()
    off, size, base = find_region(buf, name)
    return buf[off:off + size], base


if __name__ == "__main__":
    p = sys.argv[1]
    if "--list" in sys.argv:
        buf = open(p, "rb").read()
        for name in REGIONS:
            try:
                off, size, base = find_region(buf, name)
                print(f"{name}  size=0x{size:<8x} file@0x{off:x}  ram_base=0x{base:08x}")
            except SystemExit as e:
                print(f"{name}  {e}")
        raise SystemExit(0)
    name = sys.argv[sys.argv.index("--region") + 1] if "--region" in sys.argv else "WRAM"
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv \
        else os.path.splitext(p)[0] + f".{name.lower()}.bin"
    data, base = load(p, name)
    open(out, "wb").write(data)
    print(f"wrote {out} 0x{len(data):x} bytes (RAM base 0x{base:08x})")
