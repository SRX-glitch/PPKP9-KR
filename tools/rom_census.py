#!/usr/bin/env python3
"""Whole-ROM charcode census -- EVERY consumer, not just dialogue.

Why this replaces global_census.py
----------------------------------
`global_census.py` walks the ROM behind an `F8 6B` gate: a text run only counts
once a message opener has been seen. That is the right filter for *scenario*
text and the wrong one for a font census, because the game draws charcodes from
places that are not messages at all. Session 39's bug report is exactly that
failure: the player-name database is a fixed-stride record array, not dialogue,
so 「笠 稲 鶴 岡」 were reported free, given to Hangul, and the baseball lineup
screen came out as 小島原 / 刃葉 / 熱塁.

    笠 cc599   dialogue 0x   array 3x     <- old census said FREE
    稲 cc335   dialogue 0x   array 1x
    鶴 cc2200  dialogue 0x   array 2x
    岡 cc455   dialogue 0x   array 18x

Why not "just count every decodable byte"
-----------------------------------------
Measured: an ungated opcode walk over the overlays claims 3,255 of the 3,264
addressable 12px slots. Almost all of that is the walker desyncing into ARM code
and record data and decoding it as text -- every region of this ROM, including
pure graphics files, decodes at ~1.5 chars/byte because most byte values are
valid charcodes. A census with no structure is not conservative, it is empty.

So each source here is *structurally* anchored, and every charcode it claims
carries provenance (site + decoded text) so the claim can be audited by eye.

Sources
-------
  dialogue  `F8 6B` gated opcode walk                      (scenario text)
  array     fixed-stride FF-terminated record arrays       (names, ability
            labels, item names -- slot k at base + k*S, run then 0xFF then
            zero padding to the stride; >= MINSLOTS slots in a row)
  packed    variable-length FF-terminated record chains    (ability blurbs)
            with a text-plausibility filter, because an unfiltered chain walks
            straight out of a real table into the binary behind it.
  ime       u16 LITTLE-ENDIAN charcode lists, 0xFFFF terminated (kanji input
            dictionary)

The `ime` source is a second container format and it is the expensive one. In
overlay 13 (file 28), 0x2F63E0-0x2F7FC0 holds a reading-indexed kanji dictionary
for name entry -- 「たき」→滝瀧, 「だく」→濁諾 -- stored as u16 LE rather than in
the PokeTEXT byte order:

    ... FF FF | 04 E8 | 05 E8 | 06 E8 | 07 E8 | 08 E8 | 09 E8 | ... | FF FF
               哀      愛      挨      姶      逢      葵

1,837 distinct kanji, all of them in the 12px pool, every one of them drawn on
the name-input screen. Read in PokeTEXT order those same bytes decode as
plausible-looking records, so the byte-order-blind scanners claim the WRONG
charcodes there -- which is why `array`/`packed` skip any span `ime` claims.

Search space: ARM9, ARM7 and the 36 overlays. FAT files 36+ were checked for
Japanese text and are graphics/audio only -- the sole exception is
`/FsBin/multiboot/pp9mini.srl`, a separate embedded DS ROM with its own font,
which this patch does not touch (see --check-fsbin).

    python tools/rom_census.py                 # full census + free-slot count
    python tools/rom_census.py --why 599       # provenance for one charcode
    python tools/rom_census.py --check-fsbin   # re-derive the FsBin exclusion
"""
import os, sys, json, bisect, argparse, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P
import fontcodec as F

BASE = r"C:/Users/jngji/Desktop/실험실"
ORIG = BASE + r"/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
PROJ = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr"
OUT = PROJ + r"/survey/font"

MINSLOTS = 8                       # fixed-stride array: slots in a row
STRIDES = range(4, 49, 2)
MINPACK = 6                        # packed chain: records in a row

# Gaiji / unit glyphs that live in the font but never in a real record. A chain
# that hits one has walked out of the table into the binary behind it.
JUNK = set("㎏㎞㎡￥‰§¶†‡№°±×÷∞∵∴⇒⇔∀∃∠⊥⌒∫∪∩")

