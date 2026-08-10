import sys, struct, re
b = open(sys.argv[1], 'rb').read()
print('len', hex(len(b)))
# every 4-char ASCII id followed by a plausible u32 size
pat = re.compile(rb'[0-9A-Za-z_]{4}')
hits = []
for m in pat.finditer(b[:0x200000]):
    o = m.start()
    if o + 12 > len(b):
        continue
    a, c = struct.unpack_from('<II', b, o + 4)
    for size in (a, c):
        if size in (0x400000, 0x8000, 0x4000, 0x40000, 0x20000):
            hits.append((o, m.group().decode(), hex(a), hex(c)))
            break
for h in hits[:40]:
    print(h)
print('--- direct search for 0x00400000 le')
for m in re.finditer(b'\x00\x00\x40\x00', b[:0x300000]):
    o = m.start()
    print(hex(o), b[o-12:o+8].hex(), repr(b[o-12:o]))
