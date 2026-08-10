#!/usr/bin/env python3
"""Patch the FF-terminated text tables (files 13, 18, 30) in place.

These three are NOT part of overlay 28, so `build_kr`'s redirect machinery never
touched them and their text shipped in Japanese -- which is what the character
encyclopedia screen showed. They are also not plain data files: each is an
overlay whose first bytes are ARM code (`e92d4070` = stmfd sp!,{...}), so moving
or growing one is the same size of job as overlay 28 was. This module therefore
does the cheap thing that needs no hook, no relocation and no ROM growth: write
the Korean **inside the record's own bytes** and skip anything that will not fit.

  18  ability NAMES      fixed 8-byte slots. Write `ko + FF + 00...` to the slot
                         end -- that is the shape the originals already have.
                         Budget is 7 bytes, so 3 Korean syllables. All 67 fit.
  13  ability EFFECTS    variable, FF-terminated.
  30  encyclopedia       variable, FF-terminated, with 00 padding inside records.

For 13 and 30 the terminator STAYS WHERE IT IS. Moving it earlier would shorten
the record and hand the leftover original bytes to the next one; instead the
Korean is written at the record start and the remainder up to the original FF is
zero-filled. Byte 0x00 is safe filler: render_char's zero path clears a single
4px column rather than drawing charcode 0 (session 24), and file 30's records
already carry 00 padding internally.

⚠ Budgets must be measured from the ROM, not from the extracted Japanese. The
extractor decodes file 30 with `skip_nul=True`, so a reconstructed string is
shorter than the bytes it came from, and sizing against it overstates the budget
badly (it claimed 429 of 442 rows fit; the true figure is 309). Always scan
forward to the real 0xFF.

    python tools/insert_tables.py --report        # what fits, what does not
    python tools/insert_tables.py --out ROM.nds   # write a patched copy
"""
import argparse, csv, glob, os, sys

sys.path.insert(0, os.path.dirname(__file__))
import koenc
import poketbl as P
import expand_overlay as X

ORIG = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
COMMON = os.path.join(os.path.dirname(__file__), "..", "survey", "common")

SLOT = {18: 8}          # files whose records sit on a fixed stride
MAXREC = 0x80           # no record is anywhere near this long


def rows(fid):
    # "menu" is the daily action menu (`戻ります` / `練習をします` / `セーブして
    # 終わります` ...) that sits near 0x2a2440, outside every FAT file we had
    # surveyed. It was confirmed byte-identical to retail early on and then
    # never put on a worklist, so it shipped in Japanese on the screen the
    # player sees every single day.
    name = "menu_table.tsv" if fid == "menu" else f"file{fid}_table.tsv"
    path = os.path.join(COMMON, name)
    with open(path, encoding="utf-8") as f:
        for r in list(csv.reader(f, delimiter="\t"))[1:]:
            if len(r) >= 6 and r[5].strip():
                # ko is stripped: the record's own leading 0x00 indent is
                # preserved by patch(), so a leading space here would double it.
                off = int(r[1], 16)
                if _inside_profile_record(off):
                    continue
                yield off, r[4], r[5].strip()


def _profile_spans():
    """Byte ranges of encyclopedia records that insert_profiles will repoint.

    The scan that built `file30_table.tsv` had no idea about FA, so where a
    profile record is `line1 FA line2 FA line3 FF` it also recorded line3 on its
    own -- an offset that sits INSIDE the record. Writing Korean there in place
    clobbers the middle of a record the pointer pass is about to rewrite whole,
    and the profile pass then refuses it because its Japanese no longer matches.
    The pointer path wins: it carries the entire record with no length limit.
    """
    global _SPANS
    if _SPANS is None:
        try:
            import insert_profiles as IPF
            _SPANS = [(off, off + len(IPF.encode_jp(jp)))
                      for off, jp, _ko in IPF.rows()]
        except Exception:
            _SPANS = []
    return _SPANS


_SPANS = None


def _inside_profile_record(off):
    return any(a <= off < b for a, b in _profile_spans())