CC = P.CC2CH


# ---------------------------------------------------------------- ROM layout
class Rom:
    def __init__(self, path=ORIG):
        self.b = open(path, "rb").read()
        b = self.b
        self.arm9 = (int.from_bytes(b[0x20:0x24], "little"),
                     int.from_bytes(b[0x2C:0x30], "little"))
        self.arm7 = (int.from_bytes(b[0x30:0x34], "little"),
                     int.from_bytes(b[0x3C:0x40], "little"))
        ov9 = int.from_bytes(b[0x50:0x54], "little")
        self.novl = int.from_bytes(b[0x54:0x58], "little") // 32
        self.fat = int.from_bytes(b[0x48:0x4C], "little")
        self.nfiles = int.from_bytes(b[0x4C:0x50], "little") // 8
        self.ovl = []
        for k in range(self.novl):
            e = b[ov9 + k * 32: ov9 + k * 32 + 32]
            self.ovl.append({
                "id": int.from_bytes(e[0:4], "little"),
                "ram": int.from_bytes(e[4:8], "little"),
                "size": int.from_bytes(e[8:12], "little"),
                "bss": int.from_bytes(e[12:16], "little"),
                "file": int.from_bytes(e[24:28], "little"),
                "comp": int.from_bytes(e[28:32], "little"),
            })
        self._spans = sorted((self.span(i)[0], self.span(i)[1], i)
                             for i in range(self.nfiles) if self.span(i)[1] > self.span(i)[0])
        self._starts = [s[0] for s in self._spans]

    def span(self, fid):
        f = self.fat + fid * 8
        return (int.from_bytes(self.b[f:f + 4], "little"),
                int.from_bytes(self.b[f + 4:f + 8], "little"))

    def owner(self, off):
        a9, n9 = self.arm9
        if a9 <= off < a9 + n9:
            return "ARM9"
        a7, n7 = self.arm7
        if a7 <= off < a7 + n7:
            return "ARM7"
        k = bisect.bisect_right(self._starts, off) - 1
        if k >= 0 and self._spans[k][0] <= off < self._spans[k][1]:
            return f"f{self._spans[k][2]}"
        return "?"

    def code_regions(self):
        """ARM9 + ARM7 + every overlay -- everything that can hold script text."""
        out = [("ARM9", self.arm9[0], self.arm9[0] + self.arm9[1]),
               ("ARM7", self.arm7[0], self.arm7[0] + self.arm7[1])]
        for o in self.ovl:
            s, e = self.span(o["file"])
            out.append((f"f{o['file']}", s, e))
        return out


def filenames():
    d = {}
    p = PROJ + r"/survey/filelist.tsv"
    if os.path.exists(p):
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            q = ln.split("\t")
            if len(q) >= 2:
                d[int(q[0])] = q[1]
    return d


# ---------------------------------------------------------------- glyph pool
def glyph_pool(rom):
    """(pool_12px, alias_blocks) -- charcodes with independent glyph storage.

    Blocks 55-63 and 67 all point at block 0's region, so those 640 charcodes
    have no storage of their own; writing a glyph there would rewrite block 0.
    """
    tbl = F.load_table(rom.b)
    seen, alias = {}, set()
    for idx, p in enumerate(tbl):
        if p in seen:
            alias.add(idx)
        else:
            seen[p] = idx
    pool = [cc for cc in range(256, 0x1000) if cc >> 6 not in alias]
    return pool, alias


