#!/usr/bin/env python3
"""Insert the `file*_extra.tsv` worklists BY OFFSET.

`insert_common.py` finds its runs by re-walking `F8 6B` and matching the Japanese.
The runs in these worklists have no such opener -- they are introduced by `FA`,
`F808`, `F809` and dozens of others -- so they can only be located by the offset
the opcode-aware walk recorded.

Every write is gated the same way `insert_tables` gates its own:
  * the ROM bytes at the offset must still re-encode to the recorded Japanese
  * the Korean must fit the recorded budget (these files have no redirect path)
A row that fails either test is skipped and counted, never forced.

⚠ Files 8 and 20 are NOT written here. Session 29 traced the
「終 / ファイルをけしました」 save-wipe to one of them and it was never pinned down;
until that is bisected, writing anything to them risks the player's save.
"""
import os, re, sys, glob, argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P
import koenc

BASE = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"
COMMON = BASE + r"/survey/common"
# File 25 is overlay 28 -- the main scenario. `extract_all` only kept runs that
# sat inside an `F8 6B` message (its `in_dialogue` gate), so 1,471 runs with a
# usable budget were never even extracted: 「』を喰った！」 (13x), 「体力を１５回復
# します」, 「変化球ポイントが上がりやすくなります」. Same class of miss as the intro
# (111 lines) and the choice options (386 of 512).
# ⭐ SESSION 35: the flood these three were blamed for turned out to be
# TINY_TBL / MTE-code collisions / insert_file8, all fixed now, so the ban is
# worth re-testing. `PPKP9_EXTRA_ALL=1` enables them; the default stays safe
# until a screen confirms it.
SHIP = (4, 25, 27)
# Files 18/20/30 are written by a SECOND call, placed after insert_tables /
# insert_pointered / insert_profiles. All three find their records by matching
# the ORIGINAL Japanese at an offset and all three read these files -- writing
# Korean there first makes them skip the record, which is the failure `skip_off`
# below already documents for insert_profiles. Late is also correct for length:
# those passes only ever move records into an overlay tail, and this pass rebases
# through the live FAT, so it still lands in the live copy.
# (Until session 41 these three rode on `PPKP9_EXTRA_ALL=1` inside `SHIP`, i.e.
# EARLY, where the exact-length rule below left them almost nothing to do.)
# ⛔⛔ FILE 20 IS OUT BY DEFAULT AGAIN — SESSION 41 BISECTED IT TO HERE.
# The user reported two show-stoppers with every gate green: the option screen's
# cursor drawn off its icons, and the prologue skipping its fade and then hanging.
# Bisection: v144 ✅ v145 ✅ v148 ✅ v152 ✅ v153 ✅ | v154 ⛔ — and v154 is exactly
# `PPKP9_EXTRA_ALL=1`, i.e. the build that first wrote files 18/20/30. File 20 is
# the menu/system text file, which is what both symptoms are made of.
# This module's own docstring has warned about file 20 since session 29 ("until
# that is bisected, writing anything to them risks the player's save"); session 40
# switched it on anyway and session 41 promoted it to the default. That was the
# mistake. Turning it back off is the fix, not a workaround.
# `PPKP9_EXTRA_LATE=18,20,30` re-enables per file for whoever bisects further —
# file 20 must not go back in without a NEW-GAME playthrough as evidence.
_late = os.environ.get("PPKP9_EXTRA_LATE")
SHIP_LATE = (() if os.environ.get("PPKP9_EXTRA_ONLY28") == "1"
             else tuple(int(x) for x in _late.split(",") if x.strip()) if _late
             else (18, 30))
