#!/usr/bin/env python3
"""Overlay-28 name-insert runs that `dialogue_runs.tsv` never captured.

Why they are missing
--------------------
`extract_all.py` builds the overlay-28 corpus behind an `in_dialogue` gate: a run
only counts once an `F8 6B` message opener has been seen. A name pushed into a
sentence with `F8 08 <name> F8 09` from outside a message therefore never entered
the corpus, so the redirect pipeline never saw it -- and `extract_extra.py` did
not pick it up either, because it skips anything the batch corpus already
translates (「ビクトリーズ」 is in batch39). Between the two gates the run fell
through completely.

What the player sees is the session-38 bug report: Korean dialogue with a
Japanese name sitting in the middle of it.

    [F808]ビクトリーズ[F809]야구 한다면
    [F808]ビクトリーズ[F809]이겼는데！

Measured on the pristine ROM: 35 such runs, every one still Japanese in v133.
16 fit inline; the other 19 need the escape -- 「ちよ」→「치요」 is 4 bytes in a
2-byte slot, 「カンタ」→「칸타」 4 in 3, 「ビクトリーズ」→「빅토리즈」 8 in 6.

Why this is cheap
-----------------
They are in overlay 28, so the region and all three escape forms are already
there: budget 2 rides the tiny escape, 3 the banked one, 4+ the long one. The
bodies cost about 400 bytes of a region that has 16,713 bytes of slack inside the
current grow, so nothing has to grow and no hook changes.

Offsets are OVERLAY-RELATIVE, matching `dialogue_runs.tsv` -- build_kr's `lines`
list is in that space and every downstream check (`in_choice`, the region
allocator, the text gate) assumes it.

    python tools/extract_names.py            # report
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import walk_file as W
import poketbl as P

FID = 25                    # overlay 28
OPENER = b"\xf8\x08"
CLOSER = b"\xf8\x09"


def corpus_spans(lo):
    """Byte offsets some OTHER pass already claims, in absolute ROM space.

    Two owners, and missing either one causes a real failure:
      * `dialogue_runs.tsv` -- offsets are OVERLAY-RELATIVE here, hence `lo`.
      * `file25_extra.tsv`  -- absolute, and `insert_extra` writes it in place.
        ⛔ Leaving this one out is not theoretical: it shipped 19 gate failures
        (`extra verify MISS f25 0x4D1363 '』を喰った！'`) because the run was
        redirected here AND written inline there, two passes on the same bytes.
    """
    out = set()
    path = os.path.join(W.PROJ, "survey", "ov28", "dialogue_runs.tsv")
    for ln in open(path, encoding="utf-8").read().splitlines():
        p = ln.split("\t")
        if len(p) >= 4:
            o, b = lo + int(p[0], 16), int(p[1])
            out.update(range(o, o + b))
    extra = os.path.join(W.PROJ, "survey", "common", "file25_extra.tsv")
    if os.path.exists(extra):
        for ln in open(extra, encoding="utf-8").read().splitlines()[1:]:
            p = ln.split("\t")
            if len(p) >= 6 and p[5].strip():
                o, b = int(p[0], 16), int(p[1])
                out.update(range(o, o + b))
    return out


def _tail_runs(rom, lo, hi, covered):
    """Runs sitting immediately AFTER a name-insert closer `F8 09`.

    ⭐⭐ SESSION 38, from the user's screenshots: 「우리빅토리즈 は」, 「곤다 마사오） だ、」.
    The name went Korean and the particle behind it did not. Those runs are 1-3
    bytes, and every census this session was blind to them -- `extract_extra`
    defaults to --min-budget 3 and `walk_file.looks_like_text` needs len >= 2 and
    two JP characters, so a bare 「は」 is invisible to both.

    Measured across files 25/4/27/30/20: 776 sites, 238 distinct. This yields the
    overlay-28 ones, where the region makes length free for budget >= 2.

    They are walked here rather than through `W.walk` for exactly that reason:
    that walker's text filter is what hid them.
    """
    out = []
    i = lo
    while i < hi - 2:
        j = rom.find(CLOSER, i, hi)
        if j < 0:
            break
        i = j + 2
        k, ch = i, []
        while k < hi:
            c = rom[k]
            if c == 0 or c >= 0xF8:
                break
            cc, nx = P.bytes_to_cc(rom, k)
            g = P.CC2CH.get(cc)
            if g is None:
                break
            ch.append(g)
            k = nx
        if not ch or k - i < 2:
            continue            # budget 1 cannot even hold the 2-byte escape
        if any(o in covered for o in range(i, k)):
            continue
        out.append((i - lo, k - i, "".join(ch)))
    return out


def runs(rom=None):
    """[(overlay-relative offset, budget, jp)] -- the runs the corpus missed."""
    rom = rom if rom is not None else open(W.ORIG, "rb").read()
    lo, hi = W.fat_span(rom, FID)
    covered = corpus_spans(lo)
    out = []
    for tag, off, blen, t in W.walk(rom, lo, hi):
        if tag != "F808":
            continue
        # Require the exact `F8 08 <run> F8 09` shape. The tag alone is the LAST
        # opcode seen, which is not the same thing -- without this a run that
        # merely follows a name insert would be added at the wrong boundary.
        if bytes(rom[off - 2:off]) != OPENER:
            continue
        if bytes(rom[off + blen:off + blen + 2]) != CLOSER:
            continue
        if any(o in covered for o in range(off, off + blen)):
            continue
        out.append((off - lo, blen, t))
    taken = {o for o, _b, _t in out}
    out += [r for r in _tail_runs(rom, lo, hi, covered) if r[0] not in taken]
    return out


def main():
    rom = open(W.ORIG, "rb").read()
    r = runs(rom)
    print(f"name-insert runs outside the overlay-28 corpus: {len(r)}")
    import collections
    c = collections.Counter(t for _o, _b, t in r)
    for t, n in c.most_common(20):
        b = min(bb for _o, bb, tt in r if tt == t)
        print(f"   {n:3d}x  b{b:<3d} {t}")


if __name__ == "__main__":
    main()