# ---------------------------------------------------------------- source: dialogue
def src_dialogue(rom, lo, hi, hit):
    b = rom.b
    L = json.load(open(PROJ + r"/survey/ov28/opcode_lengths.json"))
    BARE = {int(k): v for k, v in L["bare"].items()}
    F8 = {int(k): v for k, v in L["f8"].items()}
    i, ind, z = lo, False, 0
    while i < hi - 2:
        if not ind:
            j = b.find(b"\xf8\x6b", i, hi)
            if j < 0:
                break
            i = j
        c = b[i]
        if c == 0:
            z += 1
            if z >= 3:
                ind = False
            i += 1
            continue
        z = 0
        if c < 0xF8:
            st, ch, ccs = i, [], []
            while i < hi:
                x = b[i]
                if x == 0 or x >= 0xF8:
                    break
                cc, nx = P.bytes_to_cc(b, i)
                g = CC.get(cc)
                if g is None:
                    break
                ch.append(g)
                ccs.append(cc)
                i = nx
            if ccs:
                t = "".join(ch)
                for cc in ccs:
                    hit(cc, "dialogue", st, t)
            if i == st:
                i += 1
        elif c in BARE:
            if c == 0xFF:
                ind = False
            i += BARE[c]
        elif c in (0xF8, 0xF9):
            if b[i + 1] == 0x6B:
                ind = True
            n = F8.get(b[i + 1])
            if n is None:
                ind = False
                n = 2
            i += n
        else:
            i += 1


# ---------------------------------------------------------------- source: arrays
def _slot(b, i, S, hi):
    """One fixed-width slot: charcode run, 0xFF, zero padding to the stride."""
    if i + S > hi:
        return None
    end, j, ch, ccs = i + S, i, [], []
    while j < end:
        c = b[j]
        if c == 0 or c >= 0xF8:
            break
        cc, nx = P.bytes_to_cc(b, j)
        g = CC.get(cc)
        if g is None or nx > end:
            return None
        ch.append(g)
        ccs.append(cc)
        j = nx
    if not ch or j >= end or b[j] != 0xFF:
        return None
    j += 1
    while j < end:
        if b[j] != 0:
            return None
        j += 1
    return "".join(ch), ccs


def src_array(rom, lo, hi, hit, arrays=None, skip=()):
    b = rom.b
    covered = bytearray(hi - lo)
    for s, e in skip:
        for k in range(max(lo, s) - lo, min(hi, e) - lo):
            covered[k] = 1
    for S in STRIDES:
        i = lo
        while i < hi - S * MINSLOTS:
            if covered[i - lo]:
                i += 1
                continue
            if _slot(b, i, S, hi) is None:
                i += 1
                continue
            recs, j = [], i
            while True:
                r = _slot(b, j, S, hi)
                if r is None:
                    break
                recs.append((j, r))
                j += S
            if len(recs) >= MINSLOTS:
                for off, (t, ccs) in recs:
                    for cc in ccs:
                        hit(cc, "array", off, t)
                if arrays is not None:
                    arrays.append((i, S, len(recs), [r[1][0] for r in recs[:6]]))
                for k in range(i - lo, j - lo):
                    covered[k] = 1
                i = j
            else:
                i += 1


# ---------------------------------------------------------------- source: packed
def plausible(t):
    """A record that could be a real label.

    Not a language model -- just enough to stop a chain walking out of a table
    into the binary behind it, which is what the unfiltered version does (it
    chained the font pointer table at 0x92FC8 straight into the name DB).
    """
    if not t or len(t) > 32:
        return False
    if any(c in JUNK for c in t):
        return False
    ok = 0
    for c in t:
        o = ord(c)
        if (0x3040 <= o <= 0x30FF or 0x4E00 <= o <= 0x9FFF or 0xFF00 <= o <= 0xFFEF
                or o in (0x3001, 0x3002, 0x300C, 0x300D, 0x3005) or c.isalnum()):
            ok += 1
    return ok == len(t)


def _record(b, i, hi, maxpad=8):
    ch, ccs = [], []
    while i < hi:
        c = b[i]
        if c == 0 or c >= 0xF8:
            break
        cc, nx = P.bytes_to_cc(b, i)
        g = CC.get(cc)
        if g is None:
            return None
        ch.append(g)
        ccs.append(cc)
        i = nx
    if not ch or i >= hi or b[i] != 0xFF:
        return None
    i += 1
    p = 0
    while i < hi and b[i] == 0 and p < maxpad:
        i += 1
        p += 1
    return "".join(ch), ccs, i