# ⛔ Session 29's save wipe was traced to an offset-driven write into file 8 or
# 20 and never pinned down further. `insert_file8.apply_orphans` carries the
# guard that made writing 20 acceptable at all -- refuse any target overlapping
# an aligned u32 that currently points into the overlay, i.e. a live pointer
# array. This pass writes the same kind of file, so it carries the same guard.
GUARDED = (18, 20, 30)
# Whether a run may be padded with 0x00 is a property of the RUN, not the FILE.
# Session 34 photographed a garbage screen after padding a 0xFF-delimited table
# entry and banned files 18/20/30 wholesale. The ban is right about the chain and
# wrong about its reach: the worklist's `opcode` column records what INTRODUCED
# each run, and only `FF` means "raw chain delimiter, budget == len(jp), the FF
# sits just past it". Everything tagged with a VM opcode (FA/FB/F8xx) carries its
# own terminator and takes 0x00 filler exactly like files 4/25/27 -- which is
# what `tail_region` already relies on: its 215 file-30 escapes are written into
# FA/FB runs and 0x00-padded, and session 41 watched them render (album epilogue
# No.33, 「난 이 세계의 신이 된다！」).
# Measured cost of the per-file ban: it blocked 197 rows that already had a
# Korean translation fitting inline -- 117 in file 30, 57 in file 20, 23 in
# file 18 -- to protect 41 real chain entries (10 + 31 + 0).
# A tag that is not a hex opcode at all (`MENU`, 11 rows in file 20) comes from a
# different extractor and its delimiter is unproven, so it is held to the strict
# rule too. `PPKP9_FF_PAD=1` pads everything, including real chain entries.
FF_PAD = os.environ.get("PPKP9_FF_PAD") == "1"
_HEX_TAG = re.compile(r"[0-9A-F]{2,4}\Z")


