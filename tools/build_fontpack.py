#!/usr/bin/env python3
"""Build a clean, complete Korean font pack.

Instead of injecting only the syllables a given translation happens to use,
pre-populate the font with a large common Hangul set once, on a fixed
syllable->charcode map. Translation then just references syllables; glyphs never
need regenerating.

Target set (priority order, capped at available scenario-free <0xC00 slots):
  1. syllables already used in the current translation (guaranteed present)
  2. KS X 1001 wansung 2350 (the standard common set), in standard order
The map is written to survey/font/kr_font_map.json and consumed by koenc/build.
"""
import os, sys, json, glob, collections
sys.path.insert(0, os.path.dirname(__file__))
import mte_hook as M
import fontcodec as F

ROM = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
OUT = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font"
TRANS = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/translation"
COMMON = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/common"
# Discovered, not hardcoded: a new batchN.tsv must never be able to add
# syllables the font pack does not know about.
BATCHES = ["common_lines"] + sorted(
    (f[:-4] for f in os.listdir(TRANS)
     if f.startswith("batch") and f.endswith(".tsv")),
    key=lambda n: int(n[5:]))


def ksx1001_wansung():
    """The 2350 KS X 1001 syllables, ordered most-likely-to-be-needed first.

    EUC-KR order is alphabetical, and the pack holds fewer slots than KS X 1001
    has syllables -- so filling in that order gave every slot to 가각간갇... and
    left the tail of the alphabet out. That is not a hypothetical: 숲 춤 얗 흡
    쏴 엎 탔 all had to be worked around in the shared-file translation, and all
    of them are late-alphabet.

    Instead score each syllable by how common its three jamo are in real Korean,
    measured on this project's own 7,276 translated lines. A product of the three
    marginal frequencies is a crude model, but it is derived from actual game
    dialogue and it puts 이 그 하 는 다 first instead of 각 갇 갈.
    """
    L = [c for lead in range(0xB0, 0xC9) for trail in range(0xA1, 0xFF)
         for c in [_euckr(lead, trail)] if c]
    ini, vow, fin = collections.Counter(), collections.Counter(), collections.Counter()
    for ch, n in _corpus_syllables().items():
        i, v, f = _jamo(ch)
        ini[i] += n; vow[v] += n; fin[f] += n
    def score(ch):
        i, v, f = _jamo(ch)
        # +1 so a jamo unseen in our corpus still ranks above nothing
        return (ini[i] + 1) * (vow[v] + 1) * (fin[f] + 1)
    return sorted(L, key=score, reverse=True)


def _euckr(lead, trail):
    try:
        ch = bytes([lead, trail]).decode("euc-kr")
    except Exception:
        return None
    return ch if len(ch) == 1 and 0xAC00 <= ord(ch) <= 0xD7A3 else None


def _jamo(ch):
    n = ord(ch) - 0xAC00
    return n // 588, (n % 588) // 28, n % 28


def _corpus_syllables():
    """Syllable counts over every Korean line this project has produced."""
    c = collections.Counter()
    for pat in (os.path.join(TRANS, "*.tsv"), os.path.join(COMMON, "file*_runs.tsv")):
        for fn in glob.glob(pat):
            for ln in open(fn, encoding="utf-8").read().splitlines()[1:]:
                for ch in ln.split("\t")[-1]:
                    if 0xAC00 <= ord(ch) <= 0xD7A3:
                        c[ch] += 1
    return c