# ---------------------------------------------------------------- source: ime
MINCHAIN = 20                      # consecutive u16 lists before we believe it


def _u16cc(v):
    h = v >> 8
    return 256 + (h - 0xE8) * 256 + (v & 0xFF) if 0xE8 <= h <= 0xF7 else None


def src_ime(rom, lo, hi, hit, spans=None):
    """u16-LE charcode lists ended by 0xFFFF, laid end to end.

    Returns the byte spans it claimed so the other scanners can skip them.
    """
    b = rom.b
    lists, i = [], lo
    while i + 1 < hi:
        seq, j = [], i
        while j + 1 < hi:
            v = int.from_bytes(b[j:j + 2], "little")
            if v == 0xFFFF:
                j += 2
                break
            c = _u16cc(v)
            if c is None:
                seq = None
                break
            seq.append(c)
            j += 2
        else:
            seq = None
        if not seq:
            i += 2
            continue
        lists.append((i, j, seq))
        i = j

    claimed, cur = [], []
    for s, e, seq in lists:
        if cur and s == cur[-1][1]:
            cur.append((s, e, seq))
        else:
            if len(cur) >= MINCHAIN:
                claimed.append(cur)
            cur = [(s, e, seq)]
    if len(cur) >= MINCHAIN:
        claimed.append(cur)

    out = []
    for chain in claimed:
        out.append((chain[0][0], chain[-1][1]))
        for s, _e, seq in chain:
            t = "".join(CC.get(c, "?") for c in seq)
            for c in seq:
                hit(c, "ime", s, t)
    if spans is not None:
        spans.extend(out)
    return out


def src_packed(rom, lo, hi, hit, chains=None, skip=()):
    b = rom.b
    blocked = bytearray(hi - lo)
    for s, e in skip:
        for k in range(max(lo, s) - lo, min(hi, e) - lo):
            blocked[k] = 1
    i = lo
    while i < hi:
        if blocked[i - lo]:
            i += 1
            continue
        r = _record(b, i, hi)
        if r is None or not plausible(r[0]):
            i += 1
            continue
        recs, j = [], i
        while True:
            r = _record(b, j, hi)
            if r is None or not plausible(r[0]):
                break
            recs.append((j, r))
            j = r[2]
        if len(recs) >= MINPACK:
            for off, (t, ccs, _e) in recs:
                for cc in ccs:
                    hit(cc, "packed", off, t)
            if chains is not None:
                chains.append((i, len(recs), [x[1][0] for x in recs[:6]]))
            i = j
        else:
            i = recs[0][1][2] if recs else i + 1


# ---------------------------------------------------------------- FsBin check
def check_fsbin(rom):
    """Do any non-overlay FAT files hold Japanese text? (Answer: only pp9mini.srl.)"""
    names = filenames()
    words = ["選手", "試合", "野球", "監督", "投手", "打者", "守備", "練習",
             "能力", "成功", "失敗", "経験", "仲間", "彼女", "友情"]
    hits = collections.Counter()
    for w in words:
        e = b"".join(P.cc_to_bytes(P.CH2CC[c]) for c in w)
        i = rom.b.find(e)
        while i >= 0:
            o = rom.owner(i)
            if o.startswith("f"):
                fid = int(o[1:])
                if fid >= 36:
                    hits[fid] += 1
            i = rom.b.find(e, i + 1)
    print("FAT files outside the overlays that contain common Japanese words:")
    if not hits:
        print("   (none)")
    for f, n in hits.most_common(20):
        print(f"   f{f:<6d} {n:5d} hits   {names.get(f, '')}")
    return hits


