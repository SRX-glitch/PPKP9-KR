#!/usr/bin/env python3
"""A redirect region in an overlay's OWN tail, for files outside the ov28 group.

Why `side_region` cannot do this
--------------------------------
`side_region` works because overlays 28/29/30 all load at 0x021C0DC0, so each can
put its region at the one hardcoded `REGION_BASE` and the hook finds it wherever
it is. Overlay 14 (file 30) loads at 0x0216C3C0 and overlays 8/9 at 0x020CA020 --
*below* ov28. Padding them up to REGION_BASE would need 0.8-1.3 MB and would run
straight through overlay 28's RAM.

What makes this possible now
----------------------------
Session 39 moved the long escape's payload from "offset from REGION_BASE" to
"address minus RET_BASE" (main RAM). One escape form can therefore name a region
ANYWHERE in main RAM, so an overlay can keep its region in its own tail. And with
the tiny codes gone (census v2 leaves none) the long form is the only one these
files need, so there is no index table to place either.

Room, measured against the group ceiling so the RAM high-water never moves:

    ov14 (f30)  group max 184,064; insert_pointered and insert_profiles already
                grow it to 163,748, leaving 20,316 B. This needs ~6 KB.

What it ships
-------------
File 30's `extra` worklist rows whose Korean does not fit inline -- 215 of them,
and they are the ENDING text: 「여기서 둘의 여행이 시작된다 느꼈다」, 「상점가를 위해
싸운」, 「거기서 결혼해 가정을 꾸렸다」. Every one has budget >= 5, so the 5-byte
long escape fits all of them.

⚠ These screens are drawn by the ARM9 printer, so `menu_hook` and `measure_hook`
  must be installed (PPKP9_CHOICE_REDIRECT=1 PPKP9_MEASURE_HOOK=1). Without them
  the escape renders as raw glyphs.

    python tools/tail_region.py 30      # report what file 30 would gain
"""
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import redirect_hook as R
import expand_overlay as XO


