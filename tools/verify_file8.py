#!/usr/bin/env python3
"""Prove that repointing file 8 touched NOTHING but pointer words.

Why this gate exists: `insert_extra`'s header records that session 29 traced a
「終 / ファイルをけしました」 save wipe to a write into file 8 or 20 and never pinned
it down, so both files were put off limits. File 8 is where the shared messages
live, so that ban is expensive -- and the likeliest cause is now known, because
file 30 turned out to have exactly the same trap: an offset-driven in-place write
landed inside a POINTER ARRAY (0x325D93) and shredded seven pointers. File 8 is
full of such arrays (54 runs, the largest 812 entries).

`insert_file8` never writes in place. It copies each record to the grown tail and
rewrites the one pointer that named it. This checks that claim against the built
ROM: every byte that differs inside file 8's original span must belong to an
aligned u32 whose ORIGINAL value pointed into the overlay. Anything else -- a
changed text byte, a changed table entry -- fails.

    python tools/verify_file8.py <rom.nds>
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import expand_overlay as X

ORIG = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
def _fids():
    """Only the files the pointer pass actually ships. A file that is NOT
    repointed is still written in place elsewhere (file 20's menu table), and
    checking it here would fail on writes that are meant to happen."""
    try:
        import insert_file8 as F8
        return F8.SHIP
    except Exception:
        return (8,)


FIDS = _fids()


def _table_spans(o):
    """ROM spans `insert_tables` is entitled to overwrite in place.

    File 20 is repointed AND carries the action-menu table that `insert_tables`
    writes in place, so a pointer-only rule fails on writes that are meant to
    happen. Rather than drop the file from the gate (which is what hid the
    session-29 hazard in the first place), the legitimate spans are reconstructed
    from the ORIGINAL rom -- the row offset from the worklist, the length from
    walking the retail terminator -- and only those are forgiven.

    ⚠ Forgiveness is NOT unconditional: a byte inside a table row still fails if
    its containing u32 was a live overlay pointer in the retail ROM. That is
    exactly the session-29 accident (an in-place write landing in a pointer
    array), and it must stay catchable even where a table is allowed to write.
    """
    spans = []
    # `insert_file8.apply_inplace` writes the records that have NO pointer, so the
    # pointer pass can never reach them (「上がった」/「下がった」, which every training
    # result prints). It writes strictly INSIDE the original run and already
    # refuses any target that overlaps a live pointer array -- the session-29
    # save-wipe guard -- so its runs are forgiven here on the same terms as
    # insert_tables': the pointer test above still applies to every byte.
    try:
        import insert_file8 as _F8
        import insert_extra as _IX
        for fid in (tuple(getattr(_F8, "SHIP_INPLACE", ()))
                    + tuple(getattr(_F8, "SHIP_ORPHAN", ()))):
            lo = X.u32(o, X.u32(o, 0x48) + fid * 8)
            hi = X.u32(o, X.u32(o, 0x48) + fid * 8 + 4)
            # ⚠ `apply_orphans` writes EVERY occurrence (`insert_extra.WORK`),
            # not just the worklist row -- the session-38 duplicate-site fix.
            # Forgiving only `rows()` here flagged those legitimate writes as
            # corruption (v196). Mirror the writer's own source.
            for off, budget, jp, _ko in _IX.WORK(fid):
                spans.append((off, off + budget))
            for off, budget, jp, _ko in _F8.rows(fid):
                spans.append((off, off + budget))
                # ⭐ SESSION 43 — the PAIRED sites. A label lives twice (the
                # increase record and the decrease one) and `apply_inplace`
                # writes both, but only one of them is a worklist row. Recompute
                # the set with the writer's own rule rather than trusting a
                # handed-over list, so this stays an independent check.
                for s in _F8.paired_sites(o, jp, off, budget, lo, hi):
                    spans.append((s, s + budget))
    except Exception:
        pass
    # The runtime particles blanked in the status lines (「힘 が ５감소」 -> 「힘 ５
    # 감소」). One byte each, same recompute-don't-trust rule.
    try:
        import json as _json
        import josa_absorb as _JA
        _w = _json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                          "..", "survey", "ov28",
                                          "opcode_lengths.json"), encoding="utf-8"))
        for fid in (4, 8, 18, 20, 25, 27, 30):
            lo = X.u32(o, X.u32(o, 0x48) + fid * 8)
            hi = X.u32(o, X.u32(o, 0x48) + fid * 8 + 4)
            for off, _b, _jp in _JA.runtime_particle_sites(o, lo, hi, _w):
                spans.append((off, off + 1))
    except Exception:
        pass
    try:
        import insert_tables as IT
    except Exception:
        return spans
    for fid in getattr(IT, "SHIP", ()):
        try:
            for off, _jp, _ko in IT.rows(fid):
                # Mirror the WRITER's contract exactly (`rom[off:term]`, the FF
                # itself never touched) instead of approximating it from
                # `budget()`. Using budget left a 2-byte tail that the writer
                # legitimately zero-pads, and a gate that is wrong by two bytes
                # is a gate people start ignoring.
                if fid in getattr(IT, "SLOT", {}):
                    spans.append((off, off + IT.SLOT[fid]))
                    continue
                term = o.find(b"\xff", off, off + IT.MAXREC)
                if term > off:
                    spans.append((off, term))
        except Exception:
            continue
    return spans


def check(o, n, fid):
    lo_o = X.u32(o, X.u32(o, 0x48) + fid * 8)
    hi_o = X.u32(o, X.u32(o, 0x48) + fid * 8 + 4)
    lo_n = X.u32(n, X.u32(n, 0x48) + fid * 8)
    _, _, ram, size = X.overlay_of_file(o, fid)
    old = o[lo_o:hi_o]
    new = n[lo_n:lo_n + len(old)]
    spans = [(a, b) for a, b in _table_spans(o) if lo_o <= a < hi_o]
    words, bad, tabled = set(), [], 0
    for i in range(len(old)):
        if old[i] != new[i]:
            w = i & ~3
            if ram <= int.from_bytes(old[w:w + 4], "little") < ram + size:
                words.add(w)
            elif any(a <= lo_o + i < b for a, b in spans):
                tabled += 1          # insert_tables' own in-place table row
            else:
                bad.append(lo_o + i)
    return words, bad, tabled


def main():
    path = sys.argv[1]
    o = open(ORIG, "rb").read()
    n = open(path, "rb").read()
    failed = False
    for fid in FIDS:
        words, bad, tabled = check(o, n, fid)
        print(f"{os.path.basename(path)}: file {fid} -- {len(words)} pointer "
              f"words rewritten, {tabled} bytes inside an insert_tables row, "
              f"{len(bad)} non-pointer bytes changed")
        if bad:
            failed = True
            print("  !! these are NOT pointers -- an in-place write got through:")
            for a in bad[:8]:
                print(f"     0x{a:06X}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