# ---------------------------------------------------------------- main
def census(rom, verbose=True):
    used = collections.defaultdict(collections.Counter)     # cc -> source -> n
    prov = {}                                               # cc -> (source, off, text)

    def hit(cc, source, off, text):
        used[cc][source] += 1
        if cc not in prov or (prov[cc][0] == "dialogue" and source != "dialogue"):
            prov[cc] = (source, off, text)

    arrays, chains, imes = [], [], []
    for tag, lo, hi in rom.code_regions():
        if hi <= lo:
            continue
        # ime FIRST: it decides which bytes the byte-order-blind scanners must
        # not touch. Reading a u16 list in PokeTEXT order yields real-looking
        # records made of the WRONG charcodes.
        skip = src_ime(rom, lo, hi, hit, imes)
        src_dialogue(rom, lo, hi, hit)
        src_array(rom, lo, hi, hit, arrays, skip)
        src_packed(rom, lo, hi, hit, chains, skip)
        if verbose:
            print(f"  {tag:>6} {hi-lo:8d}B  cumulative distinct {len(used)}"
                  + (f"   [ime spans {len(skip)}]" if skip else ""))
    return used, prov, arrays, chains, imes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--why", type=int, help="explain one charcode")
    ap.add_argument("--check-fsbin", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    rom = Rom()
    if a.check_fsbin:
        check_fsbin(rom)
        return

    pool, alias = glyph_pool(rom)
    print(f"ROM {len(rom.b)} bytes, {rom.nfiles} files, {rom.novl} overlays")
    print(f"font: {len(alias)} alias blocks {sorted(alias)} -> "
          f"12px charcodes with real storage: {len(pool)}")
    print("\nwalking ARM9 + ARM7 + 36 overlays ...")
    used, prov, arrays, chains, imes = census(rom, not a.quiet)
    if imes:
        print(f"\nu16 kanji-dictionary spans: {len(imes)}  "
              + ", ".join(f"0x{s:06X}-0x{e:06X}({rom.owner(s)})" for s, e in imes[:6]))

    per = collections.Counter()
    for cc, srcs in used.items():
        for s in srcs:
            per[s] += 1
    print(f"\ndistinct charcodes claimed, by source: {dict(per)}")

    inpool = {cc for cc in used if cc in set(pool)}
    free = [cc for cc in pool if cc not in used]
    print(f"in-pool used {len(inpool)} / {len(pool)}  ->  FREE {len(free)}")

    if a.why is not None:
        cc = a.why
        print(f"\ncc{cc} = {CC.get(cc)!r}  sources {dict(used.get(cc, {}))}")
        if cc in prov:
            s, off, t = prov[cc]
            print(f"   e.g. {s} at 0x{off:06X} ({rom.owner(off)}): {t}")
        return

    os.makedirs(OUT, exist_ok=True)
    json.dump({str(k): dict(v) for k, v in used.items()},
              open(OUT + "/census_v2_usage.json", "w"))
    json.dump(free, open(OUT + "/census_v2_free.json", "w"))
    with open(OUT + "/census_v2_prov.tsv", "w", encoding="utf-8") as f:
        f.write("cc\tchar\tsource\toffset\towner\tsample\n")
        for cc in sorted(prov):
            s, off, t = prov[cc]
            f.write(f"{cc}\t{CC.get(cc,'')}\t{s}\t0x{off:06X}\t{rom.owner(off)}\t{t}\n")
    print(f"\nwrote {OUT}/census_v2_usage.json, census_v2_free.json, census_v2_prov.tsv")

    slots_path = OUT + "/global_slots.json"
    if os.path.exists(slots_path):
        cur = json.load(open(slots_path))
        clash = [c for c in cur if c in used]
        print(f"\ncurrent global_slots.json: {len(cur)} slots, "
              f"{len(clash)} of them ARE drawn by someone")
        by = collections.Counter()
        for c in clash:
            by[prov[c][0]] += 1
        print(f"   by source: {dict(by)}")
        for c in clash[:15]:
            s, off, t = prov[c]
            print(f"   cc{c:<5d} {CC.get(c,''):2s} {s:8s} 0x{off:06X} {rom.owner(off):>6}  {t}")


if __name__ == "__main__":
    main()
