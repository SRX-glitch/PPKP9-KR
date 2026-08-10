#!/usr/bin/env python3
"""How much of the BUILT ROM still draws a Japanese glyph?

Why this number matters
-----------------------
The patch does not replace the Japanese script, it overlays Korean on top of it:
a run that fits is rewritten in place, a run that does not gets a redirect
escape, and anything the byte budget or the region cap cannot reach simply stays
Japanese. That fallback is the design working correctly -- but it means the
build's completeness is invisible. `PPKP9_REGION_CAP` moves it by thousands of
sites and nothing reports the change.

It is also the entry condition for the one milestone that would end the byte
budget for good. Dropping the Japanese glyphs entirely frees the 165 kana
ONE-BYTE codes; the top 165 syllables cover ~77% of all Hangul occurrences, so
the script would shrink by roughly 280 KB -- more than ten times what the
offset-table u32->u24 change saves. That switch is all-or-nothing: every site
still drawing a Japanese glyph becomes tile garbage the moment the glyphs go.
So the milestone is exactly "this number reaches zero", and until something
counts it, nobody can tell how far away that is.

    japanese left   a site whose charcode still maps to a Japanese character AND
                    whose glyph we did NOT reassign -- these break if the
                    Japanese glyphs are dropped
    hangul on IME   a site inside overlay 13's kanji-input dictionary whose
                    charcode we DID reassign -- the player sees Hangul in the
                    name-entry 漢字 candidate list. Accepted cost of reclaiming
                    those slots; goes away when the 漢字/変換 tabs are disabled.

    python tools/japanese_left.py <built.nds>
    python tools/japanese_left.py <built.nds> --sample 20
"""
import os, sys, json, argparse, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P
import rom_census as R

PROJ = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"
FONT = PROJ + "/survey/font"


def is_japanese(ch):
    if not ch:
        return False
    o = ord(ch)
    # kana and kanji only. Fullwidth latin, digits and punctuation stay whatever
    # they are -- the patch keeps drawing them and they are not "Japanese text".
    return 0x3040 <= o <= 0x30FF or 0x4E00 <= o <= 0x9FFF or 0xFF66 <= o <= 0xFF9D


def reassigned():
    """charcodes whose glyph is no longer the Japanese character poketbl names."""
    m = json.load(open(f"{FONT}/kr_map.json", encoding="utf-8"))
    out = set(m.get("syl", {}).values()) | set(m.get("mte", {}).values())
    import redirect_hook as RH
    out |= {RH.ESC_CC, RH.RET_CC}
    out |= set(range(RH.BANK0_CC, RH.BANK0_CC + RH.BANK_COUNT))
    return out


def ime_spans(rom):
    """byte spans of the kanji-input dictionary in the ROM being measured."""
    spans = []
    for tag, lo, hi in rom.code_regions():
        if hi > lo:
            R.src_ime(rom, lo, hi, lambda *a: None, spans)
    return spans


def _tiny_table(rom):
    """The built ROM's tiny-escape table, or None on the pristine ROM."""
    try:
        import redirect_hook as RH
        import verify_escapes as VE
        off = RH.ram2rom(RH.TINY_TBL)
        t = rom.b[off:off + 256]
        return (t, VE.engine_decode) if len(t) == 256 else (None, None)
    except Exception:
        return (None, None)


def _skip_escapes(rom):
    """Byte spans occupied by OUR redirect escapes, which must not be decoded.

    ⛔ Without this the metric counts its own patch. A redirect writes
    `F7 <b2> <payload>` into the run, and the payload bytes are an offset, not
    text -- but a text walker happily decodes them, and `F7` itself decodes to
    halfwidth katakana. Measured on v147 that produced runs like 「ｳむそ」 and
    「茜瑛蛾」 which the breakdown then filed as "untranslated Japanese". The
    engine never draws any of it: the hook consumes the escape and jumps to the
    region. So walk the way `verify_escapes` proves the engine dispatches, and
    skip what it consumes.
    """
    tiny, decode = _tiny_table(rom)
    if tiny is None:
        return set()
    import redirect_hook as RH
    out, b = set(), rom.b
    for tag, lo, hi in rom.code_regions():
        i = lo
        while i < hi - 5:
            j = b.find(bytes([RH.ESC_B1]), i, hi - 5)
            if j < 0:
                break
            got = decode(b, tiny, j)
            if got:
                out.update(range(j, j + got[2]))
                i = j + got[2]
            else:
                i = j + 1
    return out