def verify_offset(rom, off, jp):
    """Do the ROM bytes at `off` really decode to `jp`?

    This is the guard that has to exist. The extractor found file 30's records
    by scanning, and for the album titles it locked on two bytes too late: the
    real record is

        f7 68  f7 8c  00  f7 52 f7 54  00 00 00 00  d3 <title> d4 ff
        `------ icon / entry-number glyph codes ------'  「        」

    and the scan started inside `f7 54`, so the recorded "Japanese" begins with
    an operand byte -- which is where `エ「心の旅」`, `ウ8「戻った男」` and
    `ネo18「…」` get their nonsense prefixes from. Writing Korean at that offset
    overwrites the number glyph's operand and wrecks the entry.

    Re-encoding jp and comparing is the cheap, total check: if the bytes do not
    match, the offset is not a record start and nothing may be written there.
    0x00 is skipped on the ROM side because file 30 pads inside its records and
    the extractor decoded it with skip_nul.
    """
    # The decisive test is the byte BEFORE the record. Charcode lead bytes are
    # 0xE8-0xF7, so if one sits at off-1 then `off` is the SECOND byte of a
    # two-byte charcode and the record does not start here. That is exactly the
    # album titles: `f7 54` is an entry-number glyph and the scan locked onto its
    # 0x54, which decodes to a perfectly real `エ` -- so comparing the decoded
    # bytes against the ROM (they match!) can never catch this. Only the
    # predecessor can. Conservative by design: a legitimate record start whose
    # preceding byte happens to fall in that range is skipped rather than risked.
    if off > 0 and 0xE8 <= rom[off - 1] <= 0xF7:
        return False
    j = off
    for ch in jp:
        while j < len(rom) and rom[j] == 0:
            j += 1
        if ch == " ":
            continue          # the decoder renders 0x00 padding as a space

        cc = P.CH2CC.get(ch)
        if cc is None:
            return False
        b = P.cc_to_bytes(cc)
        if rom[j:j + len(b)] != b:
            return False
        j += len(b)
    return True


def lead_pad(rom, off, term):
    """Length of the record's original leading 0x00 indent."""
    n = 0
    while off + n < term and rom[off + n] == 0:
        n += 1
    return n


def budget(rom, fid, off):
    """Bytes for the Korean: record length minus terminator AND minus indent.

    The indent has to be charged. Leaving it out lets a row be accepted and then
    silently clipped: 「돌아간다」 is exactly 8 bytes and its record is 8, so the
    3-byte indent had nowhere to go, the label was drawn from the record start,
    and the first two glyphs fell outside the box -- 「F 간다」 on screen. Charging
    it means such a row is refused and stays readable Japanese instead.
    """
    if fid in SLOT:
        # the slot is the budget, whatever the original string length was
        return SLOT[fid] - 1
    term = rom.find(b"\xff", off, off + MAXREC)
    if term < 0:
        return -1
    return term - off - lead_pad(rom, off, term)


_REPOINTED = None


def _repointed(rom):
    """Offsets `insert_file8` will move whole -- the pointer path wins over ours.

    ⚠ The `menu` table is NOT "outside every FAT file", as the comment above it
    claimed for a long time: 0x2A2440 sits inside **file 20** (0x22DA00-0x2AE440),
    which is also where the practice/ability panel reads its strings. Writing the
    menu in place therefore put Korean at offsets the file-20 pointer pass gates
    on, and it refused 24 of the 66 records it was about to free -- and left 330
    non-pointer bytes changed in a file that is under the save-wipe ban.
    """
    global _REPOINTED
    if _REPOINTED is None:
        try:
            import insert_file8 as F8
            _REPOINTED = F8.handled_offsets(rom)
        except Exception:
            _REPOINTED = set()
    return _REPOINTED


def holds_pointers(rom, fid, off, term):
    """Does [off, term) contain u32s that land inside this overlay's RAM span?

    Then it is a POINTER ARRAY, not a string, and writing there breaks the game's
    own indirection. The extractor cannot tell: `88 1b 18 02` (= 0x02181B88) is a
    perfectly decodable run of kana, which is how the row at 0x325D93 came to
    claim seven pointers as the prefix of 「神田カンタ（かんだかんた）」. Writing it
    replaced the pointers AND -- because the array's interior 0x00 was skipped
    when the Japanese was extracted but not re-emitted -- shifted the name one
    byte left, so its first glyph drew as something else (「우다 칸타」 on screen).
    `verify_offset` cannot catch this: the bytes really do decode to that text.
    """
    ent = X.overlay_of_file(rom, fid) if isinstance(fid, int) else None
    if ent is None:
        return False
    lo = X.u32(rom, X.u32(rom, 0x48) + fid * 8)
    _, _, ram, size = ent
    for a in range(off, max(off, term - 3)):
        if (a - lo) % 4:
            continue
        if ram <= int.from_bytes(rom[a:a + 4], "little") < ram + size:
            return True
    return False


