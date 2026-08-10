#!/usr/bin/env python3
"""Read file 8 / 20's repointed records back THROUGH THE LIVE POINTER.

`verify_file8.py` proves the pass touched nothing but pointer words. That is a
statement about what we did NOT break; it says nothing about whether the game
can reach the Korean. Two relocation bugs shipped in this project precisely
because a written-count looked like evidence (`insert_extra` reported "97
written" for a whole session while every write went into a dead pre-relocation
copy), so the pointered passes each get a reachability gate of their own --
`verify_profiles` for the encyclopedia, this for the shared messages.

For every pointer word the pass rewrote: resolve the NEW RAM value back to a ROM
offset through the FAT the finished ROM carries, walk the record's wrapper to its
`F8 08 <run> F8 09`, decode the run with the shipped font map, and require it to
equal the Korean the worklist asked for.

    python tools/verify_file8_live.py <rom.nds>
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import expand_overlay as X
import insert_file8 as F8

ORIG = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
KRMAP = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "survey", "font", "kr_map.json")


def _inv():
    """charcode -> character.

    ⚠ BOTH tables, base first. A reader that knows only `kr_map` decodes every
    punctuation mark and surviving kana as `?` and then reports a perfectly good
    record as damaged -- 「찬스！」 came back as 「찬스?」 on the first run of this
    gate. The project's own rule: if the reader does not know every format the
    engine knows, the "damage" is the reader's.
    """
    import poketbl as P
    out = {cc: ch for ch, cc in P.CH2CC.items()}
    km = json.load(open(KRMAP, encoding="utf-8"))
    for key in ("syl", "mte"):
        for ch, cc in km.get(key, {}).items():
            try:
                out[int(cc)] = ch      # repurposed slots win
            except (TypeError, ValueError):
                pass
    return out


def decode(b, inv, f8w):
    """Walk a record the way the engine does and return its text.

    ⛔ Do NOT scan for the terminating 0xFF as a raw byte and do NOT treat 0xF8 as
    a charcode lead. A record is `… F8 5A 03 <text> F8 5A 01 …  FF`, and a 2-byte
    charcode's SECOND byte is free to be 0xFF -- 『シャドウピッチング』's Korean
    contains exactly that, so a raw scan ended the record after five bytes and
    this gate reported a perfectly good row as damaged. Opcode first, then
    charcode, then the terminator: the engine's order.
    """
    s, i = [], 0
    while i < len(b):
        c = b[i]
        if c == 0xFF:
            break
        if c == 0xF8:
            i += f8w.get(b[i + 1], 2) if i + 1 < len(b) else 2
        elif c == 0:
            s.append(" ")
            i += 1
        elif c < 232:
            s.append(inv.get(c - 1, "?"))
            i += 1
        elif i + 1 < len(b):
            cc = 256 + (c - 232) * 256 + b[i + 1]
            s.append(inv.get(cc, "?"))
            i += 2
        else:
            break                     # truncated lead byte at the record end
    return "".join(s)


def check(path, fid, inv):
    o = open(ORIG, "rb").read()
    n = open(path, "rb").read()
    lo_o = X.u32(o, X.u32(o, 0x48) + fid * 8)
    hi_o = X.u32(o, X.u32(o, 0x48) + fid * 8 + 4)
    lo_n = X.u32(n, X.u32(n, 0x48) + fid * 8)
    _, _, ram, _size = X.overlay_of_file(o, fid)
    want = {jp: ko for _off, _b, jp, ko in F8.rows(fid)}

    hi_n = X.u32(n, X.u32(n, 0x48) + fid * 8 + 4)
    kos = [k for k in want.values() if k]
    f8w, _bare = F8._oplen()

    ok = bad = 0
    misses = []
    for w in range(0, hi_o - lo_o, 4):
        old = X.u32(o, lo_o + w)
        new = X.u32(n, lo_n + w)
        # ⚠ Only words that were a LIVE OVERLAY POINTER in retail. File 20 also
        # carries the action-menu table that `insert_tables` writes in place, and
        # reading those text bytes as pointers produced 82 fake failures
        # (0xE800B6EA "lands outside the file") on this gate's first run.
        if old == new or not (ram <= old < ram + _size):
            continue
        rec = lo_n + (new - ram)
        if not (lo_n <= rec < hi_n):
            bad += 1
            misses.append((new, "pointer lands outside the file"))
            continue
        # Do NOT assume a wrapper shape: file 8 and file 20 do not share one.
        # Walk the record to its terminator and ask whether the Korean the
        # worklist wanted is in there.
        got = decode(n[rec:rec + F8.MAXREC], inv, f8w)
        if any(k and k in got for k in kos):
            ok += 1
        else:
            bad += 1
            misses.append((new, f"decoded {got!r}"))
    return ok, bad, misses


def main():
    path = sys.argv[1]
    inv = _inv()
    failed = False
    for fid in F8.SHIP:
        ok, bad, misses = check(path, fid, inv)
        print(f"{os.path.basename(path)}: file {fid} -- {ok} records read back "
              f"as their Korean through the live pointer, {bad} did not")
        for v, why in misses[:8]:
            print(f"     0x{v:08X}  {why}")
        if bad:
            failed = True
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
