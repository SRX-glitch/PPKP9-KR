#!/usr/bin/env python3
"""Initial-survey parser for a Nintendo DS ROM: header + NitroFS enumeration.
Read-only: never writes into the ROM. Emits a filesystem listing and header facts."""
import struct, sys, os, hashlib, json

def u16(b, o): return struct.unpack_from("<H", b, o)[0]
def u32(b, o): return struct.unpack_from("<I", b, o)[0]

def parse_header(d):
    h = {}
    h["title"] = d[0x00:0x0C].split(b"\x00")[0].decode("ascii", "replace")
    h["gamecode"] = d[0x0C:0x10].decode("ascii", "replace")
    h["makercode"] = d[0x10:0x12].decode("ascii", "replace")
    h["unitcode"] = d[0x12]
    h["arm9_rom_off"] = u32(d, 0x20); h["arm9_entry"] = u32(d, 0x24)
    h["arm9_ram"] = u32(d, 0x28); h["arm9_size"] = u32(d, 0x2C)
    h["arm7_rom_off"] = u32(d, 0x30); h["arm7_entry"] = u32(d, 0x34)
    h["arm7_ram"] = u32(d, 0x38); h["arm7_size"] = u32(d, 0x3C)
    h["fnt_off"] = u32(d, 0x40); h["fnt_size"] = u32(d, 0x44)
    h["fat_off"] = u32(d, 0x48); h["fat_size"] = u32(d, 0x4C)
    h["ov9_off"] = u32(d, 0x50); h["ov9_size"] = u32(d, 0x54)
    h["ov7_off"] = u32(d, 0x58); h["ov7_size"] = u32(d, 0x5C)
    h["banner_off"] = u32(d, 0x68)
    h["rom_used"] = u32(d, 0x80)
    h["header_crc"] = u16(d, 0x15E)
    return h

def read_fat(d, fat_off, fat_size):
    fat = []
    for i in range(fat_size // 8):
        s = u32(d, fat_off + i*8); e = u32(d, fat_off + i*8 + 4)
        fat.append((s, e))
    return fat

def read_fnt(d, fnt_off):
    # returns {file_id: fullpath}
    # main table: entries of 8 bytes; entry0 gives total dir count
    total_dirs = u16(d, fnt_off + 6)
    names = {}
    def walk(dir_id, prefix):
        idx = dir_id & 0x0FFF
        sub_off = u32(d, fnt_off + idx*8)
        first_file = u16(d, fnt_off + idx*8 + 4)
        p = fnt_off + sub_off
        fid = first_file
        while True:
            t = d[p]; p += 1
            if t == 0:
                break
            length = t & 0x7F
            is_dir = (t & 0x80) != 0
            nm = d[p:p+length].decode("ascii", "replace"); p += length
            if is_dir:
                subdir_id = u16(d, p); p += 2
                walk(subdir_id, prefix + "/" + nm)
            else:
                names[fid] = prefix + "/" + nm
                fid += 1
    walk(0xF000, "")
    return names, total_dirs

def main():
    rom = sys.argv[1]
    outdir = sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    d = open(rom, "rb").read()
    h = parse_header(d)
    h["file_size"] = len(d)
    h["sha1"] = hashlib.sha1(d).hexdigest()
    h["md5"] = hashlib.md5(d).hexdigest()
    fat = read_fat(d, h["fat_off"], h["fat_size"])
    h["fat_entries"] = len(fat)
    names, total_dirs = read_fnt(d, h["fnt_off"])
    h["total_dirs"] = total_dirs
    h["named_files"] = len(names)
    # overlay count from overlay table size (each entry 32 bytes)
    h["ov9_count"] = h["ov9_size"] // 32
    h["ov7_count"] = h["ov7_size"] // 32

    # file listing: id, path, start, end, size, ext
    rows = []
    for fid, path in sorted(names.items()):
        if fid < len(fat):
            s, e = fat[fid]
            rows.append((fid, path, s, e, e - s))
    # write listing
    with open(os.path.join(outdir, "filelist.tsv"), "w", encoding="utf-8") as f:
        f.write("file_id\tpath\tstart\tend\tsize\n")
        for r in rows:
            f.write(f"{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\t{r[4]}\n")
    with open(os.path.join(outdir, "header.json"), "w", encoding="utf-8") as f:
        json.dump(h, f, indent=2, ensure_ascii=False)

    # extension histogram
    exth = {}
    for r in rows:
        ext = os.path.splitext(r[1])[1].lower() or "(none)"
        exth.setdefault(ext, [0,0])
        exth[ext][0] += 1
        exth[ext][1] += r[4]

    print("=== HEADER ===")
    for k in ["title","gamecode","makercode","unitcode","file_size","sha1","md5",
              "arm9_rom_off","arm9_ram","arm9_size","arm7_rom_off","arm7_ram","arm7_size",
              "fnt_off","fnt_size","fat_off","fat_size","fat_entries","named_files","total_dirs",
              "ov9_count","ov7_count","banner_off","rom_used","header_crc"]:
        v = h[k]
        if isinstance(v, int) and k not in ("unitcode","file_size","fat_entries","named_files","total_dirs","ov9_count","ov7_count","rom_used","header_crc"):
            print(f"  {k:16} 0x{v:08X} ({v})")
        else:
            print(f"  {k:16} {v}")
    print("\n=== EXTENSION HISTOGRAM (count, total bytes) ===")
    for ext, (c, sz) in sorted(exth.items(), key=lambda x: -x[1][1]):
        print(f"  {ext:10} {c:6} files  {sz:12,} bytes")
    print(f"\n=== TOP 25 LARGEST FILES ===")
    for r in sorted(rows, key=lambda x: -x[4])[:25]:
        print(f"  id={r[0]:5} {r[4]:12,}  {r[1]}")
    print(f"\nWrote: {outdir}/filelist.tsv, header.json")

if __name__ == "__main__":
    main()