def patch(rom, fid, enc, apply=True):
    """Returns (written, skipped, [(shortfall, jp, ko, budget, need)])."""
    written, skipped, over, bad_off = 0, 0, [], 0
    for off, jp, ko in rows(fid):
        b = budget(rom, fid, off)
        if b < 0:
            skipped += 1
            continue
        if not verify_offset(rom, off, jp):
            skipped += 1
            bad_off += 1
            continue
        _t = rom.find(b"\xff", off, off + MAXREC)
        if _t > 0 and holds_pointers(rom, fid, off, _t):
            skipped += 1
            bad_off += 1
            continue
        # Range check, not equality: a menu row's offset is the RECORD start and
        # includes the leading 0x00 indent, while the pointer pass records the
        # run itself a few bytes later (`   練習をします` at 0x2A2481 vs the run at
        # 0x2A2484). Comparing offsets matched almost nothing and the in-place
        # write went through anyway.
        if _t > 0 and any(off <= r <= _t for r in _repointed(rom)):
            skipped += 1
            continue
        kb = enc.encode(ko)
        if len(kb) > b:
            skipped += 1
            over.append((len(kb) - b, jp, ko, b, len(kb)))
            continue
        if apply:
            if fid in SLOT:
                end = off + SLOT[fid]
                rom[off:end] = kb + b"\xff" + b"\x00" * (SLOT[fid] - len(kb) - 1)
            else:
                term = rom.find(b"\xff", off, off + MAXREC)
                # KEEP THE ORIGINAL LEADING 0x00 RUN. Those bytes are not slack,
                # they are the record's indent -- the renderer starts drawing at
                # the record start, so writing Korean from byte 0 shifts the
                # whole label left and the first glyphs fall outside the box.
                # Observed: 「능력 올리기」 came out 「력 올리기」 with 능 simply gone,
                # while 「설정」 -- whose original 「システム」 has NO leading padding --
                # rendered in full. 능(0x174) and 력(0x175) are adjacent charcodes
                # in the same block with the same font pointer, which is what
                # ruled out every font-side explanation.
                pad = lead_pad(rom, off, term)
                rom[off:term] = (b"\x00" * pad + kb
                                 + b"\x00" * (term - off - pad - len(kb)))
        written += 1
    over.sort(reverse=True)
    return written, skipped, over, bad_off


# File 13 is deliberately NOT shipped yet. Its records are sentence FRAGMENTS
# that the game concatenates (`手に強く、` is the tail of 「相手に強く、」), and only
# 1 of its 50 rows fits, so inserting it would build single sentences out of
# half Korean and half Japanese -- worse to read than leaving it alone. It goes
# in once the rows are short enough to ship as a set.
# ⚠ NOTHING SHIPS YET. Writing Korean into these tables produced garbled glyphs
# on screen even with correct bytes AND non-extension charcodes: the daily menu
# drew 「돌아간다」 as 「F 간다」 -- 간/다 (0x46d, 0x141) resolved while 돌/아 (0x36a,
# 0x2b1) did not. So these screens use a DIFFERENT font table from the dialogue
# engine, and only part of the charcode space overlaps. Until that table is
# identified and repointed, garbled Korean is worse than the original Japanese.
# The translations and offsets are all verified and ready; only the glyph route
# is missing. Re-enable per file once a screen has been checked in the emulator.
SHIP = (18, 30, "menu")


def apply_all(rom, verbose=True, files=SHIP):
    """Patch the table files into `rom` (a bytearray). Used by build_kr."""
    enc = koenc.Encoder()
    total_w = total_s = 0
    for fid in files:
        w, s, _, bo = patch(rom, fid, enc)
        total_w += w
        total_s += s
        if verbose:
            print(f"  table file {fid}: {w} written, {s} skipped "
                  f"({bo} of them because the offset does not match the ROM)")
    return {"written": total_w, "skipped": total_s}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--rom", default=ORIG)
    a = ap.parse_args()

    rom = bytearray(open(a.rom, "rb").read())
    enc = koenc.Encoder()

    if a.report:
        for fid in (13, 18, 30):
            w, s, over, bo = patch(rom, fid, enc, apply=False)
            print(f"\n=== file {fid} ===  들어감 {w}   초과 {s}")
            for d, jp, ko, b, n in over[:8]:
                print(f"   +{d:3}B  예산{b:3}B  {jp[:22]!r} -> {ko[:22]!r} ({n}B)")
        return

    if not a.out:
        sys.exit("--report 로 확인하거나 --out 으로 패치본을 쓸 것")
    stats = apply_all(rom)
    open(a.out, "wb").write(rom)
    print(f"\n{stats['written']} rows written, {stats['skipped']} skipped -> {a.out}")


if __name__ == "__main__":
    main()