def _worklist(fid):
    """[(abs offset, budget, jp, ko)] -- the SAME work `insert_extra` writes.

    ⭐ SESSION 41. This used to read `file<fid>_extra.tsv` directly, and that made
    the region blind to exactly the rows the player complains about. The map's
    「レストラン」/「カレー屋」 have NO worklist row -- `extract_extra` skipped them
    because the batch corpus already had a translation (the session-38 bug) -- so
    they reach the ROM only through `insert_extra.sites()`, which merges the batch
    corpus in when `PPKP9_BATCH_SITES=1`. Reading the worklist meant the region
    could never take them over when they did not fit, and file 20 has no other
    redirect path, so they simply stayed Japanese.

    Taking the work from `insert_extra.WORK` instead gives the region and the
    inline writer ONE source of truth, which is the relationship `side_region`
    already has with `insert_common`: insert_extra writes whatever fits, the
    region takes the rest, no overlap and nothing falls between them.
    ⭐⭐ AND `insert_common`'s runs worklist on top of that. 「（そして・・・）」 is
    translated as 「（그리고・・・）」 in `file8_runs.tsv` and shipped in NEITHER form:
    `insert_common.SHIP` is (4, 27), and `insert_extra`/this module only ever read
    `file<fid>_extra.tsv` plus the batch corpus. For files 8/18/20 that whole
    worklist had NO READER AT ALL -- the translation existed and went nowhere.
    Its rows carry no offsets (they are found by re-walking), so they are located
    here in the PRISTINE ROM, which is the coordinate system `plan()` rebases from.
    """
    out = []
    try:
        import insert_extra as IX
        out = [(off, blen, jp, ko) for off, blen, jp, ko in IX.WORK(fid)]
        # ⭐ SESSION 43. `PPKP9_TAIL_NO_BATCH=<fids>` keeps the batch-corpus
        # sites OUT of the region while still letting `insert_extra` write the
        # ones that fit INLINE. That splits the two halves of the file-30 hang:
        # 142 batch sites were added there, most written in place and two given a
        # 5-byte escape inside the ALBUM name list (0x326495 ゴルトマン,
        # 0x326775 フグ怪人). Only the escapes are suspect -- inline Korean is
        # the same shape the run already had -- and this switch is how that gets
        # proven instead of assumed.
        if fid in {int(x) for x in
                   os.environ.get("PPKP9_TAIL_NO_BATCH", "").split(",")
                   if x.strip()}:
            _rowoff = {o for o, _b, _j, _k in IX.rows(fid)}
            out = [r for r in out if r[0] in _rowoff]
    except Exception:
        pass
    # ⛔⛔ REVERTED, SESSION 41 -- `PPKP9_kr_v179_runs.nds` HANGS IN THE PROLOGUE.
    # Every gate was green (escape/region 19180/19180, structural 0, glyph
    # 1588/1588, extra-worklist 10678/10678 live) and the game still never gets
    # past the opening -- the §5 lesson exactly: gates prove the state of the
    # artifact, never that the change did what it meant to.
    # What this added: 230 redirect escapes into file 8's `F8 6B` runs (up from
    # 219). File 8 holds 54 POINTER ARRAYS and its records are MOVED by
    # `insert_file8`'s pointer path; the region's guard only refuses a target
    # whose own bytes read as a live overlay pointer, so it cannot see a run that
    # some other consumer reads as a RECORD. Writing an escape there is not the
    # same risk as writing Korean of the same length.
    # ⇒ Re-enable per file and prove it on hardware ONE FILE AT A TIME, and start
    #   with 18/20 (no pointer arrays) rather than 8. `PPKP9_TAIL_RUNS=8,18,20`.
    _runs_ok = {int(x) for x in
                os.environ.get("PPKP9_TAIL_RUNS", "").split(",") if x.strip()}
    try:
        import insert_common as IC
        import extract_common as EC
        tr = IC.load(fid) if fid in _runs_ok else None
        if tr:
            pri = open(ORIG, "rb").read()
            f = int.from_bytes(pri[0x48:0x4C], "little")
            lo = int.from_bytes(pri[f + fid * 8:f + fid * 8 + 4], "little")
            hi = int.from_bytes(pri[f + fid * 8 + 4:f + fid * 8 + 8], "little")
            seen = {o for o, _b, _j, _k in out}
            for off, text, ccs in EC.orig_runs(pri, lo, hi):
                ko = tr.get(text)
                # +3: `orig_runs` reports the opener, the text starts past it
                if ko is None or off + 3 in seen:
                    continue
                out.append((off + 3,
                            sum(1 if cc < 231 else 2 for cc in ccs), text, ko))
    except Exception:
        pass
    return out


ORIG = (r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/"
        r"Power Pro Kun Pocket 9 (Japan).nds")


def pristine_lo(fid):
    """Where file `fid` starts in the UNMODIFIED ROM.

    ⛔ The worklist offsets in `survey/common/file<fid>_extra.tsv` are absolute
    offsets into the PRISTINE ROM. By the time this pass runs, file 30 has been
    relocated twice (`insert_pointered`, then `insert_profiles`), so subtracting
    the CURRENT FAT start gives a negative run offset and the return address
    comes out below RET_BASE -- the build dies with "return 0x-0806A17 is outside
    overlay 28". Everything here works in FILE-RELATIVE offsets and is rebased
    onto whatever the live FAT says.
    """
    b = open(ORIG, "rb").read()
    fat = int.from_bytes(b[0x48:0x4C], "little")
    return int.from_bytes(b[fat + fid * 8:fat + fid * 8 + 4], "little")


