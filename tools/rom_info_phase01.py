# -*- coding: utf-8 -*-
"""PPKP9 Phase 0/1 fresh measurement: header, hashes, overlay table, bank map, FNT/FAT counts."""
import hashlib, json, struct, sys, io

ROM = r"C:\Users\jngji\Desktop\실험실\rom\DS\파워프로군 포켓9\Power Pro Kun Pocket 9 (Japan).nds"
data = open(ROM, "rb").read()

out = {}
out["size"] = len(data)
out["sha1"] = hashlib.sha1(data).hexdigest()
out["sha256"] = hashlib.sha256(data).hexdigest()
out["md5"] = hashlib.md5(data).hexdigest()

def u32(o): return struct.unpack_from("<I", data, o)[0]
def u16(o): return struct.unpack_from("<H", data, o)[0]

hdr = {
    "title": data[0:12].rstrip(b"\0").decode("ascii", "replace"),
    "gamecode": data[12:16].decode("ascii"),
    "makercode": data[16:18].decode("ascii"),
    "unitcode": data[18],
    "arm9_rom": u32(0x20), "arm9_entry": u32(0x24), "arm9_ram": u32(0x28), "arm9_size": u32(0x2C),
    "arm7_rom": u32(0x30), "arm7_entry": u32(0x34), "arm7_ram": u32(0x38), "arm7_size": u32(0x3C),
    "fnt_off": u32(0x40), "fnt_size": u32(0x44),
    "fat_off": u32(0x48), "fat_size": u32(0x4C),
    "ov9_off": u32(0x50), "ov9_size": u32(0x54),
    "ov7_off": u32(0x58), "ov7_size": u32(0x5C),
    "used_rom": u32(0x80),
}
out["header"] = hdr

# overlay table (ARM9)
ovs = []
n = hdr["ov9_size"] // 32
fat = hdr["fat_off"]
for i in range(n):
    o = hdr["ov9_off"] + i * 32
    ov_id, ram, size, bss, si, ei, fid, flags = struct.unpack_from("<8I", data, o)
    fstart = u32(fat + fid * 8); fend = u32(fat + fid * 8 + 4)
    ovs.append({"ov": ov_id, "ram": ram, "size": size, "bss": bss, "file_id": fid,
                "rom": fstart, "rom_size": fend - fstart, "flags": flags})
out["overlay_count"] = n
out["overlays"] = ovs

# bank map: group by ram base
banks = {}
for o in ovs:
    banks.setdefault(o["ram"], []).append(o["ov"])
out["banks"] = [{"ram": "0x%08X" % k, "ovs": v,
                 "max_size": max(x["size"] + x["bss"] for x in ovs if x["ram"] == k)}
                for k, v in sorted(banks.items())]

# FAT total files
out["fat_files"] = hdr["fat_size"] // 8

# FNT: count directories and named files
fnt = hdr["fnt_off"]
ndirs = u16(fnt + 6)
out["fnt_dirs"] = ndirs
named = 0
for d in range(ndirs):
    sub = u32(fnt + d * 8)
    p = fnt + sub
    while True:
        ln = data[p]; p += 1
        if ln == 0: break
        name_len = ln & 0x7F
        p += name_len
        if ln & 0x80: p += 2
        else: named += 1
out["fnt_named_files"] = named

json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "ppkp9_phase01.json", "w"), indent=1)

# concise print
print("size", out["size"], "used", hdr["used_rom"])
print("sha1", out["sha1"])
print("title", hdr["title"], hdr["gamecode"], hdr["makercode"], "unit", hdr["unitcode"])
print("arm9 rom=0x%X ram=0x%08X size=%d" % (hdr["arm9_rom"], hdr["arm9_ram"], hdr["arm9_size"]))
print("arm7 rom=0x%X ram=0x%08X size=%d" % (hdr["arm7_rom"], hdr["arm7_ram"], hdr["arm7_size"]))
print("fnt 0x%X %d  fat 0x%X files %d  named %d dirs %d" % (
    hdr["fnt_off"], hdr["fnt_size"], hdr["fat_off"], out["fat_files"], named, ndirs))
print("overlays", n, " ovt 0x%X" % hdr["ov9_off"])
for b in out["banks"]:
    print("bank %s  max=%6d (0x%X)  ovs=%s" % (b["ram"], b["max_size"], b["max_size"], b["ovs"]))
print("compressed overlays (flags&1):", [o["ov"] for o in ovs if o["flags"] & 0x01000000 or (o["flags"] & 0xFF000000)])
