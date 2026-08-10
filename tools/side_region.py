#!/usr/bin/env python3
"""A redirect region for a script file that is NOT overlay 28 (files 4 and 27).

The problem it solves
---------------------
`insert_common` is inline-only, so 6,369 already-translated dialogue runs in
files 4 and 27 never reach the ROM -- by far the largest remaining gap in the
patch. They could not be redirected because the region lives in overlay 28's
grown tail, and overlays 28 / 29 (file 4) / 30 (file 27) are mutually exclusive.

The way through, measured from the overlay table: **all three load at the same
RAM base 0x021C0DC0**. So each can carry its OWN region at the SAME RAM address.
The hook only ever knows `REGION_BASE`, and the return offsets it reads are
already relative to that shared base, so nothing in ARM9 or overlay 1 changes --
whichever overlay is resident, the escape resolves against that overlay's region.

    ov28 : [data 601,664] [ext pages] [ov28 region]
    ov29 : [data 551,296] [pad      ] [ext pages] [file 4 region]
    ov30 : [data 140,224] [pad      ] [ext pages] [file 27 region]

RAM high-water does not move: overlay 28 is still the largest and `expand_rom`
already pushed the heap literal past it.

⛔ NO TINY ESCAPES HERE. The 2-byte form resolves through `TINY_TBL`, a 256-byte
table in ARM9 STATIC -- one table shared by every region. A tiny code would have
to mean the same index in all three, and keeping that in step is a trap for a
future session. The banked (3-byte) and long (4-byte) forms carry their index in
the escape bytes themselves, so they are per-region by construction. The cost is
budget-2 runs only: 121 of the 6,369.

    python tools/side_region.py 27      # report what file 27 would gain
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import redirect_hook as R
import extract_common as EC
import untranslated as U
import insert_common as IC

MIN_BUDGET = 3          # banked escape; tiny (2) is deliberately excluded


def josa_map(fid):
    """{text offset: (korean particle, particle offset)} in PRISTINE offsets.

    ⭐ SESSION 43. `build_kr`'s `absorb` already moves the 1-byte Japanese
    particle that follows a name into the name's region entry, choosing 은/는 ·
    이/가 from the Korean name's final consonant -- but it only ever ran on
    overlay 28 (its offsets are `OV_FILE_START`-relative). Files 4 and 27 have
    the identical `<F808> name <F809> は` shape and nobody absorbed theirs, which
    is the 「우리빅토리즈 は」 the user photographed. Measured: f4 70 · f27 14
    sites. See tools/josa_absorb.py for why this is decidable at build time
    (the name is a static literal, so its Korean -- and its batchim -- is known).
    """
    import josa_absorb as JA
    pri = open(EC.ORIG, "rb").read()
    fat = int.from_bytes(pri[0x48:0x4C], "little")
    lo = int.from_bytes(pri[fat + fid * 8:fat + fid * 8 + 4], "little")
    hi = int.from_bytes(pri[fat + fid * 8 + 4:fat + fid * 8 + 8], "little")
    tr = dict(IC.load(fid) or {})
    try:
        import insert_extra as IX
        for _o, _b, _jp, _ko in IX.rows(fid):
            tr.setdefault(_jp, _ko)
    except Exception:
        pass
    return JA.sites(pri, lo, hi, tr)


def plan(rom, fid, enc):
    """[(text offset, budget, jp, ko, josa)] for runs that go through the region.

    Exactly the runs `insert_common` gives up on: it writes anything that fits
    and skips the rest, so taking `len(ko) > budget` here divides the work with
    no overlap and no double-write.

    ⭐ …plus the ones that FIT but carry an absorbable particle. A name that
    fits inline gets no region entry, and then there is nowhere to put the
    1-byte particle behind it -- the same reason `build_kr` has `force_redirect`.
    The escape costs no more than the run already has, so forcing them is free.
    """
    tr = IC.load(fid)
    spans = {i: (s, e) for s, e, i in U.fat_files(bytes(rom))}
    lo, hi = spans[fid]
    jm = josa_map(fid)
    pri_lo = _pristine_lo(fid)
    out = []
    for off, text, ccs in EC.orig_runs(rom, lo, hi):
        ko = tr.get(text)
        if ko is None:
            continue
        budget = sum(1 if cc < 231 else 2 for cc in ccs)
        if budget < MIN_BUDGET:
            continue
        try:
            kb = enc.encode(ko)
        except KeyError:
            continue
        # the josa map is keyed by PRISTINE text offsets
        jo = jm.get(off + 3 - lo + pri_lo)
        if len(kb) <= budget and not jo:
            continue                    # insert_common writes this one inline
        out.append((off + 3, budget, text, ko, jo))
    out += [(o, b, j, k, None) for o, b, j, k in
            _extra_rows(rom, fid, enc, lo, {o for o, _b, _j, _k, _x in out})]

    # ⛔ The walk above reads the LIVE ROM, so it only ever sees runs that are
    # STILL JAPANESE -- i.e. the ones an earlier pass could not fit inline. A
    # name whose Korean fits was already overwritten, so it is invisible here,
    # and measured that is 69 of file 4's 70 absorbable sites: without this
    # second source the whole pass writes nothing (v184 did exactly that).
    # Force those through the region so the particle has an entry to ride in.
    seen = {o for o, _b, _j, _k, _x in out}
    for toff, (pko, q, name, blen, ko) in jm.items():
        live = toff - pri_lo + lo
        if live in seen or blen < MIN_BUDGET or not ko:
            continue
        try:
            enc.encode(ko)
            enc.encode(pko)
        except KeyError:
            continue
        out.append((live, blen, name, ko, (pko, q)))
    return out, lo


def _pristine_lo(fid):
    pri = open(EC.ORIG, "rb").read()
    fat = int.from_bytes(pri[0x48:0x4C], "little")
    return int.from_bytes(pri[fat + fid * 8:fat + fid * 8 + 4], "little")


# `PPKP9_NO_SIDE_EXTRA=1` drops the second source for A/B work.
EXTRA_SOURCE = os.environ.get("PPKP9_NO_SIDE_EXTRA") != "1"


def _extra_rows(rom, fid, enc, lo, taken):
    """The same job, for the OTHER worklist: `survey/common/file<fid>_extra.tsv`.

    ⭐ SESSION 41. `plan` above only ever read `file<fid>_runs.tsv`, so the rows
    that reach the ROM by OFFSET (`insert_extra`) had no redirect path at all in
    files 4 and 27 -- `insert_extra` is inline-only and simply drops anything
    whose Korean is longer than its run. That is a translation-quality tax, not
    just a coverage number: it forces the Korean to be cut down to the Japanese
    line's byte count, and the project's rule is to drop the less important
    CONTENT rather than the particles and endings. `tail_region` already feeds
    file 30's region from this worklist; this is the same wiring for 4 and 27.

    ⛔ The worklist's offsets are PRISTINE-ROM offsets and this pass runs after
    `insert_pointered` has relocated the file, so they are rebased through the
    live FAT here -- the mistake `insert_extra.rebase` and `tail_region.
    pristine_lo` both exist to prevent.
    ⛔ Every row is held to the same gate `insert_extra` uses: the live bytes must
    still re-encode to the recorded Japanese. That is what keeps this from
    writing an escape over a run another pass already rewrote (and it is why
    offsets `plan` already claimed are excluded outright).
    """
    if not EXTRA_SOURCE:
        return []
    import insert_extra as IX
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                     "survey", "common", f"file{fid}_extra.tsv")
    if not os.path.exists(p):
        return []
    delta = lo - IX._fat_lo(open(EC.ORIG, "rb").read(), fid)
    out = []
    for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
        f = ln.split("\t")
        if len(f) < 6 or not f[5].strip():
            continue
        poff = int(f[0], 16)
        off, budget, jp, ko = poff + delta, int(f[1]), f[4], f[5].strip()
        if off in taken or budget < MIN_BUDGET:
            continue
        # Same control-flow guard `insert_extra.apply_all` applies to its
        # inline writes: a worklist row extracted with the pre-reanalysis
        # width table can START on an opcode's marker/operand byte, and the
        # live-bytes gate below cannot see that (the pristine marker bytes DO
        # re-encode to the recorded Japanese). Writing the escape there would
        # clobber the engine marker itself.
        if IX.hits_opcode(fid, poff, budget):
            continue
        try:
            kb = enc.encode(ko)
        except KeyError:
            continue
        if len(kb) <= budget:
            continue                    # insert_extra writes this one inline
        want = IX.encode_jp(jp)
        if bytes(rom[off:off + len(want)]) != want:
            continue                    # the run drifted or is already patched
        out.append((off, budget, jp, ko))
    return out


def build(rom, fid, enc):
    """(region bytes, [(text offset, escape bytes, budget)], stats)."""
    items, lo = plan(rom, fid, enc)
    info = _overlay_of(rom, fid)
    if info is None:
        raise SystemExit(f"FAT[{fid}] has no overlay-table entry")
    ov_ram = info
    # ⭐ SESSION 39 -- TWO PASSES, because the long escape now carries the
    # entry's OFFSET rather than an index, and the offset is only known once the
    # region has been laid out. Pass 1 picks the entries and orders them so every
    # index-carrying form (tiny, banked) comes first; the table is sized to that
    # prefix and the long-form entries cost no table slot at all.
    items = sorted(items, key=lambda it: 0 if it[1] < R.LONG_BUDGET else 1)
    entries, chosen, blanks = [], [], []
    n_short = 0
    for off, budget, jp, ko, jo in items:
        idx = len(entries)
        si = R.safe_index(idx)
        if budget < R.LONG_BUDGET:
            if si >= R.SHORT_CAPACITY:
                continue                # banked space exhausted; stays Japanese
            n_short += 1
        # The absorbed particle rides at the END of the entry, so the engine
        # draws 「이름」+「은」 and then resumes past the (blanked) script byte.
        tail = b""
        if jo:
            try:
                tail = enc.encode(jo[0])
            except KeyError:
                jo = None
        # The return address is where THIS occurrence resumes: the byte just past
        # its run, in the shared overlay RAM window.
        entries.append((enc.encode(ko) + tail, ov_ram + (off - lo) + budget))
        chosen.append((off, budget, si))
        if jo:
            # keyed by the chosen index: only entries that survive into `writes`
            # may blank their particle (see the filter below)
            blanks.append((len(chosen) - 1, jo[1] - _pristine_lo(fid) + lo))
    n_indexed = sum(1 for _o, b, _s in chosen if b < R.LONG_BUDGET)
    region, offs = R.build_region(entries, n_indexed, R.REGION_BASE)

    writes, midx = [], []
    for k, (off, budget, si) in enumerate(chosen):
        esc = R.escape_bytes(si, budget, offs[k])
        if len(esc) > budget:
            continue                    # cannot fit any form; stays Japanese
        writes.append((off, esc, budget))
        midx.append(k)
    # A manifest, for the same reason overlay 28 keeps one: a gate that has to
    # re-derive which bytes are escapes ends up scanning for 0xF7 and mistaking
    # ordinary text in the 0xF7 charcode band for an escape (measured: 414 false
    # hits on the first attempt). The manifest says WHERE; `verify_side` still
    # resolves every one of them through the built ROM's own region bytes.
    # FILE-RELATIVE, because `expand_to` relocates the file right
    # after this and absolute offsets would all be stale.
    manifest = [{"rel": o - lo, "budget": b, "idx": midx[j]}
                for j, (o, _e, b) in enumerate(writes)]
    # Only blank a particle whose name actually kept its escape. An entry that
    # `writes` dropped (no escape form fits its budget) still shows the Japanese
    # name, and the Japanese particle is then the correct thing to leave behind.
    kept_idx = set(midx)
    blanks = [q for k, q in blanks if k in kept_idx]
    return region, writes, {"runs": len(items), "entries": len(entries),
                            "banked": n_short, "bytes": len(region),
                            "blanks": blanks, "manifest": manifest}


def _overlay_of(rom, fid):
    import expand_overlay as X
    info = X.overlay_of_file(bytes(rom), fid)
    return None if info is None else info[2]


def main():
    import koenc, json
    fid = int(sys.argv[1]) if len(sys.argv) > 1 else 27
    fontmap = {k: int(v) for k, v in json.load(
        open(os.path.join(os.path.dirname(__file__), "..", "survey", "font",
                          "kr_font_map.json"), encoding="utf-8")).items()}
    enc = koenc.Encoder({"syl": fontmap, "one": {}, "raw": {" ": "00"}})
    rom = bytearray(open(EC.ORIG, "rb").read())
    region, writes, st = build(rom, fid, enc)
    print(f"file {fid}: {st['runs']} runs need the region, {st['entries']} placed "
          f"({st['banked']} banked), region {st['bytes']:,}B")


if __name__ == "__main__":
    main()