def used_syllables():
    """Every syllable any finished translation needs, most-wanted first.

    Three sources, and leaving any of them out is how the pack ends up missing
    everyday words:
      1. translation/batch*.tsv + intro -- overlay 28 (the Nice Guy script)
      2. survey/common/file*_runs.tsv  -- the shared files (4, 8, 20, 27)
      3. survey/common/font_gaps.tsv   -- syllables a translation WANTED but the
         pack could not draw, so the text had to be reworded. These are exactly
         the ones to put back, and they are invisible in 1 and 2 precisely
         because the workaround removed them.
    """
    u = {}
    order = 0

    # ⚠ ORDER IS NOT COSMETIC. The first ~1,238 syllables get charcodes that own
    # real glyph storage; everything after that lands in the EXTENSION pages
    # (0x0DC0-0x0FFF), which are only drawn by our render_char hook -- it swaps
    # the font table for one call and swaps back. Screens that do NOT go through
    # that hook (the daily action menu, and any other table renderer) therefore
    # draw an extension charcode as whatever the ORIGINAL font has at that slot:
    # 「연습한다」 came out as 「♫♫を…」 while 「설정」, whose syllables happened to get
    # non-extension codes, rendered correctly. So the tables go FIRST.
    def take(s):
        nonlocal order
        for c in s:
            if 0xAC00 <= ord(c) <= 0xD7A3 and c not in u:
                u[c] = order
                order += 1

    # TABLES FIRST -- they are rendered outside the hook, so every syllable they
    # use must land in a non-extension charcode. `*_table.tsv` (13/18/30 and the
    # daily action menu) keeps its Korean in column 5.
    for fn in sorted(glob.glob(os.path.join(COMMON, "*_table.tsv"))):
        for ln in open(fn, encoding="utf-8").read().splitlines()[1:]:
            f = ln.split("\t")
            if len(f) > 5:
                take(f[5])

    for fn in [n + ".tsv" for n in BATCHES] + ["intro_lines.tsv"]:
        p = os.path.join(TRANS, fn)
        if not os.path.exists(p):
            continue
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            cols = ln.split("\t")
            take(cols[-1] if cols else "")     # ko is the last column

    gaps = os.path.join(COMMON, "font_gaps.tsv")
    if os.path.exists(gaps):
        for ln in open(gaps, encoding="utf-8").read().splitlines()[1:]:
            f = ln.split("\t")
            if f and f[0]:
                take(f[0])                     # the syllable that was missing
                if len(f) > 4:
                    take(f[4])                 # and the wording it belonged to

    # Korean onomatopoeia, reserved AHEAD of the KS X filler.
    # Sound words are where the pack keeps coming up short: a translator reaches
    # for 「쨍그랑」 or 「후루룩」, one syllable is missing, and the line gets reworded
    # -- that is what font_gaps records 45 of. Claiming the slots up front costs
    # nothing, because the alternative occupant is generic KS X filler: of the
    # 182 syllables in this list 175 were already present, so it buys 7 slots out
    # of ~400 spare and removes the whole class of rewrite-because-of-the-font.
    # Real translations still outrank it -- this block runs after every worklist.
    sfx = os.path.join(COMMON, "sfx_syllables.tsv")
    if os.path.exists(sfx):
        for ln in open(sfx, encoding="utf-8").read().splitlines()[1:]:
            take(ln.split("\t")[0])

    # Both shapes of shared-file worklist. `*_runs.tsv` (files 4/8/20/27) puts
    # the Korean in column 3; `*_table.tsv` (13/18/30 -- ability names, ability
    # effects, the character encyclopedia) puts it in column 5. Globbing only
    # `_runs` left the encyclopedia's syllables out of the pack entirely, which
    # would have shown up as blank glyphs the moment those tables were inserted.
    for fn in sorted(glob.glob(os.path.join(COMMON, "file*_runs.tsv"))):
        for ln in open(fn, encoding="utf-8").read().splitlines()[1:]:
            f = ln.split("\t")
            if len(f) >= 4:
                take(f[3])
    # `file*_extra.tsv` (tools/extract_extra.py) -- the text the F8 6B walk never
    # saw. Its Korean lives in column 6. Leaving it out means a syllable used only
    # there gets no glyph slot, and build_kr aborts with "syllables not in font
    # pack" (「청룡방」's 룡 was the first).
    for fn in sorted(glob.glob(os.path.join(COMMON, "file*_extra.tsv"))):
        for ln in open(fn, encoding="utf-8").read().splitlines()[1:]:
            f = ln.split("\t")
            if len(f) >= 6:
                take(f[5])
    # `file*_profiles.tsv` -- the encyclopedia records (tools/extract_profiles.py).
    # Korean in column 6, with \n / \0 escapes that are not glyphs.
    for fn in sorted(glob.glob(os.path.join(COMMON, "file*_profiles.tsv"))):
        for ln in open(fn, encoding="utf-8").read().splitlines()[1:]:
            f = ln.split("\t")
            if len(f) >= 6:
                take(f[5].replace("\\n", "").replace("\\0", ""))
    for fn in sorted(glob.glob(os.path.join(COMMON, "file*_table.tsv"))):
        for ln in open(fn, encoding="utf-8").read().splitlines()[1:]:
            f = ln.split("\t")
            if len(f) >= 6:
                take(f[5])
    return list(u)


