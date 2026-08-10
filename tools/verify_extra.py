#!/usr/bin/env python3
"""Gate: every `file*_extra.tsv` translation is present at its LIVE offset.

Session 32 found file 25's 97 rows had been written into a dead pre-relocation
copy of overlay 28 for an entire session. Nothing caught it, because every gate
we had compares bytes at an offset *we* chose -- and the pass that chose it was
the one that was wrong. The build cheerfully printed "97 written".

This gate starts from the BUILT ROM's own FAT instead: read FAT[fid], work out
how far the file has moved since the pristine ROM, and compare the Korean bytes
where the game will actually read them. It is the `verify_profiles.py` idea
applied to the inline path.

⚠ Use a PLAIN encoder (no MTE): `insert_extra` writes with `enc_plain`, and the
MTE dictionary yields different bytes for the same text, so a good build would
read as broken. (Same trap `verify_profiles` documents.)

    python tools/verify_extra.py <built.nds>
"""
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import insert_extra as IX
import koenc

BASE = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"
FONTDIR = BASE + "/survey/font"


def _repadded():
    try:
        import strip_quote as SQ
        return SQ.repadded()
    except Exception:
        return set()


def fat_lo(rom, fid):
    fat = int.from_bytes(rom[0x48:0x4C], "little")
    return int.from_bytes(rom[fat + fid * 8:fat + fid * 8 + 4], "little")


def check(path, files=IX.SHIP, enc=None, verbose=True):
    if enc is None:
        fontmap = {k: int(v) for k, v in
                   json.load(open(os.path.join(FONTDIR, "kr_font_map.json"),
                                  encoding="utf-8")).items()}
        enc = koenc.Encoder({"syl": fontmap, "one": {}, "raw": {" ": "00"}})
    built = open(path, "rb").read()
    pristine = open(IX.ORIG, "rb").read()
    ok = bad = 0

    def _redirected(fid):
        """File-relative offsets `side_region` turned into a redirect escape.

        ⭐ SESSION 43. The josa absorption forces a NAME that already fits inline
        through the region, so the bytes at its offset are an escape, not the
        Korean this gate expects. The manifest is the authority on which
        offsets those are -- `verify_side` proves each of them resolves.
        """
        p = os.path.join(BASE, "survey", f"side_manifest_{fid}.json")
        try:
            return {e["rel"] for e in json.load(open(p, encoding="utf-8"))}
        except Exception:
            return set()

    for fid in files:
        delta = fat_lo(built, fid) - fat_lo(pristine, fid)
        pri_lo = fat_lo(pristine, fid)
        redirected = _redirected(fid)
        for off, budget, jp, ko in IX.rows(fid):
            # Same control-flow rule as every writer (insert_extra.apply_all,
            # side_region, tail_region): a row that overlaps an opcode byte
            # under the canonical width table is never written -- it is a
            # misaligned duplicate of a clean run (the doubled-kana rows,
            # RESUME §3b-0), so its span may legitimately hold the clean run's
            # redirect escape. Counting it here made a correct build read as
            # 31 failures.
            if IX.hits_opcode(fid, off, budget):
                continue
            if (off - pri_lo) in redirected:
                continue                # ships as a redirect; verify_side owns it
            b = enc.encode(ko)
            if len(b) > budget:
                continue                    # never written; reported by the build
            # Same padding rule as insert_extra: the FF-terminated tables get
            # 0xFF filler so the renderer stops (session 34 -- 0x00 filler let
            # it read past the run and flood the screen).
            if IX.needs_exact(fid, off):
                if len(b) != budget:
                    continue        # never written: exact length required
                want = b
            else:
                want = b + b"\x00" * (budget - len(b))
            # The map's destination names are the one exception: `strip_quote`
            # moves their filler to the FRONT so the Korean closes up against the
            # particle that follows (「구장에 간다」, not 「구장 에 간다」). Named by
            # offset, so every other row keeps the strict rule.
            if (fid, off) in _repadded():
                want = b"\x00" * (budget - len(b)) + b
            if bytes(built[off + delta:off + delta + budget]) == want:
                ok += 1
            else:
                bad += 1
                if bad <= 5 and verbose:
                    print(f"  extra verify MISS f{fid} 0x{off:06X}"
                          f"(+{delta:#x}) {jp!r} -> {ko!r}")
    if verbose:
        print(f"{os.path.basename(path)}: {ok}/{ok + bad} extra-worklist rows "
              f"readable at their LIVE offset")
    return ok, bad


if __name__ == "__main__":
    o, b = check(sys.argv[1] if len(sys.argv) > 1
                 else r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/builds/PPKP9_kr.nds")
    sys.exit(1 if b else 0)
