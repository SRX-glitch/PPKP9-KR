# -*- coding: utf-8 -*-
"""Migrate extra-worklist rows that START on an opcode byte to their clean run.

The pre-reanalysis width table had `F8 20` at 3 bytes (canonical: 2), so the
extractor's walk swallowed the following F8 lead and started runs ON the marker
bytes of double-marker opcodes (`F8 19 19` family) -- the doubled-kana rows
(「んんあやしいな。」).  A second family started one byte early on a `F9`
operand (old table walked F9 as width 1; canonical is 2).

Every writer now refuses these rows (insert_extra.hits_opcode), so their
translations stopped shipping.  This tool moves each row forward to the first
non-opcode byte, re-decodes the clean Japanese from the pristine ROM, keeps the
Korean, and rewrites the worklist row in place.  Round-trip gate: the clean
Japanese must re-encode byte-exactly to the pristine bytes it was decoded from.

    python tools/migrate_opcode_rows.py           # dry run, report only
    python tools/migrate_opcode_rows.py --apply   # rewrite file*_extra.tsv
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import insert_extra as IX
import poketbl as P

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMON = os.path.join(BASE, "survey", "common")
FILES = (4, 8, 18, 20, 25, 27, 30)

# Rows whose Korean still carries a translation of the SPURIOUS leading char
# (the translator saw the polluted extraction): fix the value while migrating.
KO_FIX = {
    (4, 0x5758E7): "고귀한 의무다。",          # was '？고귀한 의무다。' ('？' spurious)
    (4, 0x5761AB): "・・・모릅니다。",          # was '가・・・모릅니다。' ('が' spurious)
    (4, 0x576443): "태어났을 때부터、나에게",     # was '、태어났을...' ('、' spurious)
    (4, 0x5DB17E): "「호위모집！",             # was '의「호위모집！' ('の' spurious)
    (8, 0x452637): "외야수",                  # was '그대로 외야수' (prefix spurious)
}


def decode_span(rom, lo, hi):
    """Decode pristine bytes [lo, hi) as text; None if any byte is not text."""
    chars, i = [], lo
    while i < hi:
        b = rom[i]
        if b == 0 or b >= 0xF8:
            return None
        cc, nxt = P.bytes_to_cc(rom, i)
        ch = P.CC2CH.get(cc)
        if ch is None or nxt > hi:
            return None
        chars.append(ch)
        i = nxt
    return "".join(chars)


def main():
    apply = "--apply" in sys.argv
    rom = open(IX.ORIG, "rb").read()
    fixes = {}      # (fid, old_off_hex) -> (new_off, new_budget, new_jp)
    for fid in FILES:
        try:
            rows = IX.rows(fid)
        except Exception:
            continue
        lo, mask = IX.opcode_map(fid)
        for off, budget, jp, ko in rows:
            if not IX.hits_opcode(fid, off, budget):
                continue
            # first non-opcode byte at or after `off`
            k = off - lo
            end = off - lo + budget
            while k < end and mask[k]:
                k += 1
            clean = lo + k
            nb = off + budget - clean
            if nb < 2:
                print(f"  f{fid} 0x{off:06X} {jp!r}: no clean span left -- drop")
                continue
            if any(mask[k2] for k2 in range(k, end)):
                print(f"  f{fid} 0x{off:06X} {jp!r}: opcode INSIDE span -- skip")
                continue
            njp = decode_span(rom, clean, clean + nb)
            if njp is None:
                print(f"  f{fid} 0x{off:06X} {jp!r}: clean span not text -- skip")
                continue
            if IX.encode_jp(njp) != rom[clean:clean + nb]:
                print(f"  f{fid} 0x{off:06X} {njp!r}: round-trip mismatch -- skip")
                continue
            if not jp.endswith(njp):
                # the spurious prefix must be the ONLY difference
                print(f"  f{fid} 0x{off:06X} {jp!r} -> {njp!r}: not a suffix -- skip")
                continue
            fixes[(fid, off)] = (clean, nb, njp, jp, ko)
    print(f"migratable rows: {len(fixes)}")
    for (fid, off), (clean, nb, njp, jp, ko) in sorted(fixes.items()):
        print(f"  f{fid} 0x{off:06X}+b? -> 0x{clean:06X} b{nb}  {njp!r} -> {ko!r}")
    if not apply:
        print("(dry run -- use --apply to rewrite worklists)")
        return
    for fid in FILES:
        p = os.path.join(COMMON, f"file{fid}_extra.tsv")
        if not os.path.exists(p):
            continue
        lines = open(p, encoding="utf-8").read().splitlines()
        n = 0
        for i, ln in enumerate(lines):
            f = ln.split("\t")
            if len(f) < 6 or not f[0].startswith("0x"):
                continue
            key = (fid, int(f[0], 16))
            if key in fixes:
                clean, nb, njp, jp, ko = fixes[key]
                f[0] = f"0x{clean:06X}"
                f[1] = str(nb)
                f[4] = njp
                if key in KO_FIX:
                    f[5] = KO_FIX[key]
                lines[i] = "\t".join(f)
                n += 1
        if n:
            open(p, "w", encoding="utf-8", newline="\n").write(
                "\n".join(lines) + "\n")
            print(f"file{fid}_extra.tsv: {n} rows migrated")


if __name__ == "__main__":
    main()