def main():
    rom = open(ROM, "rb").read()
    tbl = F.load_table(rom)
    # global_slots.json (tools/alloc_plan.py) lists charcodes that own glyph
    # storage and are drawn by NO scenario -- the old scenario_slots.json only
    # asked whether Nice Guy drew them, which is why 703 of the slots in use were
    # characters some other scenario really renders.
    slots = json.load(open(os.path.join(OUT, "global_slots.json")))
    reserved = M.reserved_charcodes(tbl)
    # 재분석 census(analysis/census.json)의 drawn_codes와 합집합: 구 폭 표로 걸은
    # global_slots는 오프코드 인자로 삼킨 텍스트와 UI 뱅크 문자열 소비자를 못 봐서
    # 실제로 그려지는 cc 111개를 «비었다»고 판정했다 (kr_font_map v174에 전부 배정돼
    # 있었음). PP9 신규 인명 글리프 e50(0xCA6~0xCAE)도 이 합집합으로 보호된다.
    _re_census = os.path.join(os.path.dirname(os.path.dirname(OUT)), "..",
                              "analysis", "census.json")
    reserved = set(reserved) | set(
        json.load(open(_re_census, encoding="utf-8"))["drawn_codes"])
    # Use only 2-byte-encodable charcodes (>=256): charcodes 0-230 are 1-byte
    # (kana range, all of them drawn somewhere), and 231-255 aren't encodable.
    free = [s for s in slots if s not in reserved and s >= 256]
    free.sort()
    print(f"available glyph slots (2-byte, drawn by no scenario): {len(free)}")

    # priority-ordered target syllable list, deduped
    target = []
    seen = set()
    for ch in used_syllables() + ksx1001_wansung():
        if ch not in seen:
            seen.add(ch)
            target.append(ch)
    print(f"target set: {len(target)} (used {len(used_syllables())} + KSX fill)")

    if len(target) > len(free):
        print(f"  capping {len(target)} -> {len(free)} (slot-limited)")
        target = target[:len(free)]

    # Extension slots are served from pages in the grown overlay, so they only
    # resolve while overlay 28 is loaded. Gameplay dialogue always is; the intro
    # runs its own cutscene path and its residency is unconfirmed, so intro
    # syllables are kept on ARM9-resident slots. Everything else prefers the
    # extension slots -- that keeps the exercised path the one real text uses and
    # leaves the plain slots for the KS X 1001 filler.
    ext = set(M.EXT_CODES)
    intro_syl = set()
    p = os.path.join(TRANS, "intro_lines.tsv")
    if os.path.exists(p):
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            for c in ln.split("\t")[-1]:
                if 0xAC00 <= ord(c) <= 0xD7A3:
                    intro_syl.add(c)
    # The FF-terminated tables (ability names, encyclopedia, the daily action
    # menu) are drawn by screens that never call our render_char hook, and the
    # extension pages only resolve inside that hook -- it swaps the font table
    # for one call and swaps back. An extension charcode on those screens draws
    # whatever the ORIGINAL font holds at that slot, which is how 「연습한다」 came
    # out as 「♫♫を…」 while 「설정」 (its syllables happened to get plain slots)
    # rendered fine. So pin them to plain slots exactly like the intro.
    # file8_extra is the ability/item panel -- another screen drawn outside the
    # render_char hook, so its syllables need plain slots for the same reason.
    for fn in (sorted(glob.glob(os.path.join(COMMON, "*_table.tsv")))
               + sorted(glob.glob(os.path.join(COMMON, "file*_profiles.tsv")))
               + [os.path.join(COMMON, "file8_extra.tsv"),
                  # file20 = the daily action menu / training names / season
                  # stats, file18 = the card minigame's ability text. Session 34
                  # shipped file20 WITHOUT pinning and the user photographed the
                  # exact failure this comment predicts: 「연습한다」 (message box,
                  # render_char) drew fine while 『 』 the training NAME beside it
                  # came out 「『류旦』」 -- same screen, two renderers. Pin them.
                  os.path.join(COMMON, "file20_extra.tsv"),
                  os.path.join(COMMON, "file18_extra.tsv"),
                  # ⭐ SESSION 41 -- file30 is overlay 14, and the extension
                  # pages are not merely unhooked there, they are NOT IN RAM.
                  # They live at 0x02253C00, inside overlay 28's grown tail;
                  # `side_region` keeps them alive for files 4/27 by prepending
                  # `ext_blob` to ov29/ov30 (all three load at 0x021C0DC0), but
                  # ov14 loads at 0x0216C3C0 and its tail region carries no
                  # copy. Read on the album epilogue screen: 0x02253C00 is all
                  # zeros, so an extension charcode there draws a BLANK.
                  # Photographed on v163 -- 「이 프로그램」 came out 「이 프로그」,
                  # and the 램 (cc 3692) is the only extension code in the line.
                  # 51 of the 574 syllables files 18/20/30 need were landing on
                  # the extension page; plain slots are nowhere near exhausted.
                  os.path.join(COMMON, "file30_extra.tsv")]):
        if not os.path.exists(fn):
            continue
        for ln in open(fn, encoding="utf-8").read().splitlines()[1:]:
            f = ln.split("\t")
            if len(f) > 5:
                for c in f[5]:
                    if 0xAC00 <= ord(c) <= 0xD7A3:
                        intro_syl.add(c)
    plain = [s for s in free if s not in ext]
    extra = [s for s in free if s in ext]
    print(f"  slots: {len(plain)} ARM9-resident + {len(extra)} extension pages; "
          f"{len(intro_syl)} intro syllables pinned to ARM9")
    mapping, pi, xi = {}, 0, 0
    for ch in target:
        if ch not in intro_syl and xi < len(extra):
            mapping[ch] = extra[xi]
            xi += 1
        else:
            mapping[ch] = plain[pi]
            pi += 1
    json.dump(mapping, open(os.path.join(OUT, "kr_font_map.json"), "w",
                            encoding="utf-8"), ensure_ascii=False)
    print(f"wrote kr_font_map.json: {len(mapping)} syllables, "
          f"charcodes 0x{min(mapping.values()):04X}-0x{max(mapping.values()):04X}")


if __name__ == "__main__":
    main()