def measure(path):
    """-> (jp Counter, jp_where Counter, han_ime Counter, samples, rom)"""
    rom = R.Rom(path)
    keep = reassigned()
    ime = ime_spans(rom)
    esc = _skip_escapes(rom)

    def in_ime(off):
        return any(s <= off < e for s, e in ime)

    jp, jp_where, han_ime = collections.Counter(), collections.Counter(), collections.Counter()
    samples = collections.defaultdict(list)

    def hit(cc, source, off, text):
        ch = P.CC2CH.get(cc)
        if cc in keep:
            if source == "ime" or in_ime(off):
                han_ime[cc] += 1
            return
        if off in esc:
            return                      # our own escape payload, never drawn
        if not is_japanese(ch):
            return
        jp[cc] += 1
        owner = rom.owner(off)
        jp_where[(owner, source)] += 1
        if len(samples[(owner, source)]) < 4:
            samples[(owner, source)].append((off, text))

    for _tag, lo, hi in rom.code_regions():
        if hi <= lo:
            continue
        skip = R.src_ime(rom, lo, hi, hit)
        R.src_dialogue(rom, lo, hi, hit)
        R.src_array(rom, lo, hi, hit, None, skip)
        R.src_packed(rom, lo, hi, hit, None, skip)
    return jp, jp_where, han_ime, samples, rom


def baseline():
    """Same measurement on the pristine ROM, cached -- it never changes."""
    path = f"{FONT}/japanese_baseline.json"
    if os.path.exists(path):
        d = json.load(open(path))
        return d["total"], {tuple(k.split("/", 1)): v for k, v in d["by"].items()}
    jp, jp_where, _h, _s, _r = measure(R.ORIG)
    d = {"total": sum(jp.values()),
         "by": {f"{o}/{s}": n for (o, s), n in jp_where.items()}}
    json.dump(d, open(path, "w"), indent=1)
    return d["total"], jp_where


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rom")
    ap.add_argument("--sample", type=int, default=0)
    a = ap.parse_args()

    # ⛔ main() used to carry its OWN copy of the walk, and that copy never
    # applied the escape skip -- so the standalone tool and the build gate
    # reported different numbers for the same ROM. One implementation only.
    jp, jp_where, han_ime, samples, rom = measure(a.rom)

    base_total, base_by = baseline()
    left = sum(jp.values())
    done = base_total - left
    print(f"=== {os.path.basename(a.rom)} ===")
    print(f"JAPANESE LEFT: {left:,} of {base_total:,} occurrences "
          f"({done / base_total * 100:.1f}% replaced), {len(jp)} distinct charcodes")
    print("  (this must reach 0 before the Japanese glyphs can be dropped)")
    for (owner, source), n in jp_where.most_common(12):
        b = base_by.get((owner, source), 0)
        pct = f"{(b - n) / b * 100:5.1f}% done" if b else "   -"
        print(f"    {owner:>6} {source:<9} {n:7,} of {b:7,}  {pct}")
        for off, t in samples[(owner, source)][:a.sample]:
            print(f"          0x{off:06X}  {t[:44]}")
    print(f"\nHANGUL ON THE KANJI IME: {sum(han_ime.values()):,} occurrences, "
          f"{len(han_ime)} distinct")
    print("  (name-entry 漢字 candidates showing Hangul; 0 once the tab is disabled)")
    top = [f"{P.CC2CH.get(c, '?')}x{n}" for c, n in han_ime.most_common(10)]
    if top:
        print("    most drawn: " + " ".join(top))

    out = {"rom": os.path.basename(a.rom),
           "japanese_occurrences": sum(jp.values()),
           "japanese_distinct": len(jp),
           "hangul_on_ime_occurrences": sum(han_ime.values()),
           "by_owner_source": {f"{o}/{s}": n for (o, s), n in jp_where.items()}}
    json.dump(out, open(f"{FONT}/japanese_left.json", "w"), indent=1)
    print(f"\nwrote {FONT}/japanese_left.json")


if __name__ == "__main__":
    main()
