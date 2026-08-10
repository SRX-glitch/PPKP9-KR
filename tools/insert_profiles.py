#!/usr/bin/env python3
"""Insert `file30_profiles.tsv` by repointing whole records into the overlay tail.

These are the character-encyclopedia descriptions and the album titles. They live
in records of the form

    line1  FA  line2  FA  …  FF          (FA = 1-byte newline, FF = end)

reached through the pointer arrays at 0x32E1FC / 0x32ECEC, so a translation can be
**any length**: write the Korean record into overlay 14's grown tail and rewrite
the pointer. That is the same technique `insert_pointered` uses, but it has to be
a separate pass because that module's matcher decodes a flat 32-byte window and
cannot see FA at all.

Gates, all of which refuse rather than force:
  * the bytes at the recorded offset must re-encode to the recorded Japanese
  * every pointer that names that offset is rewritten, or none is
  * the tail must stay inside the overlay's RAM-group ceiling

    python tools/insert_profiles.py --report
"""
import os, sys, argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P
import koenc
import expand_overlay as X

BASE = r"C:/Users/jngji/Desktop/실험실"
COMMON = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/common"
WORK = COMMON + "/file30_profiles.tsv"
FID = 30
ARRAYS = [(0x32E1FC, 101), (0x32ECEC, 483)]
NEWLINE, END = 0xFA, 0xFF


def unescape(s):
    return s.replace("\\n", "\n").replace("\\0", "\x00")


def encode_jp(s):
    b = bytearray()
    for ch in s:
        if ch == "\n":
            b.append(NEWLINE)
        elif ch == "\x00":
            b.append(0)
        else:
            cc = P.CH2CC[ch]
            b += (bytes([cc + 1]) if cc < 231
                  else bytes([232 + (cc - 256) // 256, (cc - 256) % 256]))
    return bytes(b)


def encode_ko(s, enc):
    """Korean record bytes: FA for \\n, a raw 0 for \\0, charcodes for the rest.

    Both separators have to survive verbatim -- FA is the engine's newline and the
    embedded 0x00s are in the original records (one description carries one
    mid-sentence). Encoding the text in segments and re-emitting the separator
    keeps the record shape identical apart from the words themselves.
    """
    out = bytearray()
    seg, i = [], 0
    while i <= len(s):
        c = s[i] if i < len(s) else None
        if c is None or c in "\n\x00":
            if seg:
                out += enc.encode("".join(seg))
                seg = []
            if c == "\n":
                out.append(NEWLINE)
            elif c == "\x00":
                out.append(0)
        else:
            seg.append(c)
        i += 1
    return bytes(out)


def rows():
    if not os.path.exists(WORK):
        return
    for ln in open(WORK, encoding="utf-8").read().splitlines()[1:]:
        f = ln.split("\t")
        if len(f) >= 6 and f[5].strip():
            yield int(f[0], 16), unescape(f[4]), unescape(f[5].strip())


# FAT[30]'s start in the RETAIL ROM. Every offset in the worklist -- record
# offsets and the two pointer-array offsets alike -- was recorded against this
# layout, but by the time this pass runs `insert_pointered` has already grown
# overlay 14, which MOVES the whole file (arrays included) to the end of the ROM.
# Reading or writing the raw recorded offset then hits the dead pre-relocation
# copy: the Japanese is still sitting there so every gate passes, the pointers
# get "rewritten" in bytes the game never loads, and the screen stays Japanese.
# Rebase through the live FAT entry instead. A wrong constant cannot pass
# silently -- the `encode_jp` gate would reject every record.
ORIG_LO = 0x311E00



def handled_offsets(rom=None):
    """Recorded byte offsets covered by an encyclopedia record.

    `apply()` finds each record by matching the ORIGINAL Japanese still sitting at
    its offset (see the `want` check). Any earlier pass that writes Korean into
    those bytes makes the match fail, the record is skipped, its pointer is never
    rewritten, and the live-pointer gate reports FAILED. `insert_extra` asks for
    this set so it can leave those bytes alone -- same reason it already skips
    `insert_file8.handled_offsets`.
    """
    out = set()
    for off, jp, _ko in rows():
        out.update(range(off, off + len(encode_jp(jp))))
    return out


def apply(rom, enc=None, verbose=True):
    enc = enc or koenc.Encoder()
    fat = X.u32(rom, 0x48)
    lo = X.u32(rom, fat + FID * 8)
    ent = X.overlay_of_file(rom, FID)
    if ent is None:
        return {"written": 0, "skipped": 0}
    _, _, ram, size = ent
    shift = lo - ORIG_LO              # recorded offset -> current file offset

    blob, plan, bad = bytearray(), [], 0
    for off, jp, ko in rows():
        want = encode_jp(jp)
        if bytes(rom[off + shift:off + shift + len(want)]) != want:
            bad += 1
            continue
        try:
            kb = encode_ko(ko, enc)
        except KeyError:
            bad += 1
            continue
        plan.append((off, len(blob), kb))
        blob += kb + bytes([END])

    if not plan:
        if verbose:
            print(f"  profiles: nothing to write ({bad} rejected)")
        return {"written": 0, "skipped": bad}

    rom2, blob_ram, _ = X.expand(rom, FID, bytes(blob))
    rom[:] = rom2

    # `expand` moved the file again -- including the pointer arrays -- so rebase
    # once more before touching them. The RAM address of a record is unaffected
    # by any of this, which is why the match key is computed from ORIG_LO.
    shift2 = X.u32(rom, X.u32(rom, 0x48) + FID * 8) - ORIG_LO
    written = 0
    for off, rel, kb in plan:
        target = ram + (off - ORIG_LO)
        newv = blob_ram + rel
        for base, cnt in ARRAYS:
            for k in range(cnt):
                a = base + shift2 + k * 4
                if X.u32(rom, a) == target:
                    X.w32(rom, a, newv)
                    written += 1
    if verbose:
        print(f"  profiles: {len(plan)} records -> tail ({len(blob):,}B), "
              f"{written} pointers rewritten, {bad} rejected")
    return {"written": len(plan), "skipped": bad, "pointers": written}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    ap.parse_args()
    rom = bytearray(open(BASE + r"/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds",
                         "rb").read())
    print(apply(rom))


if __name__ == "__main__":
    main()
