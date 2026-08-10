#!/usr/bin/env python3
"""Drop the 『 that opens a map-destination record, to buy one byte for the Korean.

Why this exists
---------------
The town-map line is one shared 7-byte run reached from seven records:

    d9 │ f8 5a 03 │ <name bytes> │ f8 5a 01 │ da 16 eb 81 07 1f 0d │ ff
    『  │ 이름 강조 시작 │ グラウンド 등 │ 강조 끝     │ **』に行きます = 우리 7B** │ 체인 구분자

Seven byte-identical runs, so the Korean has to be the same in all of them, and
the 0xFF chain delimiter sits immediately after -- there is nowhere to grow. With
the closing 』 inside our span the best that fits is 「』에간다」 (7B); the version
with a space, 「』에 간다」, is 8B. One byte short.

The 『 is the byte that pays for it. Drop the pair and the run becomes 「에 간다」
(에 2B + 0x00 1B + 간 2B + 다 2B = exactly 7B), which is better Korean than the
bracketed form anyway -- and the name keeps the `F8 5A 03/01` emphasis that
brackets it a second time, so nothing is lost visually.

    『상점가』에간다   ->   상점가에 간다

The closing 』 goes away by itself (it is the first byte of our run, so the
translation simply omits it). This pass removes the opening 『, which lives
OUTSIDE any worklist run -- a one-byte charcode the text walker never yields,
because it requires len >= 2.

Safety
------
* 0x00 is written, not a deletion: nothing moves, the record keeps its length and
  the 0xFF chain is untouched. The engine's zero path clears one 4px column, and
  the original script already carries in-stream 0x00 (see insert_common), so the
  line just starts with a hair of blank.
* The 『 is located by the exact `d9 f8 5a 03` signature immediately before the
  name, NOT by scanning back to the previous 0xFF -- 0xFF is also the low byte of
  a two-byte charcode, and that naive walk lands mid-record (measured: 「喫茶店」's
  record start came out as 「茶店」).
* COUPLED TO THE TRANSLATION. If the worklist's Korean still contains 』 this pass
  does nothing, so reverting the translation reverts the bracket with it and the
  ROM can never end up with a 『 that has no 』.

    python tools/strip_quote.py --report
"""
import argparse, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import insert_extra as IX
import walk_file as W

OPEN_Q = 0xD9                   # 『
BLANK = 0x00                    # the narrow 4px blank the engine already uses
NAME_ON = bytes([0xF8, 0x5A, 0x03])
NAME_OFF = bytes([0xF8, 0x5A, 0x01])
# (file id, the Japanese run whose Korean drops the closing 』)
TARGETS = ((20, "』に行きます"),)


def _find_open_quote(rom, run):
    """Offset of the 『 that opens `run`'s record, or None if the shape differs."""
    if bytes(rom[run - len(NAME_OFF):run]) != NAME_OFF:
        return None
    # The name sits between the two opcodes; it is short, but bound the search so
    # a malformed record can never reach into the previous one.
    for i in range(run - len(NAME_OFF) - len(NAME_ON), run - 40, -1):
        if bytes(rom[i:i + len(NAME_ON)]) == NAME_ON:
            return i - 1 if rom[i - 1] == OPEN_Q else None
    return None


def plan(rom):
    """[(live 『 offset, name start, name end, fid, jp)] per record to tidy."""
    out = []
    for fid, jp in TARGETS:
        ko = {j: k for _o, _b, j, k in IX.rows(fid)}.get(jp)
        if ko is None or "』" in ko:
            continue            # translation still carries the bracket: leave both
        delta = IX.rebase(rom, fid)
        for off, _blen, t, _ko in IX.sites(fid):
            if t != jp:
                continue
            q = _find_open_quote(rom, off + delta)
            if q is not None:
                out.append((q, q + 1 + len(NAME_ON), off + delta - len(NAME_OFF),
                            fid, jp))
    return out


def apply_all(rom, verbose=True):
    """Blank the 『 and push the destination name's padding to the LEFT.

    ⚠ The padding move is not cosmetic pedantry, it is the whole point. The name
    is its own run and `insert_extra` pads what it does not fill with trailing
    0x00 -- 「구장」(4B) in グラウンド's 5B, 「찻집」(4B) in 喫茶店's 6B. With the
    bracket gone that padding lands between the noun and the particle and the map
    reads 「구장 에 간다」, with a gap that changes width per destination (0 for
    상점가, 1 for 구장, 2 for 찻집). Moving it in front of the name turns it into a
    small left indent instead, and the Korean closes up: 「구장에 간다」.
    """
    n = pad = 0
    for q, ns, ne, _fid, _jp in plan(rom):
        rom[q] = BLANK
        name = bytes(rom[ns:ne]).rstrip(b"\x00")
        if len(name) < ne - ns:
            rom[ns:ne] = b"\x00" * (ne - ns - len(name)) + name
            pad += 1
        n += 1
    if verbose and n:
        print(f"  map records: {n} opening 『 blanked (the Korean dropped 』), "
              f"{pad} destination names re-padded on the left")
    return {"written": n}


_repad = None


def repadded():
    """{(fid, PRISTINE offset of a name run this pass left-pads)}.

    `verify_extra` gates every worklist row on `ko + 0x00 filler` sitting exactly
    at its offset. These runs are the one place where the build deliberately
    writes `0x00 filler + ko` instead, so the gate has to be told which ones --
    told precisely, by offset, rather than by relaxing the rule for all 10,984.
    Derived from the pristine ROM so it does not depend on build order.
    """
    global _repad
    if _repad is None:
        _repad = set()
        pristine = open(IX.ORIG, "rb").read()
        for fid, jp in TARGETS:
            ko = {j: k for _o, _b, j, k in IX.rows(fid)}.get(jp)
            if ko is None or "』" in ko:
                continue
            for off, _blen, t, _ko in IX.sites(fid):
                if t != jp:
                    continue
                q = _find_open_quote(pristine, off)
                if q is not None:
                    _repad.add((fid, q + 1 + len(NAME_ON)))
    return _repad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    ap.parse_args()
    rom = bytearray(open(W.ORIG, "rb").read())
    for q, fid, jp in plan(rom):
        print(f"  file {fid} 0x{q:07X}  『 before {jp}")
    print(apply_all(rom))


if __name__ == "__main__":
    main()