def plan(rom, fid, enc):
    """Rows this pass owns: over budget inline, and big enough for the long form.

    Under-budget rows belong to `insert_extra`, which writes them in place --
    taking them here would be a double write on the same bytes.
    """
    import insert_extra as IX
    pri = pristine_lo(fid)
    out = []
    for off, budget, jp, ko in _worklist(fid):
        try:
            kb = enc.encode(ko)
        except KeyError:
            continue
        if len(kb) <= budget:
            continue                      # insert_extra writes it inline
        if budget < R.LONG_BUDGET:
            continue                      # cannot hold even the 5-byte escape
        # Control-flow guard (canonical width table): a row extracted with the
        # old table can start on an opcode marker/operand byte; the escape
        # write would clobber it. Same rule as insert_extra.apply_all.
        if IX.hits_opcode(fid, off, budget):
            continue
        out.append((off - pri, budget, jp, ko, kb))   # FILE-RELATIVE
    return out


def build(rom, fid, enc, region_ram):
    """(region bytes, [(offset, escape, budget)], stats).

    `region_ram` is where the region will sit in main RAM -- the overlay's tail.
    Every entry is long-form, so `n_indexed=0` and no offset table is emitted.
    """
    items = plan(rom, fid, enc)
    info = XO.overlay_of_file(bytes(rom), fid)
    if info is None:
        raise SystemExit(f"FAT[{fid}] has no overlay-table entry")
    ov_ram = info[2]
    lo = _fat_lo(rom, fid)          # where the file sits NOW, after relocation

    entries = [(kb, ov_ram + rel + budget)
               for rel, budget, _jp, _ko, kb in items]
    region, offs = R.build_region(entries, 0, region_ram)

    # ⛔ SESSION 29 SAVE-WIPE GUARD, same one `insert_extra.GUARDED` and
    # `insert_file8.apply_orphans` carry. It was missing here, and session 41
    # pointed this region at files 18 and 20 -- file 20 being one of the two the
    # wipe was ever traced to. An escape is a WRITE like any other: if the bytes
    # it lands on currently read as a live overlay pointer, it shreds a pointer
    # array. Refuse those targets and say how many.
    ptr = (ov_ram, info[3]) if fid in (8, 18, 20) else None
    writes, manifest, refused = [], [], 0
    for k, (rel, budget, jp, ko, _kb) in enumerate(items):
        esc = R.escape_bytes(0, budget, offs[k])
        if len(esc) > budget:
            continue
        at = lo + rel
        if ptr and any(ptr[0] <= int.from_bytes(rom[a:a + 4], "little")
                       < ptr[0] + ptr[1]
                       for a in range(at & ~3, at + budget, 4)):
            refused += 1
            continue
        writes.append((lo + rel, esc, budget))
        manifest.append({"rel": rel, "budget": budget, "idx": k,
                         "jp": jp, "ko": ko})
    return region, writes, {"runs": len(items), "entries": len(entries),
                            "bytes": len(region), "manifest": manifest,
                            "refused": refused, "region_ram": region_ram}


def _fat_lo(rom, fid):
    fat = int.from_bytes(bytes(rom[0x48:0x4C]), "little")
    return int.from_bytes(bytes(rom[fat + fid * 8:fat + fid * 8 + 4]), "little")


def main():
    import koenc
    fid = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    here = os.path.dirname(os.path.abspath(__file__))
    fontmap = {k: int(v) for k, v in json.load(
        open(os.path.join(here, "..", "survey", "font", "kr_font_map.json"),
             encoding="utf-8")).items()}
    enc = koenc.Encoder({"syl": fontmap, "one": {}, "raw": {" ": "00"}})
    rom = bytearray(open(R.__dict__.get("ORIG") or
                         r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/"
                         r"Power Pro Kun Pocket 9 (Japan).nds", "rb").read())
    rows = plan(rom, fid, enc)
    need = sum(len(r[4]) + 5 for r in rows)
    print(f"file {fid}: {len(rows)} rows need the tail region, ~{need:,} B")
    for rel, budget, jp, ko, kb in rows[:8]:
        print(f"   +0x{rel:06X} b{budget:<3d} {len(kb):3d}B  {jp[:24]} -> {ko[:24]}")


if __name__ == "__main__":
    main()
