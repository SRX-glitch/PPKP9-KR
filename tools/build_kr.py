#!/usr/bin/env python3
"""Build the Korean ROM: allocate charcodes, inject glyphs, patch dialogue.

Two ways a Korean line gets into the game:

  1. INLINE (default) -- the line is compressed (font pack charcodes + the MTE
     dictionary) until it fits the original string's byte budget. Nothing moves.
  2. REDIRECT -- the line is stored, uncompressed and unbounded, in the grown
     tail of overlay 28, and the inline bytes become a 4-byte escape that the
     text-handler hook follows (tools/redirect_hook.py, tools/expand_rom.py).
     This is for lines whose Korean cannot be squeezed into the budget without
     wrecking the translation.

Lines are never silently truncated: anything that neither fits nor can be
redirected is reported and left in Japanese.
"""
import os, sys, re, glob, json, collections, bisect
sys.path.insert(0, os.path.dirname(__file__))


def _refresh_allocation():
    """Regenerate survey/font/alloc_plan.json, then refuse to build if any of it
    lands on a glyph the game really draws.

    ⛔ SESSION 39. Every RAM address and charcode range the hooks use was a
    literal pasted in by hand, re-split incrementally, and never re-checked. By
    the time census v2 measured them, 12 of 17 placements sat on drawn glyphs --
    the MTE dictionary was writing its entries over the halfwidth katakana and
    fullwidth padding the ARM9 player-name array draws (「ｾｷﾞﾉｰﾙ」「ｸﾛｰﾊｰ」
    「鈴木　」), which is the tile garbage in the session-38 lineup screenshot.
    Running the allocator here means the plan can never be stale, and running the
    gate here means a bad plan fails the build instead of shipping.

    ⛔⛔ THIS MUST RUN BEFORE `import mte_hook` / `import redirect_hook`.
    Those modules read alloc_plan.json AT IMPORT TIME. When this lived inside
    main() the first build after any allocation change came out MIXED: the font
    pack was laid out from the new plan (300 extension slots over 5 blocks) while
    the hooks still held the previous run's (7 blocks, 234 MTE codes). Every gate
    passed, because each half was internally consistent.
    """
    import subprocess
    tools = os.path.dirname(os.path.abspath(__file__))
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    for script in ("alloc_plan.py", "verify_alloc.py"):
        r = subprocess.run([sys.executable, os.path.join(tools, script)],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", env=env)
        tail = [l for l in (r.stdout or "").splitlines() if l.strip()][-3:]
        print(f"[alloc] {script}: " + " | ".join(tail))
        if r.returncode:
            raise SystemExit(f"{script} FAILED -- do not ship this build\n"
                             f"{r.stdout}\n{r.stderr}")


_refresh_allocation()

import fontcodec as F
import poketbl as P
import mte_hook
import redirect_hook as R
import menu_hook as MH

# Redirect choice options through the ARM9 walker hook (tools/menu_hook.py).
# Opt-in: `PPKP9_CHOICE_REDIRECT=1`. Until it is confirmed on screen the default
# build keeps the session-29 behaviour -- choices capped at their inline budget,
# over-budget ones left in readable Japanese.
CHOICE_REDIRECT = bool(os.environ.get("PPKP9_CHOICE_REDIRECT"))
import expand_rom as X
import insert_tables as IT
import insert_common as IC
import insert_pointered as IP
import check_opcodes as CO
from koenc import Encoder
from PIL import Image, ImageDraw, ImageFont

BASE = r"C:/Users/jngji/Desktop/실험실"
ROMSRC = BASE + r"/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
ROMOUT = os.environ.get("PPKP9_ROMOUT", BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/builds/PPKP9_kr.nds")
SURVEY = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/survey"
FONTDIR = SURVEY + r"/font"
GULIM = r"C:/Windows/Fonts/gulim.ttc"
OV_FILE_START = 0x04CC000          # overlay 28 -> ROM

# The Korean word space is the raw byte 0x00, not a charcode. render_char's zero
# path clears exactly one 4px column and returns col+1, so the gap between words
# is a third of what a real charcode costs (every charcode is a full 12px cell),
# and it needs no glyph -- the old host 'ヅ' had its glyph blanked, and the whole-
# ROM census says some scenario draws ヅ 41 times, so that was a visible defect
# outside Nice Guy. Both text paths decode 0 as a blank charcode rather than a
# terminator: gameplay engine 0x020BFA20, cutscene width scanner 0x0203C9D4.
SPACE_BYTES = "00"

# ⭐ SESSION 37. The filler AFTER a redirect escape is never *drawn* -- the escape
# moves the cursor into the region and the return marker lands on the occurrence's
# own terminator -- but it IS *measured*, and the measurement is what sizes the
# box the text is drawn into.
#
# The cutscene path measures before it draws: scanner 0x0203C978 returns (charcode
# count, width in 4px columns) and 0x0203C91C turns that width into the box via
# `BL 01FF995C`. The scanner knows nothing about our escape, so a redirected slot
# measured as its own inline bytes: `F7 2E lo hi` = 5 columns, plus ONE column per
# 0x00 filler byte. Choice D measured 11 columns while its Korean needs 25, so the
# box was 44px and the line was cut at 4 glyphs -- observed on v116 for A/C/D, and
# misdiagnosed for two sessions as menu_hook's R9 correction being short. It was
# not: the draw walker was measured passing all 9 charcodes to render_char.
#
# The scanner's own rule is the fix: a byte < 0xF7 measures 3 columns, 0x00 only 1.
# So fill redirected slots with a 1-byte charcode instead of 0x00 and the box grows
# threefold for free -- no hook, no new code (there are only 48 bytes left below
# TINY_TBL anyway). 0xE7 is the ONE value in 0x01..0xE7 that the whole-ROM census
# says is never drawn AND that neither kr_map nor poketbl claims, so nothing can
# collide with it.
# ⚠ Inline (non-redirected) runs keep 0x00: their filler really is drawn, and a
# charcode there would paint a stray glyph instead of a 4px blank.
#
# ⚠⚠ And the box must not come out too WIDE either. Filling every spare byte with
# 0xE7 fixed the clipping and immediately produced the opposite defect on screen:
# choice C 「헌책방에 간다」 (20 columns) drew into a 26-column box and the last two
# columns still held 「로」 from choice A's longer line. The uploader only writes the
# columns it drew, so anything the box has beyond that keeps the previous draw.
# So aim the measurement AT the Korean's own width: each filler byte is worth 3
# columns as 0xE7 or 1 as 0x00, so mixing them hits any value of the right parity.
# ⭐ SESSION 38: `PPKP9_NO_PAD_AIM=1` puts the filler back to plain 0x00. That is
# the A/B that PROVES the measurement hook: with the hook installed the box is
# sized from the region entry's real width, so the filler stops mattering and the
# choices must stay whole with the aim switched off. Without the hook the same
# build clips them back to four syllables.
REDIRECT_PAD = 0x00 if os.environ.get("PPKP9_NO_PAD_AIM") == "1" else 0xE7


def scan_width(b):
    """Columns the cutscene scanner (0x0203C978) measures for `b`.

    Its rule reads only the LEAD byte: >=0xE8 consumes a second byte, 0x00 is a
    4px blank (1 column), and anything else is 3 columns below 0xF7 / 2 at or
    above it (the halfwidth band). Mirrored here so the filler can be aimed.
    """
    w = i = 0
    while i < len(b):
        lead = b[i]
        i += 2 if lead >= 0xE8 else 1
        w += 1 if lead == 0 else (3 if lead < 0xF7 else 2)
    return w


def aim_filler(esc, blen, korean):
    """Filler bytes that make the slot measure as wide as `korean` renders.

    n filler bytes span [n, 3n] columns in steps of 2, so k of them become 0xE7
    and the rest stay 0x00. Clamped: a Korean line wider than the slot can express
    still measures as wide as possible (the old behaviour, minus the clipping),
    and one narrower than n columns bottoms out at all-0x00.
    """
    n = blen - len(esc)
    if n <= 0:
        return b""
    need = scan_width(korean) - scan_width(esc)
    k = max(0, min(n, round((need - n) / 2)))
    return bytes([REDIRECT_PAD]) * k + b"\x00" * (n - k)

# A line that fits inline but leaves this many bytes of its budget unused takes
# the redirect path anyway. Inline patching has to fill the whole original byte
# span, and every filler byte draws a blank glyph, so a big shortfall shows up as
# a gap in the middle of a sentence (the run boundaries are inline control codes,
# not sentence ends). Through the region there is no filler at all: the escape
# moves the cursor away immediately and the return marker lands on the
# occurrence's own terminator. 4 leaves at most 3 filler columns = 12px = exactly
# one space, and costs ~11 KB of region; 3 would cost 26 KB for 4px more.
# ⛔ 1 IS TOO EXPENSIVE. Redirecting every line with any filler at all removed the
# trailing 4px gaps, but it pushed 2,277 more lines into the region and took the
# overlay grow from 0x8B000 to 0x9B000 -- and the user's game then FROZE ON A BLACK
# SCREEN entering the baseball part. That is the high-side memory pool the grow
# eats (RESUME: arena free stays 430 KB, the pool goes 790 KB -> 534 KB), and match
# entry was the one path never QA'd. The real noise -- marks in the MIDDLE of a
# word -- was spaces inside MTE entries, which is fixed separately and costs
# nothing. Trailing filler is cosmetic; a frozen match is not.
PAD_SHORTFALL_REDIRECT = int(os.environ.get("PPKP9_PAD_REDIRECT", "4"))

# Over-budget lines always take the redirect path. This knob additionally forces
# the N most frequent *fitting* lines through it, which was how the hook was
# first validated on screen (correct Korean = redirect resolved, blank box = it
# did not). Now that real overflows exercise the path every build, leave it at 0.
REDIRECT_TOP_N = 0
REGION_ALIGN = 0x1000              # grow the overlay by a whole number of pages

# Every byte the overlay grows is a byte taken off the scenario arena, which
# starts exactly where the overlay ends. Set PPKP9_STRESS_GROW to pad the growth
# out to what a fully translated script would need (~0x40000) and play deep: if
# the game survives that, no future batch can be the one that breaks it.
STRESS_GROW = int(os.environ.get("PPKP9_STRESS_GROW", "0"), 0)

font = ImageFont.truetype(GULIM, 12)


def encode_jp(s):
    out = bytearray()
    for ch in s:
        out += P.cc_to_bytes(P.CH2CC[ch])
    return bytes(out)


def enc_jp_len(s):
    return len(encode_jp(s))


def render(ch):
    if ch == " ":
        return [[0] * 12 for _ in range(12)]
    img = Image.new("L", (12, 12), 0)
    d = ImageDraw.Draw(img)
    bb = d.textbbox((0, 0), ch, font=font)
    d.text(((12 - (bb[2] - bb[0])) / 2 - bb[0], (12 - (bb[3] - bb[1])) / 2 - bb[1]),
           ch, font=font, fill=255)
    p = img.load()
    # 2bpp ink levels are NOT brightness: level 1 is the scene ink colour (white
    # in dialogue) and level 2 is the darker companion shade (purple here). The
    # stock font draws a stroke in both -- body in 1, a shadow edge in 2 -- which
    # is why Japanese reads white. Rendering Hangul strokes as 2 (the obvious
    # "solid" choice) made every Korean line come out dim purple; measured off a
    # capture, the Korean line was 100% purple while the Japanese line beside it
    # was a white/purple mix. So the core goes to 1 and the antialias to 2.
    return [[1 if p[x, y] >= 140 else (2 if p[x, y] >= 60 else 0) for x in range(12)]
            for y in range(12)]


def mte_expansion_fits(b, budget, expand):
    """Does every MTE expansion in `b` finish before the run does?

    An MTE code draws its FIRST glyph where it sits and the rest are parked in
    MTE_STATE for the engine-entry hook to inject one per engine call, without
    advancing the cursor (redirect_hook.build_hook). So an n-charcode entry needs
    n-1 further calls, and those only happen while the run still has bytes left.
    A code near the end of a tight run therefore loses its tail.

    Measured on screen, both directions:
      「좋아、그대로 밧줄을」  MTE[좋아、] then 13 more bytes -> renders in full
      「아니。」               MTE[아니。] then 1 filler byte -> the tail is cut,
                             which is the 「아니」 the user reported
    So the test is POSITIONAL, not a sum over the line: for each code, the bytes
    remaining after it (padding included) must cover its own debt and every later
    code's. Summing debt over the whole line instead flags 3,129 lines including
    「좋아、…」, which demonstrably works -- this rule flags 1,378 and gets both
    known cases right.

    Failing lines go to `over`, i.e. the redirect path, where the text is stored
    uncompressed and no expansion is needed. Budget-2 lines cannot carry even the
    banked escape, so those stay Japanese -- correct, since truncated Korean is
    worse than the original.
    """
    codes, j = [], 0
    while j < len(b):
        if b[j] <= 231:
            j += 1
            continue
        cc = 256 + (b[j] - 232) * 256 + b[j + 1]
        n = expand.get(cc)
        codes.append((j + 2, (n - 1) if n else 0))
        j += 2
    for k, (end, debt) in enumerate(codes):
        if not debt:
            continue
        if budget - end < sum(d for _, d in codes[k:]):
            return False
    return True


def char_cost(ch, one):
    if ch in one:
        return 1
    if 0xAC00 <= ord(ch) <= 0xD7A3:
        return 2
    cc = P.CH2CC.get(ch)
    return 1 if (cc is not None and cc < 231) else 2


def encoded_cost(ko, dict_list, one):
    """Byte length of ko under greedy longest-match dictionary encoding."""
    ds = sorted(dict_list, key=len, reverse=True)
    i = 0
    n = 0
    while i < len(ko):
        hit = None
        for s in ds:
            if ko.startswith(s, i):
                hit = s
                break
        if hit:
            n += 2
            i += len(hit)
        else:
            n += char_cost(ko[i], one)
            i += 1
    return n


def _line_subs(ko):
    """All 2-3 char substrings usable as a dictionary entry (<=3 charcodes)."""
    out = []
    for L in (3, 2):
        for j in range(len(ko) - L + 1):
            out.append(ko[j:j + L])
    return out


def train_mte(targets, weighted_corpus, one, max_entries, encodable):
    """Budget-aware dictionary trainer.

    targets:  list of (ko, budget, weight, hard) -- lines that must fit their
              budget. `hard` ranks lines with NO redirect fallback: 2 = the intro
              cutscene, 1 = choice options, 0 = ordinary lines (which do have the
              fallback). The intro outranks choices because it is one short scene
              every player sees end to end, and it is only 116 lines; choices are
              1,157 and each is seen by whoever happens to reach it.
    weighted_corpus: list of (ko, weight) -- used to spend leftover capacity on
                     general compression once the fit goal is met.
    encodable(sub) -> bool: every char in sub has a charcode.

    Phase 1 (fit): process targets HARD FIRST, then by weight; for each
      still-over-budget line, greedily add the substring that shrinks it most,
      until it fits or we run out of capacity.
    Phase 2 (compress): fill any leftover slots with the most byte-saving
      frequent substrings from the whole corpus.

    ⚠ Why `hard` outranks weight. Weight alone is the wrong priority because it
    treats all over-budget lines as equally stuck, and they are not. An overlay-28
    line that does not fit still ships correctly -- it takes the 4-byte redirect
    escape and lives in the region at any length. The **intro cutscene has no such
    fallback**: the ARM9 cutscene walker never passes through the redirect hook, so
    an over-budget intro line is truncated *permanently*. Those lines were arriving
    with weight 1 and reaching Phase 1 only after thousands of overlay-28 lines had
    consumed all 222 codes, so they never got a single entry -- which is why the
    opening's proper nouns had to be cut to 「데스」「루나」「무라」 and why 「レガタ」 stayed
    Japanese. One MTE code is 2 bytes and expands to up to 3 charcodes, so it buys
    exactly what those runs need. Measured on the intro: MTE codes DO expand in the
    cutscene (0x3303B4 holds the 2 bytes `f6 83` and draws 「그래」 on screen).
    """
    import collections
    picked = []
    pset = set()

    # ⛔ DO NOT pin short choice options here. Session 30 pinned 「아니。」/「에에？」
    # believing they shipped in Japanese because the 457 codes ran out. That was a
    # misdiagnosis: an MTE code draws its FIRST glyph in place and injects the rest
    # on LATER engine calls, so a 3-charcode entry in a 3-byte run has nowhere to
    # put its tail -- exactly the case `mte_expansion_fits` documents and rejects.
    # The pin therefore burned two dictionary slots and changed nothing. A short
    # run needs Korean that fits in PLAIN bytes (1 syllable + 1 punctuation).
    PINNED = []

    def add(sub):
        if sub in pset or not encodable(sub):
            return False
        picked.append(sub)
        pset.add(sub)
        return True

    # ⛔ TRIED AND REJECTED (session 30): breaking Phase-1 ties by how valuable
    # the substring is corpus-wide, so a hard line would reuse an entry Phase 2
    # was going to mint anyway. It sounds right and it measured WORSE -- lines
    # left in Japanese went 675 -> 677 by raw frequency (it prefers 2-char
    # entries, half the saving each) and 675 -> 677 by total saving as well.
    # Phase 1's picks feed every later decision, so perturbing them globally to
    # help a hundred intro lines costs more elsewhere than it saves. Do not
    # reintroduce without measuring the `over-budget lines have no room` count.

    def floor_cost(ko):
        """Cheapest this line could ever be, given unlimited dictionary entries.

        Every char is either emitted raw at its own cost, or folded into a 2-byte
        MTE code with up to two neighbours. Phase 1 used to pour entries into lines
        that can NEVER fit -- a 3-byte choice holding 4 Korean syllables bottoms
        out at 4 bytes no matter what -- and each of those wasted entries is one
        the next line does not get. Skipping them is pure recovered capacity.
        """
        n = len(ko)
        best = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            c = best[i + 1] + char_cost(ko[i], one)
            for L in (2, 3):
                if i + L <= n:
                    c = min(c, best[i + L] + 2)
            best[i] = c
        return best[0]

    # ⚠ respect max_entries -- PPKP9_MTE_MAX=0 must really mean an empty dictionary,
    # or the diagnostic build it exists for is not actually testing anything.
    for sub in PINNED:
        if len(sub) <= 3 and len(picked) < max_entries:
            add(sub)

    # Phase 1: fit -- no-fallback lines first (intro, then choices), then by weight
    for ko, budget, w, hard in sorted(targets, key=lambda t: (-t[3], -t[2])):
        if hard and floor_cost(ko) > budget:
            continue                      # hopeless; do not burn entries on it
        guard = 0
        while len(picked) < max_entries and encoded_cost(ko, picked, one) > budget:
            cur = encoded_cost(ko, picked, one)
            best, best_gain = None, 0
            for sub in _line_subs(ko):
                if sub in pset or not encodable(sub):
                    continue
                picked.append(sub)
                gain = cur - encoded_cost(ko, picked, one)
                picked.pop()
                if gain > best_gain:
                    best, best_gain = sub, gain
            if best is None or best_gain <= 0:
                break
            add(best)
            guard += 1
            if guard > 12:
                break

    # Phase 2: compress leftover capacity by frequency
    while len(picked) < max_entries:
        cand = collections.Counter()
        cur_pset = sorted(picked, key=len, reverse=True)
        for ko, w in weighted_corpus:
            i = 0
            seg = []
            while i < len(ko):
                hit = next((s for s in cur_pset if ko.startswith(s, i)), None)
                if hit:
                    if seg:
                        pass
                    i += len(hit)
                else:
                    seg.append((i, ko[i]))
                    i += 1
            for L in (3, 2):
                for j in range(len(ko) - L + 1):
                    sub = ko[j:j + L]
                    if sub not in pset and encodable(sub):
                        cand[sub] += w

        def saving(kv):
            sub, n = kv
            return (sum(char_cost(c, one) for c in sub) - 2) * n

        best = max(cand.items(), key=saving, default=None)
        if best is None or saving(best) <= 0:
            break
        room = max_entries - len(picked)
        for sub, n in sorted(cand.items(), key=saving, reverse=True)[:room]:
            if saving((sub, n)) <= 0:
                break
            add(sub)
        break
    return picked


# Korean particles alternate on whether the preceding syllable has a final
# consonant, and the preceding word here is the NAME we just translated -- so the
# right allomorph is computable per occurrence. That is the whole reason the
# absorption can be done automatically instead of by hand, 267 sites over.
# ⛔ 「に」「で」「へ」 are deliberately absent: 「に」 is 에 after a place and 에게 after
# a person, and nothing in the byte stream says which. A wrong particle reads
# worse than the Japanese one, so those sites keep 「に」.
_JOSA = {"は": ("은", "는"), "が": ("이", "가"), "を": ("을", "를"),
         "と": ("과", "와"), "も": ("도", "도"), "の": ("의", "의"),
         "や": ("이랑", "랑")}


def _josa(ko_name, jp_particle):
    """The particle to append to `ko_name`, or None if we should not guess."""
    pair = _JOSA.get(jp_particle)
    if not pair or not ko_name:
        return None
    last = ko_name.rstrip()[-1:]
    if not last or not (0xAC00 <= ord(last) <= 0xD7A3):
        return None                 # not a Hangul syllable: cannot read a batchim
    return pair[0] if (ord(last) - 0xAC00) % 28 else pair[1]


def main():
    # ---- inputs ----
    trans = {}
    # Discovered, not listed. The hand-maintained tuple this replaced was 119
    # entries long and every new batch needed a line added by hand -- a forgotten entry
    # drops thousands of translated lines from the build and nothing complains,
    # because a missing batch just looks like untranslated text. Numeric sort
    # (not lexicographic) preserves the load order the old tuple had, which
    # matters: later batches intentionally override earlier ones on duplicate jp.
    tdir = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/translation"
    names = ["common_lines.tsv"] + [
        os.path.basename(p) for p in
        sorted(glob.glob(tdir + "/batch*.tsv"),
               key=lambda p: int(re.search(r"batch(\d+)\.tsv$", p).group(1)))]
    for name in names:
        for ln in open(f"{tdir}/{name}", encoding="utf-8").read().splitlines()[1:]:
            if "\t" in ln:
                jp, ko = ln.split("\t")[:2]
                # ⭐ A LEADING SPACE IN `ko` IS DATA, NOT WHITESPACE. Runs that
                # follow a `F8 08 <name> F8 09` insert start immediately after the
                # name, so 「カンタ」+「君のお母さん。」 needs 「 군의 어머니。」 to come
                # out as 「칸타 군의 어머니。」 -- Japanese does not space there and
                # Korean does. `ko.strip()` silently ate it. Only line-ending
                # whitespace is stripped now; measured first, no batch row in the
                # corpus had leading OR trailing spaces, so nothing else moves.
                ko = ko.strip("\r\n\t")
                if jp.strip() and ko.strip():
                    trans[jp.strip()] = ko
    print(f"[trans] {len(names)} files -> {len(trans)} unique lines")
    # absolute-ROM-offset patches (intro cutscene etc. -- outside overlay 28)
    intro = []
    for ln in open(BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/translation/intro_lines.tsv",
                   encoding="utf-8").read().splitlines()[1:]:
        p = ln.split("\t")
        if len(p) >= 3:
            intro.append((int(p[0], 16), p[1].strip(), p[2].strip()))
    lines = []
    # dialogue_runs.tsv (tools/extract_all.py) replaces the old dialogue_lines.tsv:
    # same addr/byte-budget/text shape, but it walks inline control codes instead
    # of stopping at them, so it holds the whole script (35k runs, not 10k).
    for ln in open(SURVEY + r"/ov28/dialogue_runs.tsv", encoding="utf-8").read().splitlines():
        p = ln.split("\t")
        if len(p) >= 4:
            lines.append((int(p[0], 16), int(p[1]), p[3]))
    # ⭐ SESSION 38. `extract_all`'s `in_dialogue` gate means a name pushed into a
    # sentence with `F8 08 <name> F8 09` from OUTSIDE an `F8 6B` message never
    # entered this corpus -- and `extract_extra` skipped it too, because the batch
    # corpus already translates it. Between the two gates 「ビクトリーズ」 fell
    # through, and the player reads Korean dialogue with a Japanese name in it.
    # These are overlay 28, so they ride the region and escapes that are already
    # there; feeding them into `lines` is all it takes.
    import extract_names as EN
    _named = [(o, b, t) for o, b, t in EN.runs() if t in trans]
    lines += _named
    print(f"translations: {len(trans)}   dialogue lines: {len(lines)} "
          f"(+{len(_named)} name inserts the corpus missed)")

    # ---- opcode-mask guard (reanalysis width table, 2026-08-09) ----
    # dialogue_runs.tsv was extracted with the OLD width table, which had
    # `F8 20` at 3 bytes (canonical: 2). Wherever `F8 20` is immediately
    # followed by another F8 opcode, the old walk swallowed that F8 lead and
    # started the text run ON the marker bytes of double-marker opcodes
    # (`F8 19 19` and family). Shipping those rows overwrites live engine
    # markers with Korean -- the 37 bytes the new opcode gate caught. Until
    # the corpus is re-extracted and re-keyed (master.tsv merge), drop every
    # run that overlaps an opcode byte under the canonical table.
    _pr0 = open(ROMSRC, "rb").read()
    _pf = int.from_bytes(_pr0[0x48:0x4C], "little")
    _plo = int.from_bytes(_pr0[_pf + 25 * 8:_pf + 25 * 8 + 4], "little")
    _phi = int.from_bytes(_pr0[_pf + 25 * 8 + 4:_pf + 25 * 8 + 8], "little")
    _Lw = json.load(open(os.path.join(SURVEY, "ov28", "opcode_lengths.json"),
                         encoding="utf-8"))
    _own = CO.opcode_bytes(_pr0, _plo, _phi,
                           {int(k): v for k, v in _Lw["bare"].items()},
                           {int(k): v for k, v in _Lw["f8"].items()})
    _span = _phi - _plo
    _bad = [(o, b, t) for o, b, t in lines
            if 0 <= o < _span and any(_own[o + k] for k in range(min(b, _span - o)))]
    if _bad:
        lines = [r for r in lines if r not in set(_bad)]
        print(f"opcode-mask guard: {len(_bad)} runs overlap opcode bytes under "
              f"the canonical width table -- quarantined (left Japanese). "
              f"sample: {[(hex(o), t[:12]) for o, _, t in _bad[:6]]}")

    # ---- Korean font pack (fixed complete map) ----
    # A pre-built complete Hangul font (tools/build_fontpack.py) on a stable
    # syllable->charcode map. Regenerate it here so any newly-used syllable is
    # guaranteed a slot, then inject ALL of its glyphs -- font is decoupled from
    # which lines happen to be translated.
    import build_fontpack
    build_fontpack.main()
    fontmap = {k: int(v) for k, v in
               json.load(open(os.path.join(FONTDIR, "kr_font_map.json"),
                              encoding="utf-8")).items()}
    all_ko = list(trans.values()) + [ko for _, _, ko in intro]
    need = {c for t in all_ko for c in t if 0xAC00 <= ord(c) <= 0xD7A3}
    missing = need - set(fontmap)
    if missing:
        raise SystemExit(f"{len(missing)} syllables not in font pack: "
                         f"{sorted(missing)[:20]}")
    mapping = {"syl": fontmap, "one": {}, "raw": {" ": SPACE_BYTES}}
    onebyte = set(mapping["one"]) | set(mapping["raw"])   # chars costing 1 byte
    print(f"font pack: {len(fontmap)} Hangul glyphs (complete); "
          f"space -> raw byte 0x{SPACE_BYTES} (4px blank, no glyph)")

    # ---- MTE dictionary (expanded at runtime by the ARM9 hook) ----
    base_enc = Encoder(mapping)          # no mte yet: char-level charcodes

    def encodable(sub):
        # ⛔ NEVER put a space inside a dictionary entry. Outside the dictionary a
        # Korean space is the raw byte 0x00, whose render_char path clears exactly
        # one 4px column and draws nothing. Inside an entry it goes through
        # charcode(' ') instead and becomes the GAME's own space character, which
        # is a real glyph of a different width -- so every expansion that spanned a
        # word boundary left a visible mark mid-sentence. That is the "noise" seen
        # in 「괴롭히는⋅짓은」 (`괴롭히` + `는 `) and 「들고⋅있어줘」. 87 of 457 entries had
        # one. Forbidding them costs a little compression and removes the artifact.
        if " " in sub:
            return False
        return all(base_enc.charcode(c) is not None for c in sub)

    occ = collections.Counter(jp for _, _, jp in lines)
    jp_budget = {}
    for off, blen, jp in lines:
        jp_budget[jp] = blen              # identical text -> identical budget

    # ---- which runs are choice options -------------------------------------
    # Needed BEFORE training, not just before redirecting: a choice option has no
    # redirect fallback (escapes are not intercepted inside a choice block), so it
    # is exactly as `hard` as an intro line and must compete for MTE entries on
    # the same footing. Computed from the PRISTINE overlay: `F8 15 <count>` opens
    # a choice list and `F8 2D` closes it.
    choice_spans = []
    _romsrc0 = open(ROMSRC, "rb").read()
    _f = int.from_bytes(_romsrc0[0x48:0x4C], "little")
    _lo = int.from_bytes(_romsrc0[_f + 25 * 8:_f + 25 * 8 + 4], "little")
    _hi = int.from_bytes(_romsrc0[_f + 25 * 8 + 4:_f + 25 * 8 + 8], "little")
    # ⛔⛔ SESSION 35: this used to scan forward for `F8 2D` and, when it found
    # none within 400 bytes, GUESS a 200-byte span. 146 of the 199 blocks took
    # that guess, spans ran up to 392 bytes, and **1,841 runs were marked as
    # choice options when only ~656 are.** A choice option can never be
    # redirected (the escape is not intercepted there), so every mislabelled
    # over-budget line was silently locked to Japanese and counted in no total --
    # that is where the user's "미번역 구간" came from: 「今日の食事分は確保した。」
    # 「商店街で漢方薬売ってるんだ。」 all had translations and all sat inside one
    # bogus 381-byte span.
    # `F8 15 <count>` states how many options follow (session 30 established the
    # width and the count byte), so take exactly the next `count` recorded runs
    # and end there. Measured: 199 blocks either way, longest span 392B -> 96B,
    # counts 2-8, in-choice runs 1,841 -> 656.
    _starts = sorted(off for off, _, _ in lines)
    _by_start = {off: blen for off, blen, _ in lines}
    _i = _romsrc0.find(b"\xf8\x15", _lo, _hi)
    while 0 <= _i < _hi - 4:
        if _romsrc0[_i - 1] != 0xF8:          # not the `F8 F8` separator's tail
            _s, _n = _i - _lo, _romsrc0[_i + 2]
            if 1 <= _n <= 12:
                _k = bisect.bisect_left(_starts, _s)
                _sel = _starts[_k:_k + _n]
                if _sel:
                    choice_spans.append((_s, _sel[-1] + _by_start[_sel[-1]]))
        _i = _romsrc0.find(b"\xf8\x15", _i + 1, _hi)

    def in_choice(off):
        return any(s <= off < e for s, e in choice_spans)

    choice_jp = {jp for off, _, jp in lines if in_choice(off)}
    print(f"choice options excluded from redirect: {len(choice_jp)} distinct "
          f"(escapes are not intercepted there) -- trained as hard targets")
    # targets: every translated line that has a place to go, with its budget
    targets = []
    for jp, ko in trans.items():
        if jp in jp_budget:
            # hard only for choice options: ordinary overlay-28 lines still ship
            # via the redirect when they overflow, choices cannot.
            targets.append((ko, jp_budget[jp], occ.get(jp, 1),
                            1 if jp in choice_jp else 0))
    for romoff, jp, ko in intro:
        # hard=2: the cutscene walker never reaches the redirect region, so an
        # over-budget intro line is truncated for good -- see train_mte's note.
        targets.append((ko, enc_jp_len(jp), 1, 2))
    weighted = [(ko, occ.get(jp, 1)) for jp, ko in trans.items()]
    weighted += [(ko, 1) for _, _, ko in intro]
    # DIAGNOSTIC: PPKP9_MTE_MAX caps the dictionary (0 = no MTE at all). The
    # dictionary's charcodes and storage are the patch's biggest footprint on the
    # OTHER scenarios, so this measures what buying that back would cost in
    # redirects and overlay growth.
    mte_cap = int(os.environ.get("PPKP9_MTE_MAX", str(mte_hook.MAX_ENTRIES)), 0)
    mte_subs = train_mte(targets, weighted, onebyte,
                         min(mte_cap, mte_hook.MAX_ENTRIES), encodable)
    entries = []          # entries[i] = charcode list for MTE code code_for(i)
    mte_map = {}
    for sub in mte_subs:
        ccs = [base_enc.charcode(c) for c in sub]
        if any(c is None for c in ccs):
            continue
        mte_map[sub] = mte_hook.code_for(len(entries))
        entries.append(ccs)
    mapping["mte"] = mte_map
    json.dump(mapping, open(os.path.join(FONTDIR, "kr_map.json"), "w",
                            encoding="utf-8"), ensure_ascii=False, indent=1)
    enc = Encoder(mapping)
    print(f"MTE dictionary: {len(entries)}/{mte_hook.MAX_ENTRIES} entries "
          f"(sample: {list(mte_map)[:8]})")

    # code -> how many charcodes it expands to, for the slack test below
    mte_expand = {code: len(sub) for sub, code in mte_map.items()}

    enc_plain_early = Encoder({**mapping, "mte": {}})

    # ⛔⛔⛔ SESSION 36 — CHOICES MAY NOT CARRY MTE CODES AT ALL.
    # `mte_expansion_fits` (below) encodes the dialogue engine's rule: a parked
    # charcode is injected once per FOLLOWING ENGINE CALL, so leaving enough
    # bytes after a code pays its debt. That premise is FALSE for choices. The
    # injector lives at the overlay-1 engine entry (`redirect_hook.build_hook`),
    # and choice options are drawn by the ARM9 walker at 0x0203CBC8, which never
    # goes through it -- so an MTE code in a choice loses EVERYTHING past its
    # first glyph, no matter how much room follows it.
    # Measured on screen by the user, on v114 (choice redirect hook ON, so the
    # hook is not the fix either -- it only corrects the escape's charcode count):
    #   「ただのきまぐれです。」 -> 「그냥 변덕입니다。」(8)  drew 「그냥 변덕」   (4~5)
    #   「スポーツ用品店へ」     -> 「스포츠용품점으로」(8)  drew 「스포츠용품」 (6)
    #   「たった今、一人釣れた。」-> 「방금 낚였다」(5, plain) drew in full        ✔
    # So: plain only. A choice that then does not fit stays JAPANESE, which is
    # the project's standing rule -- truncated Korean is worse than the original.
    # `PPKP9_CHOICE_MTE=1` restores the old behaviour for A/B measurement.
    CHOICE_MTE = os.environ.get("PPKP9_CHOICE_MTE") == "1"

    def inline_encode(ko, blen, is_choice=False):
        """Inline bytes for one run: the shortest form whose MTE tail can play out.

        ⭐⭐ SESSION 35, from a user photo of the first practice choice: option B
        「今日の食事分は確保した。」 was Japanese on screen even though its Korean is
        19 B and the run's budget is 19. It fit and was still thrown away, because
        `mte_expansion_fits` rejected it -- an MTE code near the END of the run has
        no following engine calls to inject its parked charcodes. And a choice
        option has no redirect to fall back on (the escape is not intercepted
        there), so "does not fit" means "stays Japanese" forever.
        Measured: 145 choice runs in that state.

        It is the SAME positional problem `region_encode` solves, so use the same
        shape -- try full MTE, then plain-ify a growing tail, then plain -- and
        pick the first candidate that fits the budget AND passes the positional
        check. Plain is longest but never has a tail to lose, so it wins whenever
        the budget can afford it.
        """
        # ⛔ MEASURED: putting plain FIRST costs more than it buys. v93 tried it
        # (safest-first, on the theory that plain can never lose an MTE tail) and
        # `left Japanese` went 79 -> 236: plain is longer, so 391 lines stopped
        # qualifying for the redirect and fell back to Japanese. 45 choice options
        # gained, 153 dialogue lines lost -- a net loss. `mte_expansion_fits`
        # already guards the tail, so keep the SHORTEST form first and only
        # plain-ify a tail when the positional check actually rejects it.
        if is_choice and not CHOICE_MTE:
            return enc_plain_early.encode(ko)
        cands = [enc.encode(ko)]
        for k in (2, 3, 4):
            if len(ko) > k:
                cands.append(enc.encode(ko[:-k]) + enc_plain_early.encode(ko[-k:]))
        cands.append(enc_plain_early.encode(ko))
        for c in cands:
            if len(c) <= blen and mte_expansion_fits(c, blen, mte_expand):
                return c
        return cands[0]                    # nothing fits; caller reports it

    # ---- budget check ----
    fits, over = [], []
    for off, blen, jp in lines:
        ko = trans.get(jp)
        if ko is None:
            continue
        try:
            b = inline_encode(ko, blen, in_choice(off))
        except KeyError as e:
            over.append((jp, ko, f"unmapped {e}"))
            continue
        ok = len(b) <= blen and mte_expansion_fits(b, blen, mte_expand)
        (fits if ok else over).append((off, blen, jp, ko, b))
    print(f"\noccurrences to patch: {len(fits)}   over budget: {len(over)}")
    if over:
        seen = set()
        for item in over:
            key = item[2] if len(item) > 3 else item[0]
            if key in seen:
                continue
            seen.add(key)
            if len(item) > 4:
                print(f"  OVER  {item[2]!r} -> {item[3]!r}  {len(item[4])}B > {item[1]}B")
            else:
                print(f"  SKIP  {item[0]!r} -> {item[1]!r} ({item[2]})")

    uniq = len({jp for _, _, jp, _, _ in fits})
    print(f"distinct lines patched: {uniq}, total occurrences: {len(fits)}")

    # ---- pick the lines that go through the redirect region ----
    # A line is redirectable only if EVERY one of its occurrences has room for
    # the escape; a 2- or 3-byte budget (「うん。」and friends) cannot hold it,
    # but such lines are short enough to fit inline anyway.
    min_budget = collections.defaultdict(lambda: 1 << 30)
    for off, blen, jp in lines:
        min_budget[jp] = min(min_budget[jp], blen)

    # ⛔ A choice option can never be redirected. Inline Korean works there (the
    # 「응。」 substitution renders), but the escape is NOT intercepted: the hook
    # sits on the dialogue engine's cursor fetch, and the choice list is read by
    # a different path, so the escape bytes get drawn as glyphs. `F7 2E xx yy`
    # comes out as three stray kana -- 「단축한다」 rendered as 「ヴごん」, which is
    # the "noise" the user reported. This was in the shipped v0.9: 811 option
    # occurrences (706 distinct) were redirected and every one of them was
    # garbage on screen. Over-budget options therefore stay Japanese; readable
    # Japanese beats a scrambled escape.
    # ⛔⛔ SESSION 35: both of these tests used to be asked of the LINE and then
    # applied to every OCCURRENCE of it. They are facts about an occurrence:
    # "does this run have room for an escape" is about this run's budget, and
    # "is this a choice option" is about this run's offset. Judging per line threw
    # away every占 occurrence of a line that merely APPEARS somewhere unfavourable
    # -- measured on v85: 75 runs blocked because the same Japanese occurs
    # elsewhere at budget < 2, and 38 blocked because it occurs inside some choice
    # block, while these particular runs had room and sat in ordinary dialogue.
    def redirectable_here(off, blen):
        # budget 2 rides the two-byte escape (redirect_hook.tiny_escape); it has
        # its own charcode per line, so capacity is the F7 band, not an index
        if blen < R.TINY_BUDGET:
            return False
        return CHOICE_REDIRECT or not in_choice(off)

    # ---- occurrences that must redirect so their particle can be absorbed ----
    # See the `absorb` block further down. A name that FITS inline gets no region
    # entry, and then there is nowhere to put the 1-byte particle behind it -- so
    # 「夏菜」(4B, fits) kept its 「の」 while 「ビクトリーズ」(over budget) lost it.
    # Force those occurrences through the region even though they fit; the escape
    # is 4 bytes at budget >= 4 and 3 at budget 3, so it costs nothing they do not
    # already have. Measured: 18 absorbable sites without this, 267 candidates.
    absorb, force_redirect = {}, set()
    rom_src = open(ROMSRC, "rb").read()
    for off, blen, jp in lines:
        ko = trans.get(jp)
        if not ko or not redirectable_here(off, blen):
            continue
        p = off + blen
        if bytes(rom_src[OV_FILE_START + p:OV_FILE_START + p + 2]) != b"\xf8\x09":
            continue
        q = p + 2
        pb = rom_src[OV_FILE_START + q]
        if pb == 0 or pb >= 0xE8:
            continue                        # 1-byte charcodes only
        nxt = rom_src[OV_FILE_START + q + 1]
        if nxt != 0 and nxt < 0xF8:
            continue                        # the particle run is longer than 1 byte
        pko = _josa(ko, P.CC2CH.get(pb - 1))
        if not pko:
            continue
        absorb[off] = (pko, q)          # encoded later: enc_plain is not built yet
        force_redirect.add(off)

    # over holds 5-tuples for real overflows and 3-tuples for unmappable text
    over_jp = {item[2] for item in over if len(item) == 5}
    redirect_jp = {jp for off, blen, jp in lines
                   if (jp in over_jp or off in force_redirect)
                   and redirectable_here(off, blen)}
    # DIAGNOSTIC: PPKP9_NO_REDIRECT builds with the whole redirect+grow subsystem
    # off (no escapes, no region, no overlay grow, no engine hook). Over-budget
    # lines stay Japanese. Used to bisect the residual Success-scene freeze
    # (cause #2): if the scene still freezes with this, the culprit is MTE/font,
    # not the redirect/grow structural change.
    NO_REDIRECT = bool(os.environ.get("PPKP9_NO_REDIRECT"))
    if NO_REDIRECT or os.environ.get("PPKP9_GROW_ONLY"):
        redirect_jp = set()
    stuck = over_jp - redirect_jp
    extra = 0
    for jp in sorted({j for _, _, j, _, _ in fits}, key=lambda j: -occ.get(j, 1)):
        if extra >= REDIRECT_TOP_N:
            break
        if jp not in redirect_jp and redirectable(jp):
            redirect_jp.add(jp)
            extra += 1
    if stuck:
        print(f"⚠ {len(stuck)} over-budget lines have no room for the escape "
              f"either -- left in Japanese: {sorted(stuck)[:5]}")
    # Dump them with the REASON, because the two reasons need opposite responses
    # and the count alone hides which is which:
    #   budget<3  -- the run cannot hold even the 3-byte banked escape. Nothing
    #                but a shorter Korean wording will ever fit.
    #   choice    -- the run has room, but escapes are not intercepted inside a
    #                choice block, so it is capped at its inline budget. These
    #                are translatable the moment the Korean is short enough.
    with open(os.path.join(SURVEY, "stuck_lines.tsv"), "w",
              encoding="utf-8", newline="") as f:
        f.write("min_budget\treason\tjp\tko\n")
        for jp in sorted(stuck, key=lambda j: min_budget[j]):
            why = "choice" if jp in choice_jp else "budget<3"
            f.write(f"{min_budget[jp]}\t{why}\t{jp}\t{trans.get(jp, '')}\n")
    # ...and the lines that fit but would leave a visible run of filler glyphs.
    # Identical text has an identical budget, so the shortfall is a property of
    # the line, not of the occurrence.
    # ⚠ `redirectable_here` is per occurrence now, so ask it about THIS run.
    gappy = {jp for off, blen, jp, _, b in fits
             if blen - len(b) >= PAD_SHORTFALL_REDIRECT
             and redirectable_here(off, blen)}
    if not NO_REDIRECT and not os.environ.get("PPKP9_GROW_ONLY"):
        gappy -= redirect_jp
        redirect_jp |= gappy
        print(f"redirecting {len(gappy)} lines that fit but would leave "
              f">={PAD_SHORTFALL_REDIRECT} filler glyphs")

    # Region strings are unbounded, so encode them without the budget dance.
    # One entry per OCCURRENCE, not per line: each entry carries the address to
    # return the script cursor to, which is that occurrence's own terminator.
    # Budget-3 occurrences can only carry the banked 3-byte escape, whose index
    # space is the first R.SHORT_CAPACITY entries -- so allocate those first.
    region_idx, region_entries, manifest = {}, [], {}
    # Region strings are encoded WITHOUT the MTE dictionary. Compression buys
    # nothing here -- the region is length-unbounded -- and it actively breaks
    # things: an MTE code parks its expansion tail for the engine-entry hook to
    # inject one charcode per engine call, and in the region the code is followed
    # immediately by the RET marker, so the tail has nowhere to play out and gets
    # cut. That is what made 「아니。」 (a single MTE code for the whole string)
    # come out as 「아니」. Plain-encoding region text removes the hazard entirely.
    enc_plain = Encoder({**mapping, "mte": {}})

    def region_encode(ko):
        """Region text, MTE-compressed only where the expansion can play out.

        ⭐ SESSION 35. The region is the binding constraint on the whole patch --
        it is at its RAM ceiling (grow 0x7E000; the match freezes past ~0x80000),
        so every byte saved here is a line that ships instead of staying Japanese.
        Plain-encoding every entry was a blanket workaround for a POSITIONAL
        problem: an n-charcode MTE entry parks n-1 charcodes for the engine-entry
        hook to inject one per following engine call, and an entry ends at its RET
        marker, which is not drawn. A code sitting at the very end therefore loses
        its tail -- the 「아니。」 that came out 「아니」.

        So do not invent a new rule: reuse `mte_expansion_fits`, the checker that
        already encodes the measured behaviour, with the entry's own text as the
        run. Try full MTE, then plain-ify a growing tail until every code has the
        calls it needs, and fall back to plain if none of that works. Expansions
        are at most 3 charcodes (measured: 94 of length 2, 260 of length 3), so a
        2-character plain tail is always enough -- the loop is belt and braces.
        """
        b = enc.encode(ko)
        if mte_expansion_fits(b, len(b), mte_expand):
            return b
        for k in (2, 3, 4):
            if len(ko) <= k:
                break
            b2 = enc.encode(ko[:-k]) + enc_plain.encode(ko[-k:])
            if mte_expansion_fits(b2, len(b2), mte_expand):
                return b2
        return enc_plain.encode(ko)

    _REGION_MTE = os.environ.get("PPKP9_REGION_MTE") == "1"
    # ⛔ SESSION 36: a CHOICE entry may not carry MTE even in the region.
    # `region_encode`'s positional rule (and `mte_expansion_fits` behind it)
    # assumes the parked charcodes are injected once per following DIALOGUE
    # ENGINE call. A choice is drawn by the ARM9 walker at 0x0203CBC8, which
    # never reaches the injector, so the entry loses everything past each code's
    # first glyph however much room follows. Measured on v114 (choice hook ON,
    # region MTE ON): 「스포츠용품점으로」 drew 「스포츠용품」.
    # Plain costs bytes, but a redirected entry has the whole region to sit in --
    # that is the point of sending choices through the hook at all.
    encoded_ko = {jp: (enc_plain.encode(trans[jp])
                       if (not _REGION_MTE or jp in choice_jp)
                       else region_encode(trans[jp]))
                  for jp in redirect_jp}
    if _REGION_MTE:
        _nc = sum(1 for jp in redirect_jp if jp in choice_jp)
        if _nc:
            print(f"region: {_nc} choice entries forced to plain "
                  f"(the ARM9 choice walker cannot inject MTE expansions)")
    if _REGION_MTE:
        _p = sum(len(enc_plain.encode(trans[jp])) for jp in redirect_jp)
        _m = sum(len(v) for v in encoded_ko.values())
        print(f"region MTE: {_p:,}B -> {_m:,}B text "
              f"({100 * (_p - _m) / max(_p, 1):.1f}% smaller)")

    # Measurement only (PPKP9_MEASURE_REGION_MTE=1). The note above is right that
    # a code sitting immediately before the RET marker loses its expansion tail --
    # but that is a POSITIONAL problem, not a reason the region cannot use MTE at
    # all. An expansion needs at most two following engine calls, so keeping the
    # last two syllables of every entry plain gives every code somewhere to play
    # out. This prints what that would buy before anyone writes the real thing.
    if os.environ.get("PPKP9_MEASURE_REGION_MTE"):
        def region_mte(ko):
            if len(ko) <= 3:
                return enc_plain.encode(ko)
            return enc.encode(ko[:-2]) + enc_plain.encode(ko[-2:])
        plain_b = sum(len(encoded_ko[jp]) + 8 for jp in redirect_jp)
        try:
            mte_b = sum(len(region_mte(trans[jp])) + 8 for jp in redirect_jp)
            print(f"[measure] region plain {plain_b:,}B -> MTE-with-plain-tail "
                  f"{mte_b:,}B  ({100 * (plain_b - mte_b) / plain_b:.1f}% smaller)")
        except KeyError as e:
            print(f"[measure] region MTE estimate failed: {e}")
    # ⚠ Per OCCURRENCE, not per line: a run with no room for an escape, or one
    # sitting inside a choice block, stays Japanese without dragging its siblings
    # down with it.
    todo = [(off, blen, jp) for off, blen, jp in lines
            if jp in redirect_jp and redirectable_here(off, blen)]
    todo.sort(key=lambda t: t[1] != 3)          # budget-3 first, order otherwise kept

    # ---- hard cap on the region, because the overlay grow has a ceiling -------
    # Measured with grow-only builds (zero-filled region, no hook): the match part
    # loads and plays at grow 0x70000 and freezes on a black screen at 0x8D000. It
    # is the SIZE, not the content -- a zero-filled region of the shipping size
    # fails just the same. The grow moves the scenario heap base up, and the match
    # allocates from what is left, so past some point it has nowhere to run.
    # When the region has to shrink, drop the RAREST lines first: a line seen once
    # costs the same bytes as one seen fifty times, so keeping the frequent ones
    # buys the most visible Korean per byte.
    cap = os.environ.get("PPKP9_REGION_CAP")
    if cap:
        limit = int(cap, 0)
        keep, used, dropped = [], 0, 0
        for off, blen, jp in sorted(todo, key=lambda t: -occ.get(t[2], 1)):
            # text + `F7 38` + u24 offset + its 4-byte table slot. ⚠ Keep this
            # in step with redirect_hook._build_region_slim -- when the marker
            # shrank from 8 bytes to 5 this still said 8 and the cap silently
            # stopped matching the region it was supposed to bound.
            # ⭐ SESSION 39: the 9 was `[F7 38][u24 return]` (5) + the entry's
            # u32 table slot (4). Only tiny and banked entries still have a slot
            # -- the long form carries its offset in the escape -- so charging
            # every occurrence for one over-counts the region by ~4 B each and
            # drops lines that would have fit.
            need = len(encoded_ko[jp]) + ((5 if blen >= R.LONG_BUDGET else 9)
                                          if R.SLIM else 12)
            if used + need > limit:
                dropped += 1
                continue
            used += need
            keep.append((off, blen, jp))
        order = {id(x): i for i, x in enumerate(todo)}
        todo = sorted(keep, key=lambda t: (t[1] != 3, order.get(id(t), 0)))
        redirect_jp = {jp for _, _, jp in todo}
        print(f"region cap {limit:#x}: keeping {len(todo)} occurrences "
              f"(~{used:,}B), dropped {dropped} rarest -- those stay Japanese")
    # With the slim return the entry no longer knows its call site, so two
    # occurrences of the same line with the same run length can SHARE one entry.
    # That is worth more than the 5 bytes the marker itself saves.
    # Tiny (budget-2) occurrences must land on region indices 0..N-1: the hook
    # reads the index straight out of the 256-byte b2 table, so there is no room
    # for an offset. Everything else follows.
    n_tiny = len(R.tiny_codes())
    # ⭐ SESSION 39. Order: tiny (needs a TINY_TBL slot) -> banked (needs a table
    # slot) -> long (carries its own offset, needs NO slot). The table is sized to
    # the leading indexed run, so anything long-form after them costs nothing.
    _order = {R.TINY_BUDGET: 0}
    todo.sort(key=lambda t: _order.get(t[1], 1 if t[1] < R.LONG_BUDGET else 2))
    for off, blen, jp in todo:
        i = len(region_entries)
        if blen == R.TINY_BUDGET and i >= n_tiny:
            continue                       # out of tiny charcodes; stays Japanese
        _pk = absorb.get(off)
        region_entries.append((encoded_ko[jp] + (enc_plain.encode(_pk[0]) if _pk else b""),
                               R.OV28_RAM + off + blen))
        region_idx[off] = i
        manifest[f"0x{off:06X}"] = {"idx": i, "jp": jp,
                                    "ko": trans[jp], "budget": blen}
    n_short = sum(1 for _, blen, _ in todo if blen == 3)
    if n_short > R.SHORT_CAPACITY:
        raise SystemExit(f"{n_short} budget-3 redirects exceed the banked escape "
                         f"capacity {R.SHORT_CAPACITY}; widen BANK_COUNT")
    # Over-budget occurrences never entered `fits`, so fold the redirected ones
    # back in -- otherwise their escape is never written and the line silently
    # stays Japanese.
    fits += [it for it in over if len(it) == 5 and it[2] in redirect_jp]
    # Everything below LONG_BUDGET carries an index and therefore a table slot.
    # They sort first, so the indexed run is a prefix and the table stops there.
    n_indexed = sum(1 for _o, _b, _j in todo
                    if _b < R.LONG_BUDGET and _o in region_idx)
    redirect_region, region_offs = R.build_region(region_entries, n_indexed,
                                                 R.REGION_BASE)
    print(f"region table: {n_indexed} indexed entries of {len(region_entries)} "
          f"({len(region_entries) - n_indexed} carry their own offset)")
    # the extension glyph pages sit in front of the redirect region, which is
    # exactly what REGION_BASE already accounts for
    grow = (R.EXT_PAGE_BYTES + len(redirect_region)
            + REGION_ALIGN - 1) & ~(REGION_ALIGN - 1)
    grow += STRESS_GROW
    # ---- session 45: reserve for file 25's OWN extra-region ------------------
    # The main redirect region above serves the F8 6B dialogue corpus; file 25's
    # `extra` rows (F8 07/F8 27/FC/FF consumers) had NO overflow path -- ov28's
    # grow ended flush against the heap (389B slack measured on v217). This
    # reserve keeps zero-filled space at the very end of the grow; the pass at
    # the bottom of this file fills it via tail_region. ⚠ Changing the grow
    # moves every success-heap cheat address (delta was +0x72000 through v217).
    F25_RESERVE = int(os.environ.get("PPKP9_F25_RESERVE", "0x2000"), 0)
    grow += F25_RESERVE
    print(f"redirect: {len(redirect_jp)} lines / {len(region_entries)} occurrences "
          f"({n_short} via the 3-byte banked escape), "
          f"region {len(redirect_region)}B -> overlay grows 0x{grow:X}; "
          f"escape charcode {R.ESC_CC} ({R.ESC_B1:02X} {R.ESC_B2:02X}), "
          f"return charcode {R.RET_CC} ({R.ESC_B1:02X} {R.RET_B2:02X})")
    json.dump(manifest, open(os.path.join(SURVEY, "redirect_manifest.json"), "w",
                             encoding="utf-8"), ensure_ascii=False, indent=1)

    # ---- intro (absolute ROM offset) budget check ----
    intro_fits = []
    romsrc = open(ROMSRC, "rb").read()
    for romoff, jp, ko in intro:
        jb = enc_jp_len(jp)
        # verify the offset really holds the expected JP bytes
        want = encode_jp(jp)
        got = romsrc[romoff:romoff + len(want)]
        if got != want:
            print(f"  INTRO MISMATCH at 0x{romoff:X}: rom={got.hex()} expected={want.hex()}")
            continue
        b = enc.encode(ko)
        if len(b) <= len(want):
            intro_fits.append((romoff, len(want), jp, ko, b))
        else:
            print(f"  INTRO OVER  {jp!r} -> {ko!r}  {len(b)}B > {len(want)}B")
    print(f"intro lines to patch: {len(intro_fits)}/{len(intro)}")

    # ---- patch ----
    rom = bytearray(open(ROMSRC, "rb").read())

    tbl = F.load_table(bytes(rom))

    # Alias-block charcodes have no storage of their own -- blocks 55-63 all point
    # at block 0 -- so their glyphs go into extension pages at the front of the
    # grown overlay and the stub points the font table there for the duration of
    # one render_char call. Writing them through tbl[block] would corrupt the kana
    # in block 0, which is why they are routed here instead.
    assert mte_hook.EXT_BLOCKS == list(range(mte_hook.EXT_BLOCK0,
                                             mte_hook.EXT_BLOCK0 + len(mte_hook.EXT_BLOCKS))), \
        "extension pages must be contiguous from EXT_BLOCK0 -- the stub indexes them by block"
    ext_pages = {b: bytearray(0x900) for b in mte_hook.EXT_BLOCKS}
    byblock = collections.defaultdict(list)
    for s, cc in mapping["syl"].items():
        byblock[cc // 64].append((s, cc))
    for block, items in byblock.items():
        if block in ext_pages:
            for ch, cc in items:
                F.encode_glyph(ext_pages[block], cc, render(ch))
            continue
        blockdata = F.block_region(bytes(rom), tbl, block)
        for ch, cc in items:
            F.encode_glyph(blockdata, cc, render(ch))
        o = F.ram2rom(tbl[block])
        rom[o:o + 0x900] = blockdata
    ext_blob = b"".join(bytes(ext_pages[b]) for b in mte_hook.EXT_BLOCKS)
    # DIAGNOSTIC PPKP9_NO_EXT=1: EXT_BLOCKS is empty so no pages are built.
    # Keep the RESERVED span the same size anyway -- REGION_BASE is computed
    # from R.EXT_PAGE_BYTES, and moving the region would add a second variable
    # to an experiment asking one question ("does the match still hang
    # without the font-table swap?").
    if os.environ.get("PPKP9_NO_EXT") == "1" and not ext_blob:
        ext_blob = bytes(R.EXT_PAGE_BYTES)
    assert len(ext_blob) == R.EXT_PAGE_BYTES, \
        f"extension pages {len(ext_blob)}B != redirect_hook.EXT_PAGE_BYTES {R.EXT_PAGE_BYTES}"
    n_ext = sum(len(v) for k, v in byblock.items() if k in ext_pages)
    print(f"patched {len(byblock) - len(ext_pages)} font blocks + "
          f"{len(ext_pages)} extension pages ({n_ext} Hangul glyphs)")

    # Pad the shortfall that survives PAD_SHORTFALL_REDIRECT with 0x00, which is
    # a charcode like any other in the gameplay stream and the NARROWEST thing
    # that can be drawn: render_char's zero path clears exactly one 4px column
    # (0x0203D150) and returns col+1, where the 1-byte space is full width and
    # eats three. The original script already carries in-stream 0x00 inside
    # dialogue -- 419 runs continue with more text right after one -- and both
    # stream walkers decode it as charcode 0 rather than a terminator (engine
    # 0x020BFA20, name walker 0x020C3838), so this is native behaviour, not a
    # new assumption.
    # ⚠ The INTRO keeps the 1-byte space. That text goes through the ARM9
    # cutscene scanner, which is a different, 0-terminated walker -- the session-7
    # warning about stray 0x00s applies there and only there.
    # DIAGNOSTIC: PPKP9_REGION_ONLY builds the region and grows/appends it, but
    # writes NO escapes (redirected lines stay Japanese) and installs no hook.
    # Isolates whether the mere presence of region CONTENT at 0x02253C00 causes
    # cause #2 (vs the escapes in the script).
    REGION_ONLY = bool(os.environ.get("PPKP9_REGION_ONLY"))
    pad_b = bytes.fromhex(SPACE_BYTES)
    inline_n = redir_n = dropped_n = 0
    dropped_off = set()
    # The particle whose Korean now sits at the end of the preceding region entry
    # must not ALSO be drawn from the script. 0x00 is the engine's own narrow
    # blank (see insert_common's note), so the line simply closes up.
    # ⚠ Only blank a site whose name actually got an index: the region cap can
    # drop an occurrence after `absorb` was built, and then the Japanese particle
    # is still the correct thing to show.
    absorbed_n = 0
    for off, (_pko, q) in absorb.items():
        if off not in region_idx:
            continue
        rom[OV_FILE_START + q] = 0x00
        absorbed_n += 1
    if absorbed_n:
        print(f"particle absorb: {absorbed_n} one-byte particles moved into the "
              f"name's region entry and blanked in the script")
    for off, blen, jp, ko, b in fits:
        romoff = OV_FILE_START + off
        # Inline runs pad with 0x00 (their filler is drawn, so it must stay blank).
        # Redirected ones pad to AIM the measured width -- see REDIRECT_PAD.
        filler = None
        if off in region_idx:
            if REGION_ONLY:
                continue          # leave the original Japanese bytes untouched
            b = R.escape_bytes(R.safe_index(region_idx[off]), blen,
                               region_offs[region_idx[off]])
            filler = aim_filler(b, blen, region_entries[region_idx[off]][0])
            redir_n += 1
        else:
            # Over-budget occurrences are folded into `fits` so their escape gets
            # written, but the REGION CAP can drop one after the fold -- then it
            # has no index and still carries its too-long inline encoding. That
            # line simply stays Japanese; writing it would be silent corruption.
            if len(b) > blen:
                dropped_n += 1
                dropped_off.add(off)
                continue
            inline_n += 1
        # ⚠ A slice assignment LONGER than its slice inserts bytes and shifts the
        # entire ROM. The FAT then reads as filenames and the build dies far away
        # with "file size != overlay size" -- an hour of bisecting. Never silent.
        if len(b) > blen:
            raise SystemExit(f"escape/inline {len(b)}B does not fit the {blen}B "
                             f"run at 0x{off:06X} ({jp!r} -> {ko!r})")
        if filler is None:
            filler = b"\x00" * (blen - len(b))
        rom[romoff:romoff + blen] = b + filler
    for romoff, blen, jp, ko, b in intro_fits:
        if len(b) > blen:
            raise SystemExit(f"intro {len(b)}B does not fit the {blen}B run at "
                             f"0x{romoff:06X} ({jp!r} -> {ko!r})")
        rom[romoff:romoff + blen] = b + pad_b * (blen - len(b))
    print(f"patched occurrences: {inline_n} inline, {redir_n} redirected, "
          f"{dropped_n} left Japanese (over budget and no region slot)")

    # ---- install the ARM9 hooks ----
    # DIAGNOSTIC PPKP9_NO_MTE_HOOK: leave render_char completely unpatched.
    # PPKP9_MTE_MAX=0 is NOT the same test -- it empties the dictionary but the
    # stub is still installed, so charcodes inside CODE_RANGES are still
    # intercepted. This flag is for the one question that matters here: does the
    # match/minigame screen draw a charcode we claimed as an MTE code? Those codes
    # were only ever verified "unused" against **file25 + intro** (see mte_hook's
    # own note: "Scenario-scoped (Nice Guy only) ... even if other scenarios use
    # them"), and the match UI was never in that measurement.
    if os.environ.get("PPKP9_NO_MTE_HOOK"):
        print("DIAGNOSTIC PPKP9_NO_MTE_HOOK: render_char left unpatched "
              "(Korean on extension pages will not draw)")
    else:
        info = mte_hook.apply(rom, entries)
        print(f"MTE hook installed: stub {info['stub_bytes']}B, "
              f"dict {info['dict_entries']}/{info['capacity']} entries "
              f"({info['code_ranges']} code ranges, "
              f"{info['dict_regions']} dict regions)")
    NO_HOOK = bool(os.environ.get("PPKP9_NO_HOOK"))
    GROW_ONLY = os.environ.get("PPKP9_GROW_ONLY")   # e.g. "0x35000"
    if GROW_ONLY:
        # no escapes (redirected lines stay JP), no hook, but grow the overlay by
        # the given amount with a zero-filled region -> isolates the structural
        # grow/relocation/heap-shift from escapes AND hook AND region content.
        g = int(GROW_ONLY, 0)
        print(f"DIAGNOSTIC PPKP9_GROW_ONLY: grow overlay by 0x{g:X}, no escapes/hook/region")
        out = X.expand(rom, g, append=b"\x00" * g)
    elif NO_REDIRECT:
        print("DIAGNOSTIC PPKP9_NO_REDIRECT: skipping redirect hook + overlay grow")
        out = bytes(rom)
    elif NO_HOOK or REGION_ONLY:
        # keep escapes + region + grow, but DON'T patch the engine / write hook.
        # Redirected lines render garbled, but the structural change (grow, heap
        # shift, file relocation, appended region) is intact -> isolates whether
        # cause #2 is the grow/region/relocation vs the engine hook.
        print("DIAGNOSTIC PPKP9_NO_HOOK: grow+region kept, engine hook NOT installed")
        out = X.expand(rom, grow, append=ext_blob + redirect_region)
    else:
        hook_len = R.install(rom)
        print(f"redirect hook installed: {hook_len}B @0x{R.HOOK_ADDR:08X} "
              f"(overlay-1 engine site 0x{R.ENGINE_PATCH:08X}), "
              f"region base 0x{R.REGION_BASE:08X}")

        # The OTHER walker -- ARM9 static 0x0203CBC8, which draws menus, the
        # FF-terminated tables and choice options. Off by default: it is the
        # newest and least-proven patch in the build, and a bad one garbles the
        # screens that currently read fine in Japanese.
        if CHOICE_REDIRECT:
            mh = MH.install(rom)
            print(f"menu/choice hook installed: {mh['size']}B "
                  f"@0x{mh['addr']:08X} (ARM9 site 0x{MH.SITE:08X})")

            # The measurement pass that runs BEFORE that walker and decides how
            # wide the box is. Without it the box is sized from the escape's raw
            # bytes (~11 cells for a 25-cell line) and the Korean is clipped --
            # session 37's P1 truncation. Opt-in with PPKP9_MEASURE_HOOK=1 until
            # a screen confirms it; it only makes sense with CHOICE_REDIRECT, so
            # it lives inside this branch.
            if os.environ.get("PPKP9_MEASURE_HOOK") == "1":
                import measure_hook as MEH
                qh = MEH.install(rom)
                print(f"measure hook installed: {qh['size']}B "
                      f"@0x{qh['addr']:08X} (ARM9 site 0x{MEH.SITE:08X})")

        # ---- grow overlay 28 and append the redirect region ----
        # Relocates file25 into the ROM's tail slack, extends the overlay's RAM
        # size and pushes the scenario heap up by the same amount.
        out = X.expand(rom, grow, append=ext_blob + redirect_region)
    # ---- the FF-terminated text tables (files 13, 18, 30) ----
    # These live in their own overlays, not in overlay 28, so nothing above
    # touches them and they shipped in Japanese -- the character encyclopedia
    # screen was the visible symptom. Patched in place, after the expand, at
    # their ORIGINAL offsets: only FAT[25] moves, so every other file stays put.
    # Rows whose Korean does not fit the record are skipped, not truncated.
    out = bytearray(out)                 # expand() hands back immutable bytes

    # ---- mirror the font into the SECOND copy ----
    # Every one of the 68 glyph blocks exists twice in the ROM at a constant
    # +0x1499418, the second copy inside FAT[1897] -- a 1.87 MB blob whose first
    # bytes are an NDS header (`PAWAPOKE9..NTRJ`), i.e. an embedded image. Only
    # the first copy was ever patched. Screens that draw from the second one show
    # the original glyphs, which is the leading suspect for the garbled menu
    # (「돌아간다」 -> 「F 간다」). Mirroring costs nothing and removes the variable.
    FONT_COPY_DELTA = 0x1499418
    if os.environ.get("PPKP9_FONT_MIRROR") == "1":   # off by default: unverified
        lo = min(F.ram2rom(p) for p in F.load_table(bytes(out)))
        hi = max(F.ram2rom(p) for p in F.load_table(bytes(out))) + 0x900
        out[lo + FONT_COPY_DELTA:hi + FONT_COPY_DELTA] = out[lo:hi]
        print(f"font mirror: {hi - lo:#x} bytes copied to +{FONT_COPY_DELTA:#x} "
              f"({lo + FONT_COPY_DELTA:#x})")

    # ---- choice-block gate ----
    # `F8 15 <count>` opens a choice list. opcode_lengths.json had it at TWO
    # bytes, so the run walker started a text run on the COUNT byte, and the
    # redirect escape written there replaced the count with 0xF7 -- 106 of the
    # 206 choice blocks in the overlay. The engine then drew nothing at all:
    # that is the empty choice box hunted since session 27, and it is why the
    # symptom moved around whenever the redirect set changed (which is what made
    # `PPKP9_MTE_MAX=0` look like a fix, and what made line-level bisection
    # blame ordinary dialogue). The count byte is not text and must never move.
    pristine = open(ROMSRC, "rb").read()
    _L = json.load(open(os.path.join(SURVEY, "ov28", "opcode_lengths.json"),
                        encoding="utf-8"))
    CO_BARE = {int(k): v for k, v in _L["bare"].items()}
    CO_F8 = {int(k): v for k, v in _L["f8"].items()}
    f0 = int.from_bytes(pristine[0x48:0x4C], "little")
    ov_lo = int.from_bytes(pristine[f0 + 25 * 8:f0 + 25 * 8 + 4], "little")
    ov_hi = int.from_bytes(pristine[f0 + 25 * 8 + 4:f0 + 25 * 8 + 8], "little")
    f1 = int.from_bytes(out[0x48:0x4C], "little")
    shift = int.from_bytes(out[f1 + 25 * 8:f1 + 25 * 8 + 4], "little") - ov_lo
    damaged = total = 0
    i = pristine.find(b"\xf8\x15", ov_lo, ov_hi)
    while 0 <= i < ov_hi - 4:
        # `F8 F8` is the option separator, so a naive search also matches its
        # second byte followed by a text byte 0x15 -- and that text is ours to
        # replace. Requiring the predecessor not to be 0xF8 drops those five
        # false hits without weakening the real check.
        if pristine[i - 1] == 0xF8:
            i = pristine.find(b"\xf8\x15", i + 1, ov_hi)
            continue
        total += 1
        if pristine[i + 2] != out[i + 2 + shift]:
            damaged += 1
            print(f"  choice gate: @{i:#x} count {pristine[i+2]} -> "
                  f"{out[i+2+shift]:#04x}   orig {pristine[i-4:i+14].hex(' ')}")
            print(f"                              new  "
                  f"{bytes(out[i-4+shift:i+14+shift]).hex(' ')}")
        i = pristine.find(b"\xf8\x15", i + 1, ov_hi)
    if damaged:
        raise SystemExit(f"{damaged} choice blocks had their `F8 15 <count>` "
                         f"operand overwritten -- a run is starting one byte "
                         f"early. Check opcode_lengths.json (keys are DECIMAL, "
                         f"so F8 15 is entry \"21\", not \"15\").")
    print(f"choice gate: {total} choice blocks, {damaged} damaged")

    # ---- opcode gate ----
    # Broader version of the same idea: walk the pristine overlay, mark every
    # byte that belongs to an opcode (lead + operands) and require the output to
    # hold those bytes unchanged. Text may change; control flow may not. The walk
    # is charcode-aware -- lead bytes 0xE8-0xF7 take a second byte that can be
    # any value including 0xF8+, and reading those as opcode leads reports
    # thousands of phantom corruptions.
    ol = CO.opcode_bytes(pristine, ov_lo, ov_hi, CO_BARE, CO_F8)
    opbad = sum(1 for k in range(ov_hi - ov_lo)
                if ol[k] and pristine[ov_lo + k] != out[ov_lo + k + shift])
    if opbad:
        raise SystemExit(f"{opbad} opcode bytes changed in the overlay -- a patch "
                         f"is writing past a run's end. Run tools/check_opcodes.py.")
    print(f"opcode gate: {sum(ol):,} opcode bytes, {opbad} changed")

    # ---- shared dialogue files (4, 8, 20, 27) ----
    # Scenario-independent dialogue in its own FAT files, which overlay 28's
    # redirect never reached. 7,251 rows were translated sessions ago and then
    # never inserted because no path existed; this is inline-only, so the ~2,540
    # rows whose Korean already fits go in and the rest stay Japanese.
    com = IC.apply_all(out)
    print(f"shared dialogue: {com['written']} runs written, "
          f"{com['skipped']} skipped (do not fit)")

    # ---- text the F8 6B walk never saw ----
    # insert_common anchors on the dialogue message opener, which is one of ~76
    # opcodes that introduce text in file 4 alone. The rest carry real sentences
    # (「に着いたぞ。」, 「』を飲んだ！」) and whole screens of names, and they were never
    # even extracted. tools/walk_file.py walks with the validated opcode widths and
    # tools/extract_extra.py writes those runs out WITH OFFSETS, because without an
    # opener there is nothing to re-find them by.
    # Whole-record rebuilds. Must run BEFORE insert_extra: both write the same
    # runs, and the record pass needs the ORIGINAL Japanese in every run of a
    # record to prove the rebuild is safe.
    import insert_records as IR
    IR.apply_all(out, enc_plain)

    import insert_extra as IX
    ext = IX.apply_all(out, enc_plain)
    print(f"extra (non-F8 6B) runs: {ext['written']} written, "
          f"{ext['skipped']} too long, {ext['mismatch']} offset mismatch")

    # The town map's 「』に行きます」 is one shared 7-byte run with a 0xFF right
    # behind it, so 「』에 간다」 (8B) does not fit and 「』에간다」 (7B) has to drop
    # the space. Dropping the BRACKET PAIR instead buys that byte: the closing 』
    # is the first byte of our own run (the translation just omits it) and this
    # pass blanks the opening 『, which sits outside every worklist. Runs after
    # insert_extra because it keys off the Korean actually merged there.
    import strip_quote as SQ
    SQ.apply_all(out)

    # ---- in-place tables ----
    # ⚠ ORDERING. Everything below this line RELOCATES overlay 14 (expand_overlay
    # moves the file and rewrites the FAT). insert_tables writes at the recorded
    # ROM file offset, and its `verify_offset` gate still passes there after a
    # relocation -- the old copy keeps the original Japanese, it is just dead.
    # So running it afterwards wrote 311 file-30 rows into bytes the game never
    # loads: the encyclopedia name/index labels shipped in Japanese while the
    # build log happily reported them written. Any in-place writer MUST run
    # before the first expand.
    # DIAGNOSTIC PPKP9_NO_TABLES=1: skip insert_tables + insert_pointered +
    # insert_profiles entirely. Those three are the ONLY thing in the build that
    # RELOCATES AND GROWS OVERLAY 14 (FAT[30]: 131,281 -> 162,907 B), and they run
    # in every build ever shipped, including v0.9 and every session-35 diagnostic
    # (they are downstream of PPKP9_NO_REDIRECT / PPKP9_MTE_MAX / PPKP9_NO_EXT, so
    # none of those four A/B builds removed them). Session 24 measured that the
    # match dies on overlay SIZE, not content -- and this is a size change nobody
    # has ever turned off. Korean ability names / encyclopedia stay Japanese in
    # this build; the only question it answers is whether the match still dies.
    # ★★ SESSION 36 RESULT (user A/B on a real match, 장타까지 확인):
    #   v101 (all three off)      -> match plays fine, long hits included
    #   v100 (all three on)       -> emulator dies, same as the shipped build
    # So the crash lives in this block. Of the three, ONLY `insert_pointered`
    # (fids 18/30/13/4) and `insert_profiles` (fid 30) change an overlay's SIZE --
    # they grow OVL 8/14/5/29. `insert_tables` writes in place and moves nothing.
    # `PPKP9_NO_POINTERED=1` therefore keeps every in-place table and drops exactly
    # the growth, which is the shipping candidate; `PPKP9_NO_TABLES=1` stays as the
    # bigger hammer that also drops the in-place tables.
    # `PPKP9_POINTERED=18,30` restricts insert_pointered to the listed file ids so
    # the four can be bisected one at a time.
    NO_TABLES = os.environ.get("PPKP9_NO_TABLES") == "1"
    NO_POINTERED = NO_TABLES or os.environ.get("PPKP9_NO_POINTERED") == "1"
    if NO_TABLES:
        print("DIAGNOSTIC PPKP9_NO_TABLES: no in-place tables, no pointered "
              "tables, no encyclopedia -- overlay 14 keeps its retail size")
        tbl = {"written": 0, "skipped": 0}
    else:
        tbl = IT.apply_all(out)
    print(f"text tables: {tbl['written']} rows written, "
          f"{tbl['skipped']} skipped (do not fit)")

    # ---- pointered tables ----
    # Ability names reached through the pointer array get their Korean in the
    # overlay's grown tail instead of inside the record, so length stops
    # mattering. That is what makes 「슬로스타터」/「포커페이스」 possible at all --
    # in-place they were capped at three syllables, and the long originals were
    # never even extracted. Growing stays inside the RAM group's largest overlay,
    # so it costs no RAM and does not touch the scenario arena.
    _only = os.environ.get("PPKP9_POINTERED")
    if NO_POINTERED:
        _ptab = ()
        print("DIAGNOSTIC PPKP9_NO_POINTERED: no pointered tables, no "
              "encyclopedia -- every overlay keeps its retail size")
    elif _only is not None:
        _ptab = tuple(int(x) for x in _only.split(",") if x.strip())
        print(f"DIAGNOSTIC PPKP9_POINTERED: pointered tables limited to {_ptab}")
    else:
        _ptab = tuple(IP.TABLES)
    for _fid in _ptab:
        out, _n, _m = IP.apply(bytes(out), _fid, enc)
        out = bytearray(out)

    # ---- encyclopedia records (pointered, so length is free) ----
    # `line FA line FA … FF` records reached through file 30's pointer arrays.
    # A separate pass from insert_pointered, whose matcher decodes a flat 32-byte
    # window and cannot see the FA newline at all.
    # Runs LAST on purpose: insert_pointered reads and rewrites the same arrays at
    # their retail offsets and has no rebasing, so it has to see the file where it
    # expects it. This pass rebases itself (insert_profiles.ORIG_LO).
    # ---- file 8's shared messages (pointered, so length is free) ----
    # Pitch/ability/item names and the shop lines. Katakana is 1 byte and Hangul
    # is 2, so in place they were structurally impossible -- 12 of 554 shipped.
    # Their records are pointed at, so they move to the tail instead.
    import insert_file8 as IF8
    # ⭐ Session 35: the RELOCATION is what floods the ability panel, not the
    # Korean -- 「근력」 rendered correctly there before the flood started, and the
    # flood is kana, i.e. not our tail blob read back. So ship the 99 records
    # whose Korean fits their original run WITHOUT moving anything: same length,
    # same layout, no overlay growth, no pointer rewrite. `apply_inplace` refuses
    # any target overlapping a live overlay pointer, which is the session-29
    # save-wipe hazard this file is banned for.
    for _fid in IF8.SHIP_INPLACE:
        IF8.apply_inplace(out, _fid, enc_plain)
    # The 114 records whose Korean is longer than the run it replaces cannot stay
    # put. Appending them past the overlay is what floods the panel, so try the
    # padding INSIDE the file instead (1,729 B that no pointer names). Opt-in with
    # PPKP9_FILE8_RELOC=1 until a screen confirms it.
    for _fid in IF8.SHIP_RELOC:
        IF8.apply_relocate(out, _fid, enc_plain)
    # The pointer-less rows. Must run BEFORE `apply()`, which relocates the file:
    # these offsets are rebased through the live FAT, and writing after the move
    # would land in the dead pre-relocation copy -- the exact mistake the
    # `insert_extra` note records ("97 written" into bytes the game never loads).
    # ⭐ SESSION 38. This used to be gated on `IF8.SHIP`, the RELOCATING path,
    # which is off by default -- so the orphan rows never ran in any build. They
    # are the rows no pointer names, and they carry 「下がった」/「上がった」 at
    # 0x44EED9: that is why 「파워가 ５下がった」 kept its Japanese verb while the
    # noun beside it was Korean. `apply_orphans` carries the session-29 save-wipe
    # guard itself (it refuses any target overlapping a live overlay pointer), so
    # it does not need the relocating path's permission -- only file 8 being
    # written in place at all, which is `SHIP_INPLACE`.
    # ⛔⛔ SESSION 41 -- THIS GATE MEANT `apply_orphans` STILL NEVER RAN.
    # Session 38 found the pass wired behind the RELOCATING path and "fixed" it by
    # widening the condition from `IF8.SHIP` to SHIP|SHIP_INPLACE|SHIP_RELOC. All
    # three of those default to `()`, so the union is EMPTY and the loop body was
    # still dead -- the same bug, one layer out. `SHIP_ORPHAN` defaults to (8, 20)
    # and was being ignored entirely.
    # Symptom the user photographed on v177: 「파워가 ５下がった」. The Korean 「감소」
    # is sitting in file8_extra.tsv at 0x44EED9 and `verify_strings` says that exact
    # offset is still the original Japanese in the built ROM; same for 「上がった」
    # (f8 x4 sites). Nothing else writes them -- insert_extra ships (4,25,27) and
    # SHIP_LATE (18,20,30), and they fit inline so the tail region does not take them.
    # `apply_orphans` needs no permission from the relocating path: it carries the
    # session-29 save-wipe guard itself (refuses any target overlapping a live
    # overlay pointer), which is the only reason file 8 was ever gated.
    for _fid in IF8.SHIP_ORPHAN:
        IF8.apply_orphans(out, _fid, enc_plain)

    # ---- runtime-assembled status lines: drop the Japanese particle ----------
    # 「[스탯] が [수] 감소」 is assembled at run time (`F8 07` picks the label from
    # a variable slot, so its operand is one of only TWO values -- not a per-stat
    # constant). Nothing at build time knows which label lands there, so 은/는 ·
    # 이/가 cannot be chosen; see josa_absorb.runtime_particle_sites.
    # USER DECISION (session 43): blank it. 「힘 ５ 감소」 is idiomatic Korean for a
    # stat readout, and 0x00 is the engine's own narrow blank -- no new code, one
    # byte per site, against a render_char hook + a 512 B batchim bitmap for 10
    # sites. `PPKP9_NO_JOSA_BLANK=1` restores the Japanese particle for A/B.
    if os.environ.get("PPKP9_NO_JOSA_BLANK") != "1":
        import josa_absorb as JA
        _w = json.load(open(os.path.join(SURVEY, "ov28", "opcode_lengths.json"),
                            encoding="utf-8"))
        _pri = open(ROMSRC, "rb").read()
        for _fid in (4, 8, 18, 20, 25, 27, 30):
            JA.blank_runtime_particles(out, _fid, _pri, _w)
    f8 = {"written": 0, "pointers": 0, "skipped": 0}
    for _fid in IF8.SHIP:
        r = IF8.apply(out, _fid, enc_plain)
        for k in f8:
            f8[k] += r[k]
    if f8["written"]:
        print(f"shared messages (files {IF8.SHIP}): {f8['written']} records "
              f"repointed, {f8['pointers']} pointers rewritten, "
              f"{f8['skipped']} rejected")

    import insert_profiles as IPF
    prof = ({"written": 0, "skipped": 0} if NO_POINTERED
            else IPF.apply(out, enc_plain))
    if prof["written"]:
        print(f"encyclopedia records: {prof['written']} written, "
              f"{prof.get('pointers', 0)} pointers rewritten, "
              f"{prof['skipped']} rejected")

    # ---- files 18/20/30: the inline rows the FF rule was blocking -------------
    # Second `insert_extra` call, deliberately AFTER the three record passes
    # above (they all match the original Japanese at an offset, so Korean written
    # first would starve them).
    # These files used to ride on `PPKP9_EXTRA_ALL=1` inside `SHIP`, where the
    # per-FILE exact-length rule left them almost nothing to write. Session 41
    # measured what that cost on v162: 197 rows whose Korean already fitted the
    # budget shipped as Japanese -- 117 in file 30, 57 in 20, 23 in 18 -- while
    # every gate reported green. The rule is now per RUN (only a raw `FF`
    # introducer means "chain entry"), and these three moved here.
    if IX.SHIP_LATE:
        late = IX.apply_all(out, enc_plain, files=IX.SHIP_LATE)
        print(f"extra (files {IX.SHIP_LATE}): {late['written']} written, "
              f"{late['skipped']} too long, {late['mismatch']} offset mismatch, "
              f"{late['refused']} refused (pointer array)")
        if not late["written"]:
            raise SystemExit("insert_extra SHIP_LATE wrote nothing -- a pass that "
                             "reports no work done is a failed pass (see RESUME §5)")

    # ---- header 0x80 must cover EVERY relocated file ----
    # ---- ③ per-overlay regions: growth probe -------------------------------
    # Files 4 and 27 carry 6,369 translated lines with no redirect path, because
    # the region lives in overlay 28's tail and overlays 28/29/30 are mutually
    # exclusive. They all load at the SAME RAM base, so each can hold its own
    # region at the SAME address -- no hook change, no new escape form.
    #
    # Before building three regions, prove the ROM tolerates the growth at all.
    # `PPKP9_GROW_OV=27:0x8000` pads file 27 out to the shared region base and
    # appends that many zero bytes. If the game still boots and plays, the
    # structural half of ③ is settled and only the region content remains.
    _grow_ov = os.environ.get("PPKP9_GROW_OV")
    if _grow_ov:
        import expand_overlay as XO
        _heap = X.HEAP_BASE + grow          # expand_rom bumped the literal by `grow`
        for _spec in _grow_ov.split(","):
            _fid, _sz = _spec.split(":")
            out = bytearray(XO.expand_to(bytes(out), int(_fid),
                                         R.REGION_BASE - R.EXT_PAGE_BYTES,
                                         b"\x00" * int(_sz, 0), _heap)[0])

    # ---- ③ the real thing: a region per side overlay ------------------------
    # `PPKP9_SIDE_REGION=27` or `=4,27`. Runs LAST, after `insert_pointered`
    # has finished relocating overlay 29, so the offsets `side_region.plan`
    # reads from the live FAT are the ones that survive into the file.
    # ⭐ SESSION 39: ON BY DEFAULT. Session 38 built this and left it behind an
    # env var because it had never been played. It has now: `japanese left` goes
    # 228,851 -> 69,335 occurrences (52.1% -> 85.5% replaced) and the Korean
    # renders in サクセス on hardware (`_states_s39/v148_story.png`). It is by far
    # the largest single win available -- 7,828 of the 9,218 runs that HAVE a
    # translation and were still showing Japanese are files 4 and 27.
    # `PPKP9_NO_SIDE_REGION=1` turns it off for A/B work.
    _side = os.environ.get("PPKP9_SIDE_REGION", "4,27")
    if os.environ.get("PPKP9_NO_SIDE_REGION") == "1":
        _side = ""
    if _side:
        import expand_overlay as XO
        import side_region as SR
        _heap = X.HEAP_BASE + grow
        for _fid in (int(x) for x in _side.split(",") if x.strip()):
            _region, _writes, _st = SR.build(out, _fid, enc_plain)
            for _off, _esc, _bud in _writes:
                # Pad with 0x00, not REDIRECT_PAD: `aim_filler` exists to widen
                # the ARM9 measurement scanner's box, and these runs are drawn by
                # overlay 1's engine, which never consults that scanner.
                out[_off:_off + _bud] = _esc + b"\x00" * (_bud - len(_esc))
            # The absorbed particle now sits at the end of the name's region
            # entry, so the script copy must go -- 0x00 is the engine's own
            # narrow blank (see the `absorb` note above), and the line closes up.
            for _q in _st.get("blanks", []):
                out[_q] = 0x00
            out = bytearray(XO.expand_to(bytes(out), _fid,
                                         R.REGION_BASE - R.EXT_PAGE_BYTES,
                                         ext_blob + _region, _heap)[0])
            json.dump(_st["manifest"],
                      open(os.path.join(SURVEY, f"side_manifest_{_fid}.json"), "w"))
            print(f"side region file {_fid}: {_st['entries']}/{_st['runs']} runs "
                  f"redirected ({_st['banked']} banked), region {_st['bytes']:,}B"
                  + (f", {len(_st['blanks'])} particles absorbed"
                     if _st.get("blanks") else ""))

    # ---- ④ a region in an overlay's OWN tail (file 30) ----------------------
    # `side_region` only works for the ov28/29/30 group, which shares one RAM
    # base and can therefore share REGION_BASE. Overlay 14 loads below it and
    # cannot be padded up without running through overlay 28's RAM. What makes
    # this possible is the session-39 escape change: the long form now carries
    # `address - RET_BASE`, so it can name a region anywhere in main RAM.
    # ⚠ Runs LAST -- after insert_profiles has finished relocating overlay 14 --
    #   so the tail address it appends at is the one that survives into the file.
    # ⚠ These rows are drawn by the ARM9 printer, so they only render with
    #   menu_hook installed (PPKP9_CHOICE_REDIRECT=1).
    _tail = os.environ.get("PPKP9_TAIL_REGION", "30" if CHOICE_REDIRECT else "")
    for _fid in (int(x) for x in _tail.split(",") if x.strip()):
        try:
            import expand_overlay as XO
            import tail_region as TR
            _e, _oid, _oram, _osize = XO.overlay_of_file(bytes(out), _fid)
            _obss = int.from_bytes(out[_e + 12:_e + 16], "little")
            _tail_ram = _oram + _osize + _obss
            _reg, _writes, _st = TR.build(out, _fid, enc_plain, _tail_ram)
            for _off, _esc, _bud in _writes:
                out[_off:_off + _bud] = _esc + bytes(1) * (_bud - len(_esc))
            out = bytearray(XO.expand_to(bytes(out), _fid, _tail_ram, _reg,
                                         X.HEAP_BASE + grow)[0])
            # ⛔ encoding="utf-8" is REQUIRED: this box's default is cp949 and
            # the manifest carries Japanese, so the dump raises and the `except`
            # below swallows it -- the pass silently does nothing while every
            # gate still reports green.
            json.dump(_st["manifest"],
                      open(os.path.join(SURVEY, f"tail_manifest_{_fid}.json"),
                           "w", encoding="utf-8"),
                      ensure_ascii=False)
            print(f"tail region file {_fid}: {len(_writes)}/{_st['runs']} runs "
                  f"redirected, region {_st['bytes']:,}B at RAM 0x{_tail_ram:08X}"
                  + (f", {_st['refused']} refused (pointer array)"
                     if _st.get("refused") else ""))
        except Exception as _e2:
            # Loud, not a footnote. A silently skipped pass produces a build
            # whose gates are all green and whose text never changed.
            import traceback as _tb
            _tb.print_exc()
            raise SystemExit(f"tail region f{_fid} FAILED: {_e2}")

    # ⛔⛔ SESSION 36. `expand_rom.expand()` declares the used size for the file IT
    # moves (overlay 28) -- and then `insert_pointered` / `insert_profiles` run
    # AFTERWARDS and relocate four more overlays past that mark. Every build ever
    # shipped therefore claims the ROM ends at 0x2B43800 while overlays 5/8/14/29
    # live up to 0x2CB4F13. The correlation with the match crash is exact:
    #   v101 (max FAT end <= used size)  -> match plays fine
    #   v100 / v91 / v0.9 (files past it) -> emulator dies
    # so this is re-declared here, after the last relocation, from the FAT itself
    # rather than from whatever the last mover happened to know.
    # ---- session 45: file 25's extra-region, in the grow's reserved tail -----
    # Same machinery as the tail regions above, but the space is INSIDE ov28's
    # grow (reserved next to the grow computation), because ov28's own tail ends
    # at the heap base and cannot be extended. The long escape names an absolute
    # RAM address, so entries living below the heap work exactly like a tail.
    if F25_RESERVE:
        import expand_overlay as XO
        import tail_region as TR
        _e25, _oid25, _oram25, _osize25 = XO.overlay_of_file(bytes(out), 25)
        _res_ram = _oram25 + _osize25 - F25_RESERVE
        _reg25, _wr25, _st25 = TR.build(out, 25, enc_plain, _res_ram)
        if len(_reg25) > F25_RESERVE:
            raise SystemExit(f"f25 region {len(_reg25)}B > reserve {F25_RESERVE:#x}"
                             " -- raise PPKP9_F25_RESERVE (moves cheat delta!)")
        for _off, _esc, _bud in _wr25:
            out[_off:_off + _bud] = _esc + bytes(1) * (_bud - len(_esc))
        _fat25 = int.from_bytes(out[0x48:0x4C], "little")
        _lo25 = int.from_bytes(out[_fat25 + 25 * 8:_fat25 + 25 * 8 + 4], "little")
        _fo25 = _lo25 + _osize25 - F25_RESERVE
        out[_fo25:_fo25 + len(_reg25)] = _reg25
        json.dump(_st25["manifest"],
                  open(os.path.join(SURVEY, "tail_manifest_25.json"), "w",
                       encoding="utf-8"), ensure_ascii=False)
        print(f"f25 extra region: {len(_wr25)}/{_st25['runs']} runs redirected, "
              f"region {len(_reg25):,}B at RAM 0x{_res_ram:08X} (inside the grow)"
              + (f", {_st25['refused']} refused (pointer array)"
                 if _st25.get("refused") else ""))

    # ---- session 45: 2-byte runs -- one Korean syllable, OFFSET-keyed --------
    # A run whose budget is 2 bytes cannot hold a redirect escape (3B minimum),
    # so its only Korean form is a single syllable -- and that per-OFFSET ko can
    # ride neither `extra_overrides` (Japanese-keyed: would retranslate every
    # おい in the file) nor `sites()` (one ko per jp string). This pass reads
    # survey/common/short_runs.tsv (fid, pristine offset, jp, ko) and writes in
    # place behind the same want-gate insert_extra uses. Exact length only --
    # no padding, no structure change, so the ROM layout is untouched.
    _srp = os.path.join(SURVEY, "common", "short_runs.tsv")
    if os.path.exists(_srp):
        import insert_extra as _IXS
        _sn = _ss = 0
        for _ln in open(_srp, encoding="utf-8").read().splitlines()[1:]:
            if not _ln.strip() or _ln.startswith("#"):
                continue
            _fs, _os_, _jp, _ko = (_ln.split("\t") + [""])[:4]
            _want = _IXS.encode_jp(_jp)
            _kb = enc_plain.encode(_ko)
            _at = int(_os_, 16) + _IXS.rebase(out, int(_fs))
            if bytes(out[_at:_at + len(_want)]) != _want or len(_kb) != len(_want):
                _ss += 1
                continue
            out[_at:_at + len(_kb)] = _kb
            _sn += 1
        print(f"short runs: {_sn} written, {_ss} skipped")

    # Turn off the kanji-input dictionary whose glyphs alloc_plan just took.
    # Reclaiming those 966 kanji is what makes the syllable budget fit, but it
    # would leave the サクセス name-entry keyboard offering Hangul where a kanji
    # candidate belongs. Repointing every reading at an empty candidate list puts
    # the keyboard in a state the ORIGINAL game reaches for 4,342 of its 5,439
    # readings, so no new code path is involved. See tools/disable_ime.py.
    # ⚠ Runs on `out` but plans from the pristine ROM -- the index table must be
    # read before anything else in this build could have touched it.
    if os.environ.get("PPKP9_KEEP_IME") != "1":
        import disable_ime as DI
        _n, _empty = DI.apply(out, pristine=open(ROMSRC, "rb").read())
        print(f"kanji IME: repointed {_n} index entries at the empty list "
              f"@RAM 0x{_empty:08X} (conversion off)")

    _fat = int.from_bytes(out[0x48:0x4C], "little")
    _nfat = int.from_bytes(out[0x4C:0x50], "little") // 8
    _maxend = max(int.from_bytes(out[_fat + i * 8 + 4:_fat + i * 8 + 8], "little")
                  for i in range(_nfat))
    _used = int.from_bytes(out[0x80:0x84], "little")
    if _maxend > _used:
        X._declare_used_size(out, _maxend)
        print(f"  (header used size was 0x{_used:X} but files reach 0x{_maxend:X})")

    open(ROMOUT, "wb").write(out)

    # Gate: walk the LIVE pointer arrays in the finished ROM and confirm each
    # translated record is actually reachable. Every other gate here checks bytes
    # at an offset we chose, which is exactly what let two relocation bugs ship --
    # the bytes were right and the game read somewhere else.
    if f8.get("written"):
        import subprocess as _sp
        _r = _sp.run([sys.executable,
                      os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "verify_file8.py"), ROMOUT],
                     capture_output=True, text=True)
        print((_r.stdout or "").rstrip())
        if _r.returncode:
            print((_r.stderr or "").rstrip())
            raise SystemExit("file 8 pointer-only verify FAILED")
        # …and the other half of the question. `verify_file8` proves we broke
        # nothing; this proves the game can REACH the Korean, by resolving each
        # rewritten pointer through the finished ROM's own FAT and decoding the
        # record it lands on. A written-count has fooled this project twice.
        _r = _sp.run([sys.executable,
                      os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "verify_file8_live.py"), ROMOUT],
                     capture_output=True, text=True)
        print((_r.stdout or "").rstrip())
        if _r.returncode:
            print((_r.stderr or "").rstrip())
            raise SystemExit("file 8 live read-back verify FAILED")

    if prof.get("written"):
        import subprocess
        r = subprocess.run([sys.executable,
                            os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "verify_profiles.py"), ROMOUT],
                           capture_output=True, text=True)
        print((r.stdout or "").rstrip())
        if r.returncode:
            print((r.stderr or "").rstrip())
            raise SystemExit("encyclopedia pointer verify FAILED")
    print(f"wrote {ROMOUT}  ({len(out)} bytes)")

    # ---- extra-worklist rows must be readable where the GAME reads them ----
    # `insert_extra` reported "97 written" for file 25 for a whole session while
    # every one of those writes went into a dead pre-relocation copy of overlay
    # 28. A written-count is not evidence. This gate starts from the built ROM's
    # own FAT, so it measures the bytes the game will actually load.
    import verify_extra as VX
    _vok, _vbad = VX.check(ROMOUT)
    if _vbad:
        raise SystemExit(f"{_vbad} extra-worklist rows are NOT at their live "
                         f"offset -- an in-place writer is patching a relocated "
                         f"file at its pristine offset (see insert_extra.rebase)")

    # ---- verify from the patched file ----
    rom2 = open(ROMOUT, "rb").read()
    fat = int.from_bytes(rom2[0x48:0x4C], "little")
    ov_start = int.from_bytes(rom2[fat + 25 * 8:fat + 25 * 8 + 4], "little")
    ov_end = int.from_bytes(rom2[fat + 25 * 8 + 4:fat + 25 * 8 + 8], "little")
    print(f"overlay 28 now at 0x{ov_start:07X}-0x{ov_end:07X} "
          f"({ov_end - ov_start} bytes)")
    # ⚠ Occurrences the region cap dropped are STILL in `fits` -- they keep their
    # original Japanese bytes on purpose (writing the too-long Korean would shift
    # the ROM). Counting them as verify failures made the gate read 25044/25079 on
    # a build with nothing wrong with it, which is exactly how a real corruption
    # would hide. They are excluded here and reported on their own line instead,
    # so any nonzero `bad` now means something actually went wrong.
    bad = 0
    checked = [r for r in fits if r[0] not in dropped_off]
    for off, blen, jp, ko, b in checked:
        want = (R.escape_bytes(R.safe_index(region_idx[off]), blen,
                               region_offs[region_idx[off]])
                if off in region_idx else b)
        got = rom2[ov_start + off:ov_start + off + len(want)]
        if got != want:
            bad += 1
            if bad <= 5:
                print(f"  text verify MISMATCH @0x{off:06X} {jp!r} -> {ko!r}: "
                      f"want {want.hex(' ')} got {got.hex(' ')}")
    print(f"text verify: {len(checked)-bad}/{len(checked)} occurrences byte-exact "
          f"({len(dropped_off)} distinct runs left Japanese by the region cap, "
          f"not checked)")

    # Walk every redirect end to end exactly as the hook will: escape -> offset
    # table -> Korean bytes -> return marker -> the occurrence's own terminator.
    region_off = ov_start + (R.REGION_BASE - R.OV28_RAM)
    rbad = []
    for off, i in region_idx.items():
        si = R.safe_index(i)
        want_esc = R.escape_bytes(si, [b for o, b, j in lines if o == off][0],
                                  region_offs[i])
        esc = rom2[ov_start + off:ov_start + off + len(want_esc)]
        if esc != want_esc:
            rbad.append((off, "escape"))
            continue
        # ⭐ SESSION 39: only tiny/banked entries have a table slot. The long form
        # carries its offset in the escape, so read it back from there -- walking
        # the table for all of them is what made this gate report 1676/17543 on a
        # build whose escapes verified 17543/17543 against the engine's own order.
        if R.OFFSET_ESC and len(want_esc) == R.LONG_BUDGET:
            toff = R.un248(want_esc[2:5]) + R.RET_BASE - R.REGION_BASE
        else:
            toff = int.from_bytes(rom2[region_off + 4 * si:region_off + 4 * si + 4],
                                  "little")
        text, tail = region_entries[i]
        p = region_off + toff
        blen = [b for o, b, j in lines if o == off][0]
        if R.SLIM:
            # entry is `[text][F7 38][u24 offset from OV28_RAM]`
            if rom2[p:p + len(text)] != text:
                rbad.append((off, "text"))
                continue
            m = p + len(text)
            if rom2[m:m + 2] != bytes([R.ESC_B1, R.RET_B2]):
                rbad.append((off, "marker"))
                continue
            back = R.RET_BASE + int.from_bytes(rom2[m + 2:m + 5], "little")
            if back != tail or back != R.OV28_RAM + off + blen:
                rbad.append((off, "return"))
            continue
        if rom2[p:p + len(text)] != text:
            rbad.append((off, "text"))
            continue
        # the marker follows the text immediately -- the alignment slack lives
        # in front of the text, so nothing renderable sits between them
        m = p + len(text)
        if (m - region_off) % 4 or rom2[m:m + 2] != bytes([R.ESC_B1, R.RET_B2]):
            rbad.append((off, "marker"))
            continue
        back = int.from_bytes(rom2[m + 4:m + 8], "little")
        if back != tail or back != R.OV28_RAM + off + blen:
            rbad.append((off, "return"))
    print(f"region verify: {len(region_idx)-len(rbad)}/{len(region_idx)} redirects "
          f"walk escape -> text -> return marker -> original terminator")
    if rbad:
        print(f"  BROKEN: {rbad[:8]}")

    # ⛔ The gate above is NOT enough and shipped a broken ROM for many builds: it
    # walks each escape in the form we WROTE it, while the engine decides the form
    # at runtime from TINY_TBL. Session 35: TINY_TBL was never written, so 738
    # occurrences were dispatched as tiny index 0 and the engine resumed at the top
    # of the script. This re-decodes every escape the way the hook does.
    try:
        import verify_escapes as VE
        if VE.check(ROMOUT):
            print("  ⛔ escape gate FAILED -- do not ship this build")
    except Exception as e:                        # never block a build on the gate
        print(f"  (escape gate skipped: {e})")

    # ⛔ "Translated but not shipped" had NO number anywhere. `left Japanese`
    # counts only the region-cap drops, so ~962 occurrences that were excluded
    # from the redirect for other reasons (session 35: a choice-span heuristic
    # that mislabelled 1,841 runs) stayed Japanese and appeared in no total. The
    # user found them by playing. Read the finished ROM back and say the number.
    try:
        import scan_runs as SR
        _rb = open(ROMOUT, "rb").read()
        _lo = SR.W.fat_lo(_rb, 25)
        _t = R.ram2rom(R.TINY_TBL)
        _tiny = _rb[_t:_t + 256]
        _inv, _tr = SR._inv_map(), SR._batches()
        _stuck = 0
        _unreadable = 0
        for _o, _b, _jp in SR.W.load_runs():
            _wantko = _tr.get(_jp, "").strip()
            if not _wantko:
                continue
            # A run whose recorded boundary predates the canonical width table
            # (quarantined marker rows) can make read_run walk out of range --
            # count it instead of losing the whole metric to one exception.
            try:
                _got, _ = SR.read_run(_rb, _lo, _o, _b, _inv, _tiny)
            except Exception:
                _unreadable += 1
                continue
            if _got.strip() == _jp.strip():
                _stuck += 1
        if _unreadable:
            print(f"  (shipping gate: {_unreadable} runs unreadable -- stale "
                  f"pre-reanalysis boundaries)")
        print(f"shipping gate: {_stuck} runs have a translation but still show "
              f"Japanese (region cap + every other exclusion)")
    except Exception as e:
        print(f"  (shipping gate skipped: {e})")

    # How much of the game still DRAWS Japanese, measured on the built ROM.
    # The shipping gate above only counts runs we have a translation for; this
    # counts everything, which is the number that has to reach zero before the
    # Japanese glyphs can be dropped (and their 165 one-byte kana codes handed to
    # the commonest syllables, worth ~280 KB of script). It also moves whenever
    # PPKP9_REGION_CAP moves, and nothing else reports that.
    # ⛔ THE ONE FAILURE MODE THAT HAD NO GATE. Overlay 28's grow pushes the
    # scenario heap up and past a point the match cannot allocate -- "모드 진입
    # 자체가 안 된다". Sessions 24, 37 and 39 each found it by playing to the
    # screen and hanging. Validated against real builds: v145 (0x83000) hangs,
    # v146 (0x79000) plays to the batter's box.
    try:
        import verify_grow as VG
        _g, _b, _o = VG.grow_of(ROMOUT)
        if _g > VG.SAFE:
            print(f"  ⛔ overlay 28 grow 0x{_g:X} exceeds the verified-playing "
                  f"0x{VG.SAFE:X} -- the match may not start. Lower "
                  f"PPKP9_REGION_CAP, or play to the batter's box before shipping.")
        else:
            print(f"grow gate: overlay 28 grow 0x{_g:X} <= 0x{VG.SAFE:X} "
                  f"(verified playing)")
    except Exception as e:
        print(f"  (grow gate skipped: {e})")

    # Side regions get their own gate: they resolve against a DIFFERENT overlay's
    # copy of the shared RAM base, so overlay 28's region verify says nothing
    # about them.
    for _fid in (int(x) for x in (_side or "").split(",") if x.strip()):
        try:
            import verify_side as VS
            VS.check(ROMOUT, _fid)
        except Exception as e:
            print(f"  (side verify f{_fid} skipped: {e})")

    try:
        import japanese_left as JL
        _jp, _where, _hime, _s, _r = JL.measure(ROMOUT)
        _base, _baseby = JL.baseline()
        _left = sum(_jp.values())
        print(f"japanese left: {_left:,} of {_base:,} occurrences "
              f"({(_base - _left) / _base * 100:.1f}% replaced); "
              f"{sum(_hime.values())} Hangul drawn in the kanji-IME candidate list")
    except Exception as e:
        print(f"  (japanese-left metric skipped: {e})")

    # ⛔ The user's standing requirement: the dialogue must never take a wrong
    # branch again. A wrong branch comes from ONE thing -- a non-text byte being
    # overwritten -- and the opcode gate above proves that for overlay 28 only.
    # Files 4, 8, 18, 20, 27 and 30 are written too and nothing checked them.
    try:
        import verify_writes as VW
        if VW.check(ROMOUT, show=4):
            print("  ⛔ structural bytes changed -- control flow is at risk")
    except Exception as e:
        print(f"  (write gate skipped: {e})")

    tbl2 = F.load_table(rom2)
    gbad = 0
    ext_page_rom = ov_start + (mte_hook.EXT_BASE - R.OV28_RAM)
    for ch, cc in list(mapping["syl"].items()):
        blk = cc // 64
        if blk in mte_hook.EXT_BLOCKS:
            # extension glyphs live in the grown overlay, reached through the
            # font-table swap, so verify them where the stub will read them
            o = ext_page_rom + (blk - mte_hook.EXT_BLOCK0) * 0x900
            g = F.decode_glyph(bytearray(rom2[o:o + 0x900]), cc)
            if g != render(ch):
                gbad += 1
            continue
        g = F.decode_glyph(F.block_region(rom2, tbl2, cc // 64), cc)
        if g != render(ch):
            gbad += 1
    n = len(mapping["syl"])
    print(f"glyph verify: {n-gbad}/{n} exact")

    # ---- decode a few patched spots back through the real encoding ----
    print("\nre-decoded from the patched ROM:")
    shown = set()
    for off, blen, jp, ko, b in fits:
        if jp in shown:
            continue
        shown.add(jp)
        if off in region_idx:
            i = region_idx[off]
            si = R.safe_index(i)
            toff = int.from_bytes(rom2[region_off + 4 * si:region_off + 4 * si + 4], "little")
            data, ret = region_entries[i]
            print(f"  0x{ov_start+off:06X}  {jp!r} -> REDIRECT[{i}] "
                  f"@region+0x{toff:X} -> {enc.decode(data)!r} ({len(data)}B vs "
                  f"{blen}B inline budget, returns to 0x{ret:08X})")
        else:
            data = rom2[ov_start + off:ov_start + off + len(b)]
            print(f"  0x{ov_start+off:06X}  {jp!r} -> {enc.decode(data)!r}  "
                  f"({len(b)}/{blen}B)")
        if len(shown) >= 14:
            break


if __name__ == "__main__":
    main()