def encode_jp(s):
    b = bytearray()
    for ch in s:
        cc = P.CH2CC[ch]
        if cc < 231:
            b.append(cc + 1)
        else:
            b += bytes([232 + (cc - 256) // 256, (cc - 256) % 256])
    return bytes(b)


ORIG = (r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/"
        r"Power Pro Kun Pocket 9 (Japan).nds")
_pristine_lo = {}


def _fat_lo(rom, fid):
    fat = int.from_bytes(rom[0x48:0x4C], "little")
    return int.from_bytes(rom[fat + fid * 8:fat + fid * 8 + 4], "little")


def rebase(rom, fid):
    """How far file `fid` has already moved in `rom` since the pristine ROM.

    ⚠⚠ THIS IS WHY FILE 25's ROWS NEVER REACHED THE SCREEN. The worklist offsets
    are pristine ROM offsets, and this pass writes them literally. That is fine
    for a file that has not moved yet -- but overlay 28 (FAT[25]) is grown and
    relocated near the TOP of `build_kr.main`, thousands of lines before this
    runs. The bytes left behind at 0x4CC000 still decode to the recorded
    Japanese, so the `!= want` gate happily passed, the build reported
    "97 written" every time, and every one of those writes went into a copy the
    game never loads. Measured: 97 of 97 Korean strings present at the pristine
    offset, 0 of 97 at the live offset.

    Same class as session 31's `insert_tables` bug, and the same lesson: a
    "written" count from an in-place writer proves nothing. Rebasing through the
    live FAT makes the pass correct wherever it runs in the order.
    """
    if fid not in _pristine_lo:
        _pristine_lo[fid] = _fat_lo(open(ORIG, "rb").read(), fid)
    return _fat_lo(rom, fid) - _pristine_lo[fid]


def rows(fid):
    p = os.path.join(COMMON, f"file{fid}_extra.tsv")
    if not os.path.exists(p):
        return
    for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
        f = ln.split("\t")
        # ⛔ SESSION 45: ASCII-whitespace strip ONLY. str.strip() also eats
        # U+3000, and the choice-preview width fix pads ko with trailing
        # full-width spaces ON PURPOSE (equal sibling widths stop the box
        # from showing the previous line's tail). A bare .strip() silently
        # unshipped every one of those pads.
        if len(f) >= 6 and f[5].strip():
            yield int(f[0], 16), int(f[1]), f[4], f[5].strip(" \t\r\n")


_orig_rom = None
_sites = {}
_batch = None
_strict = {}


def strict_offsets(fid):
    """Pristine offsets whose run must be replaced at EXACTLY its own length.

    A run qualifies when nothing proves it carries its own terminator: the raw
    `FF` chain delimiter, or a tag the opcode walk did not produce at all. Built
    from the same pristine walk `sites()` uses, so every DUPLICATE occurrence is
    classified on its own tag rather than inheriting the worklist row's, and
    unioned with the worklist column so a row the walk no longer reproduces is
    still judged (and, when in doubt, judged strictly).
    """
    if fid in _strict:
        return _strict[fid]
    s = set()
    p = os.path.join(COMMON, f"file{fid}_extra.tsv")
    if os.path.exists(p):
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            f = ln.split("\t")
            if len(f) >= 3 and (f[2] == "FF" or not _HEX_TAG.match(f[2])):
                s.add(int(f[0], 16))
    global _orig_rom
    import walk_file as W
    if _orig_rom is None:
        _orig_rom = open(ORIG, "rb").read()
    lo, hi = W.fat_span(_orig_rom, fid)
    for tag, off, _blen, _t in W.walk(_orig_rom, lo, hi):
        if tag == "FF" or not _HEX_TAG.match(tag):
            s.add(off)
    _strict[fid] = s
    return s


# ⛔ The strict rule NARROWS the session-34 ban, it must never widen it. Files
# 4/25/27 have padded every run since session 34 and their FF-chain consumers
# (`f25/packed`, `f25/array` in `japanese_left`) read 0 occurrences of leftover
# Japanese on v162 -- i.e. those chains are fully Korean and have been shipping
# that way. Applying the per-run test to them as well cost 601 occurrences on
# v163 (f25/packed 0 -> 321, f25/array 0 -> 280) for no reported symptom, which
# is a regression, not a fix. If those chains ever DO need the exact rule, that
# is its own investigation with its own screen.
STRICT_FILES = (18, 20, 30)


_opmap = {}


def opcode_map(fid):
    """Bytes of file `fid` (pristine, file-relative) that belong to an OPCODE.

    ⛔⛔ SESSION 41 — THE PROLOGUE HANG. Walking the built ROM's files with the
    validated opcode table found 140 clobbered control-flow bytes in file 30 and
    20 in file 18. Two different mistakes land there:
      * the introducer itself (`FA`/`FB`/`F9`/`FF`, width 1) — the write STARTED
        one byte early, the shifted-duplicate row problem, never checked on 18/30
      * operands of `FC`/`FD`/`FE` (width 3) — the write RAN PAST the run's end
    Either way the engine stops mid-sequence, which is the 「나오다 마는」 symptom
    the user described, and it is the same family as session 30's `F8 15` (a wrong
    width in opcode_lengths.json let the walker read an operand as text).
    Chasing the individual rows is whack-a-mole; refusing any write that touches a
    control-flow byte fixes both at the source. `build_kr`'s `opcode gate` proves
    the result -- but it only ever checked overlay 28, which is why files 18/20/30
    shipped broken from v154 on with every gate green.
    """
    if fid in _opmap:
        return _opmap[fid]
    import json
    import check_opcodes as CO
    global _orig_rom
    if _orig_rom is None:
        _orig_rom = open(ORIG, "rb").read()
    lo, hi = _fat_lo(_orig_rom, fid), 0
    fat = int.from_bytes(_orig_rom[0x48:0x4C], "little")
    hi = int.from_bytes(_orig_rom[fat + fid * 8 + 4:fat + fid * 8 + 8], "little")
    L = json.load(open(os.path.join(BASE, "survey", "ov28",
                                    "opcode_lengths.json"), encoding="utf-8"))
    _opmap[fid] = (lo, CO.opcode_bytes(_orig_rom, lo, hi,
                                       {int(k): v for k, v in L["bare"].items()},
                                       {int(k): v for k, v in L["f8"].items()}))
    return _opmap[fid]


def hits_opcode(fid, off, budget):
    """True if [off, off+budget) would overwrite a control-flow byte."""
    lo, mp = opcode_map(fid)
    return any(mp[k] for k in range(off - lo, min(off - lo + budget, len(mp)))
               if k >= 0)


def needs_exact(fid, off):
    """True if the run at pristine offset `off` may not be 0x00-padded."""
    return not FF_PAD and fid in STRICT_FILES and off in strict_offsets(fid)

# The SECOND half of the 「공용 텍스트」 bug, and it hides inside the extractor's
# own definition of "done". `extract_extra.walk` skips a run `if t in tr`, and
# `walk_file.translated()` counts the whole batch corpus -- so a string that was
# translated for overlay 28 was declared finished and NEVER WRITTEN INTO THE
# WORKLIST OF ANY OTHER FILE. 「商店街」 is the one the user can see: batch120 has
# 「商店街 -> 상점가」, the map draws it from file 20 @0x2A2A30, and no worklist
# mentions that offset, so the map reads 「『商店街』간다」 -- Korean verb, Japanese
# place name, in one box. Measured outside overlay 28: 2,858 such sites.
# ⚠ These strings were translated in overlay 28's context, never reviewed in this
# file's. The write is held to the same three gates as everything else here (the
# validated opcode walk found the run, the live bytes still re-encode to the
# recorded Japanese, the Korean fits the budget) plus the two below, and overlay
# 28 itself is excluded -- its inline bytes belong to the redirect machinery and
# the text/region gates check them byte-for-byte.
#
# SESSION 38 STATUS: UNTESTED, not condemned. `PPKP9_kr_v126_batchsites.nds`
# passes every build gate and fixes the map to 「『상점가』간다」. A block-glyph box
# was photographed on it and first written up here as a regression -- that was
# WRONG, and the probe that retracted it is worth keeping:
#   * font pointer table in RAM == ROM (68/68), Hangul glyph data in RAM == ROM
#   * render_char is handed a valid Hangul charcode from overlay 1's engine
#   * all 1,881 charcodes this switch writes resolve to a real glyph (static scan)
#   * v125 and v126 differ in ZERO bytes inside file 25 -- and 「新装開店でーす！」,
#     the line that was supposedly corrupted, lives in file 25
#   * the two emulator runs had provably different frame counts (press_buttons is
#     wall-clock, not frame-exact), so they were not the same random event
# What is still missing is a FRAME-EXACT replay: until an A/B runs the same input
# on both ROMs, no on-screen difference here means anything. Use tap/tap_sequence
# (deterministic while frozen), not press_buttons.
BATCH_SITES = os.environ.get("PPKP9_BATCH_SITES") == "1"
# ⛔⛔ SESSION 43 — FILE 30 IS EXCLUDED, AND THE REASON IS A SHIPPED HANG.
# The user hit an EMPTY dialogue box that never advances, four lines into the
# prologue on a new game. Bisected on hardware: v180 walks past it, v181 does
# not, and the ONLY difference that touches file 30 is `PPKP9_BATCH_SITES=1`.
# What it does there: the batch corpus matches 142 more sites in file 30, and
# 0x3253CC..0x3267xx is not script at all -- it is a CHARACTER-NAME ARRAY
# (武美 · 向井 · ゴルトマン · ソルジャー …). Two of those names are over budget
# in Korean, so `tail_region` took them over and wrote a 5-byte redirect escape
# INTO THE ARRAY (0x326495 「ゴルトマン」, 0x326775 「フグ怪人」).
# ⚠ THE MECHANISM IS NOT PROVEN, ONLY THE CAUSE. The obvious story ("that array
# has a consumer that cannot read our escape") does NOT follow from "it is a bank
# string": measured on the WORKING build, file 30 already carries 516 escapes on
# pointer-owned strings, file 18 carries 121 and file 20's map names are 3 of
# them -- all verified on hardware. So a bank string is not by itself unsafe, and
# whatever breaks here is narrower (a different consumer for THIS array -- the
# overlay-1 name walker at 0x020C3838 is the candidate, unhooked, but untested).
# Do not generalise this into "no escapes on bank strings"; that would delete 640
# working redirects.
# Verified: `PPKP9_BATCH_SITES` off with everything else from v191 (v192) walks
# the same path fine, file 30's tail region back to 699 entries like v180.
# ⇒ Re-enabling file 30 needs a span filter that can tell script from array
#   (master.tsv's `kind` column knows), not just this switch.
BATCH_EXCLUDE = tuple(int(x) for x in os.environ.get("PPKP9_BATCH_EXCLUDE","25,30").split(",") if x.strip())


def _has_jp(s):
    return any(0x3040 <= ord(c) <= 0x30FF or 0x4E00 <= ord(c) <= 0x9FFF
               for c in s if c not in "・ー")


def batch_map(fid):
    """jp -> ko from the batch corpus, for files whose worklist never saw it."""
    global _batch
    if not BATCH_SITES or fid in BATCH_EXCLUDE:
        return {}
    if _batch is None:
        import glob, re
        tdir = os.path.join(BASE, "translation")
        names = ["common_lines.tsv"] + [
            os.path.basename(p) for p in
            sorted(glob.glob(tdir + "/batch*.tsv"),
                   key=lambda p: int(re.search(r"batch(\d+)\.tsv$", p).group(1)))]
        _batch = {}
        for n in names:
            for ln in open(f"{tdir}/{n}", encoding="utf-8").read().splitlines()[1:]:
                if "\t" not in ln:
                    continue
                jp, ko = (ln.split("\t") + [""])[:2]
                jp, ko = jp.strip(), ko.strip()
                # A row whose Korean still carries kana/kanji is a half-finished
                # line (「いあ -> い아」). Fine as a hint in a worksheet, not as a
                # blind write into a file nobody reviewed it against.
                if jp and ko and not _has_jp(ko):
                    _batch[jp] = ko
    return _batch


# Minimum encoded length of the ORIGINAL run for writing at every walked
# occurrence (session 45, see comment inside `sites()`). 4 bytes ~ 1e-4 chance
# matches per file; 2 bytes matched ~20 times in one file. Recorded worklist
# offsets are exempt -- they were extracted, not pattern-matched.
MIN_MULTI_BYTES = int(os.environ.get("PPKP9_MIN_MULTI_BYTES", "4"))


def sites(fid):
    """EVERY occurrence of a translated run in file `fid` (pristine offsets).

    ⭐⭐ SESSION 38 -- this is the 「공용 텍스트」 bug. `extract_extra.py` collapses
    identical strings to ONE row (`best[t]`, keeping the tightest budget), and the
    `occurrences` column records how many it threw away. This pass then wrote that
    single offset, so text that appears N times shipped Korean once and Japanese
    N-1 times. Measured on the pristine ROM: 2,490 such sites across files
    4/8/18/20/25/27/30, 2,326 of them with room for the Korean already in hand.
    The symptom the user reported -- 「대화 로그는 한국어인데 텍스트창은 일본어」, and the
    map's 「『商店街』に行きます」 (7 occurrences, 1 patched) -- is exactly this.

    Sites come from re-walking the PRISTINE ROM with the same validated opcode
    table `extract_extra` used, so the offsets are the same ones the worklist was
    built from; `rebase()` maps them to wherever the file lives now, and the
    per-site `want` gate still has the final say. Budget is per-site: the worklist
    carries the SMALLEST budget of the group, but a wider occurrence can hold more.
    """
    if fid in _sites:
        return _sites[fid]
    global _orig_rom
    import walk_file as W
    tr = {jp: ko for _o, _b, jp, ko in rows(fid)}
    tr.update({jp: ko for jp, ko in batch_map(fid).items() if jp not in tr})
    out = []
    if tr:
        if _orig_rom is None:
            _orig_rom = open(ORIG, "rb").read()
        lo, hi = W.fat_span(_orig_rom, fid)
        seen = set()
        # SESSION 45 -- a pattern this short matches code and data by chance, not
        # just text: 「はい」 (2 encoded bytes, `1a 02`) walked out of file 20 at 20
        # sites, 19 of them false -- BNE opcodes (1A->EB turned them into BLs), a
        # u32 ID array, and the asset table after "start_obj_0.bin". That broke
        # the バンザイ command (and matches the game-over freeze shape). Short rows
        # keep their RECORDED worklist offset only; batch-only strings (no
        # recorded offset) must clear the same bar everywhere.
        rec = {}
        for o, _b, jp, _k in rows(fid):
            rec.setdefault(jp, set()).add(o)
        for _tag, off, blen, t in W.walk(_orig_rom, lo, hi):
            ko = tr.get(t)
            if ko is not None:
                if (len(encode_jp(t)) < MIN_MULTI_BYTES
                        and off not in rec.get(t, ())):
                    continue
                out.append((off, blen, t, ko))
                seen.add(t)
        # A row whose text the walk no longer produces still gets its recorded
        # offset -- never silently drop finished translation work.
        for off, budget, jp, ko in rows(fid):
            if jp not in seen:
                out.append((off, budget, jp, ko))
    _sites[fid] = out
    return out


# `PPKP9_ONE_SITE=1` reverts to the pre-session-38 behaviour (one write per
# distinct string) for bisecting, should a duplicate site ever turn out to be
# data that merely decodes like text.
WORK = rows if os.environ.get("PPKP9_ONE_SITE") == "1" else sites


def apply_all(rom, enc=None, verbose=True, files=SHIP):
    enc = enc or koenc.Encoder()
    tot = skip = bad = 0
    # File 8's rows are POINTERED (insert_file8): its records get moved whole into
    # the overlay tail, where length stops mattering. Writing the same run in
    # place first would leave Korean at the offset that pass gates on, so it
    # would refuse every record it was about to free. The pointer path wins.
    try:
        import insert_file8 as F8
        skip_off = F8.handled_offsets(rom)
    except Exception:
        skip_off = set()
    # Same reason, for file 30: `insert_profiles` runs LAST (it needs the grown
    # tail) and finds every encyclopedia record by matching the ORIGINAL Japanese
    # at its offset. Writing Korean there first made it skip the record and the
    # live-pointer gate reported FAILED -- measured twice in session 34, once via
    # insert_records and once via this pass. Leave those bytes alone.
    try:
        import insert_profiles as PRF
        skip_off |= PRF.handled_offsets(rom)
    except Exception:
        pass
    refused = 0
    for fid in files:
        w = s = b = r = op = 0
        distinct = set()
        delta = rebase(rom, fid)
        ptr = None
        if fid in GUARDED:
            import expand_overlay as XO
            info = XO.overlay_of_file(bytes(rom), fid)
            ptr = (info[2], info[3]) if info else None
        for off, budget, jp, ko in WORK(fid):
            if off in skip_off:
                continue
            at = off + delta                # live offset, not the pristine one
            want = encode_jp(jp)
            if bytes(rom[at:at + len(want)]) != want:
                b += 1                      # offset no longer matches: never write
                continue
            kb = enc.encode(ko)
            if len(kb) > budget:
                s += 1
                continue
            # Session-29 save-wipe guard, for the files that carry pointer arrays
            # (see GUARDED): refuse a target whose bytes currently read as a live
            # overlay pointer. Aligned u32s, because that is how the arrays are
            # written and how `insert_file8.apply_orphans` checks them.
            if ptr and any(
                    ptr[0] <= int.from_bytes(rom[a:a + 4], "little")
                    < ptr[0] + ptr[1]
                    for a in range(at & ~3, at + budget, 4)):
                r += 1
                continue
            # Control-flow guard (see `opcode_map`): never write over an opcode.
            if hits_opcode(fid, off, budget):
                op += 1
                continue
            # Padding byte matters. Files 4/25/27 sit inside an `F8 6B` message
            # that carries its own terminator, so 0x00 filler is harmless. The
            # FF-terminated tables (18/20/30) record budget == len(jp) EXACTLY
            # and the 0xFF sits just past it -- measured session 34: 「はい」
            # budget 2, bytes `1A 02`, next byte `FF`. Filling the slack with
            # 0x00 leaves non-terminator bytes in front of that FF and the table
            # renderer never stops: correct Korean lines then a screenful of
            # garbage (user photo). Terminate our own string instead.
            if needs_exact(fid, off):
                # These tables are a CHAIN of 0xFF-delimited strings and the
                # recorded budget is exactly len(jp), with the FF just past it.
                # Any filler changes the chain: 0x00 is not a delimiter so the
                # renderer reads past the run, and an early 0xFF splits one
                # entry into two so every later entry shifts by one. Both were
                # photographed by the user in session 34 -- correct Korean lines
                # followed by a screenful of garbage. Only an EXACT-length
                # replacement leaves the chain intact.
                if len(kb) != budget:
                    s += 1
                    continue
                rom[at:at + budget] = kb
            else:
                rom[at:at + budget] = kb + b"\x00" * (budget - len(kb))
            w += 1
            distinct.add(jp)
        tot += w
        skip += s
        bad += b
        refused += r
        if verbose:
            print(f"  extra file {fid}: {w} written ({len(distinct)} distinct, "
                  f"{w - len(distinct)} repeat sites), {s} too long, "
                  f"{b} offset mismatch"
                  + (f", {r} refused (pointer array)" if r else "")
                  + (f", {op} refused (opcode)" if op else "")
                  + (f"   [rebased {delta:+#x}]" if delta else ""))
    return {"written": tot, "skipped": skip, "mismatch": bad, "refused": refused}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    rom = bytearray(open(r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/"
                         r"Power Pro Kun Pocket 9 (Japan).nds", "rb").read())
    st = apply_all(rom)
    print(st)


if __name__ == "__main__":
    main()
