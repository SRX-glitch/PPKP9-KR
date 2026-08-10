#!/usr/bin/env python3
"""Repoint file 8's shared messages so their length stops mattering.

File 8 holds the strings the whole game shares -- pitch names, ability labels and
the status lines (「무언가가 몸에 익었다！」). In place they are hopeless: katakana is
ONE byte per character and Hangul is two, so 「カーブ」 has a 3-byte field that a
Korean 「커브」 already overflows. That is why only 12 of 554 rows ever shipped.

They are not stuck, though -- they are POINTERED. Each record looks like

    F8 22 00   F8 08   <text>   F8 09   F8 22 01   FF
    `---------------' `------'
     wrapper opcodes   the run the worklist records

and a u32 elsewhere in the file points at the record start (usually 5-8 bytes
before the run). Move the record to the overlay's grown tail, rewrite that
pointer, and the Korean may be any length -- the same trick that freed the
encyclopedia in insert_profiles.

Only the text run is replaced; every wrapper opcode is copied through byte for
byte, so colour/size state is untouched.

    python tools/insert_file8.py --report
"""
import json, os, sys, argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poketbl as P
import koenc
import expand_overlay as X

BASE = r"C:/Users/jngji/Desktop/실험실"
COMMON = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/common"
OPLEN = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/ov28/opcode_lengths.json"

# fid -> its FAT start in the RETAIL ROM. Every offset in a worklist was recorded
# against that layout, and by the time this runs the file may already have been
# relocated, so each pass rebases through the live FAT (see insert_profiles).
# File 20 is here for the same reason file 8 is: the practice/ability panel reads
# ITS copy of 「筋力」, not file 8's -- translating file 8 alone changed nothing on
# that screen. Both were banned together over the unproven save wipe, and both
# are pointered, so neither needs an in-place write.
FILES = {8: 0x443200, 20: 0x22DA00}

# ⛔ FILE 20 IS SHIPPED OUT — measured, not guessed. Growing ov9 puts our tail at
# RAM 0x0214AA60, immediately past the overlay's end (0x020CA020 + 0x80A00), and
# **the game uses that memory at runtime**. Dumping it live shows our records
# interleaved with counter tables and asset paths (`/FsBin/iwasaki/bg/sc1bg21.bin`),
# and 「돌아갑니다」's first two bytes had been zeroed, so the walker drew a blank and
# then 「아갑니다」 -- pointer right, record right in ROM, clobbered in RAM.
# ov23 (file 8) does NOT show this: its 근력 record reads back byte-for-byte at
# 0x021AB6BD. Group headroom (`GROUP_MAX`) says nothing about whether the bytes
# after an overlay are free -- the same trap that killed the region-relocation
# plan in session 30. File 20's worklist and translations are kept for whenever a
# genuinely free home exists; its menu strings go back through `insert_tables`.
# 세션35: 세션34 막바지에 «폭주 원인 확인용»으로 ()로 껐던 것을 되돌렸다. 그 실험은
# 검증되지 않은 채 끝났고(v73, SHA1 627ba100, 화면 미확인), 그 사이 파일8 레코드 212개가
# 통째로 미출하 상태였다. 폭주의 원인은 그 뒤 사용자 실기 A/B로 «파일18/20/30을 켠 것»으로
# 확정됐으므로(RESUME.md ★★★★ 최종 확정) 파일8을 끌 이유가 없다.
# ⛔⛔ SESSION 35, SETTLED BY A USER A/B ON HARDWARE: the pointer path is what
# floods the training-result / ability panel. On v80 (this tuple empty, everything
# else identical to v79) the screen reads cleanly -- 「練習が終わった！／体力ガ ２６
# 下がった／筋力ガ １２上がった」 in Japanese, no garbage. With 8 enabled the same
# screen printed 「근력ガ　１２上がった」 and then a screenful of kana. The flood text
# is kana, not Hangul, so the walker is NOT reading our tail blob -- and file 8's
# records sit CONTIGUOUSLY (`00 | F8 5A n | F8 08 text F8 09 | F8 23 00 | FF`
# repeating), so moving one to the overlay tail breaks "the next record is right
# behind me" for whatever reads them as a sequence.
# Sessions 29-34 blamed the font tables, the FF chains and files 18/20/30 for this.
# It was here. ⛔ Do not re-enable without a path that keeps the records adjacent.
# The 213 translations stay in the worklist, so nothing is lost.
# ★★★ SESSION 36 — BOTH BANS ABOVE RESTED ON A BUG THAT IS NOW FIXED.
# `X.expand()` used to drop the tail blob at `ram + size`, which is EXACTLY where
# the NDS loader starts an overlay's `.bss`. Check the two addresses the notes
# above quote against the retail overlay table:
#   file20 -> OVL 9,  ram 0x020CA020 + size 0x80A40 = **0x0214AA60**, bss 8,320
#             = the very address session 35 dumped and found "interleaved with
#               counter tables", with 「돌아갑니다」's first two bytes zeroed.
#               That was the loader zeroing .bss on top of our record. Not a
#               mystery consumer of "the memory after an overlay" -- it was ours.
#   file8  -> OVL 23, ram 0x021992C0 + size 0x117A0 = 0x021AAA60, bss only 32
#             = the blob buried all 32 bytes of that overlay's .bss and the
#               zero-fill slid up past them. 「근력」 at 0x021AB6BD sits above the
#               damage, which is why the record read back byte-for-byte while the
#               panel still flooded with KANA -- the walker had lost its state,
#               so it was reading raw file bytes, not our Hangul blob. The
#               "records must stay adjacent" theory was never needed.
# `expand()` now places the blob ABOVE the bss and lets the file's own zeros
# initialise it, so neither overlay loses a byte of .bss.
# `PPKP9_FILE8=1` -> file 8 only; `PPKP9_FILE8=8,20` -> both.
_f8 = os.environ.get("PPKP9_FILE8", "")
SHIP = ((8,) if _f8 == "1" else
        tuple(int(x) for x in _f8.split(",") if x.strip()) if _f8 else ())
FID = 8                     # default for the CLI
ORIG_LO = FILES[FID]
END = 0xFF
MAXREC = 256


def work_path(fid):
    return f"{COMMON}/file{fid}_extra.tsv"


def encode_jp(s):
    b = bytearray()
    for ch in s:
        if ch == " ":
            b.append(0)          # the game's space is a raw 0x00, not a charcode
            continue
        cc = P.CH2CC[ch]
        b += (bytes([cc + 1]) if cc < 231
              else bytes([232 + (cc - 256) // 256, (cc - 256) % 256]))
    return bytes(b)


def _oplen():
    """(f8 widths, bare widths). ⚠ The JSON keys are DECIMAL strings, so `F8 15`
    is `f8["21"]` -- the trap that produced the blank-choice-box regression."""
    raw = json.load(open(OPLEN, encoding="utf-8"))
    f8 = {int(k): int(v) for k, v in raw["f8"].items()}
    bare = {int(k): int(v) for k, v in raw["bare"].items()}
    return f8, bare


TAIL_MAX = 32


def record_end(rom, after_run):
    """Offset of the record's terminating FF, scanned from the end of the text run.

    ⚠ Deliberately NOT an opcode walk. `opcode_lengths.json` was derived from
    overlay 28 and says `F8 23` is 4 bytes, but file 8's records end
    `… F8 09 F8 23 00 FF` -- three. Trusting the table stepped straight over the
    terminator and every record was rejected. Rather than edit a shared table on
    the strength of one file (that is how the `F8 15` width regression happened),
    scan the short wrapper tail for the FF and make the caller prove the record
    round-trips. Records whose tail is longer than TAIL_MAX are refused.
    """
    end = rom.find(b"\xff", after_run, after_run + TAIL_MAX)
    return end


def pointer_slots(rom, lo, hi, ram, size):
    """{record offset: [slot offsets]} for every u32 in the file that lands in it."""
    out = {}
    for a in range(lo, hi - 3, 4):
        v = int.from_bytes(rom[a:a + 4], "little")
        if ram <= v < ram + size:
            out.setdefault(lo + (v - ram), []).append(a)
    return out


def rows(fid=FID):
    p = work_path(fid)
    if not os.path.exists(p):
        return
    for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
        f = ln.split("\t")
        if len(f) >= 6 and f[5].strip():
            yield int(f[0], 16), int(f[1]), f[4], f[5].strip()


def plan(rom, fid=FID):
    """[(record start, run offset, run length, jp, ko)] for rows we can repoint."""
    orig_lo = FILES[fid]
    fat = X.u32(rom, 0x48)
    lo = X.u32(rom, fat + fid * 8)
    hi = X.u32(rom, fat + fid * 8 + 4)
    _, _, ram, size = X.overlay_of_file(rom, fid)
    shift = lo - orig_lo
    slots = pointer_slots(rom, lo, hi, ram, size)
    out = []
    for off, blen, jp, ko in rows(fid):
        cur = off + shift
        # ⛔⛔ SESSION 43 — 이 창을 넓히지 말 것. 8 바이트가 실증된 안전값이다.
        # 「（そして・・・）」(0x45453A) 의 레코드 시작은 22바이트 앞(0x454524)이라 8 로는
        # 못 찾는다. 그래서 64 로 넓혀 봤고 **세 번 연속 게이트에 걸렸다**:
        #   v200: 128레코드 → live read-back 1건 실패 (`0x021AAC19` = 'あいい   ')
        #   v201: 「한 레코드를 두 런이 주장」(0x451EE4 = スクリュー+シンカー) 을 거부해도
        #         여전히 1건 실패 — 남은 원인은 미규명.
        # ⚠ 왕복 증명은 이걸 **못 잡는다**: head 를 ROM 에서 그대로 떠 오므로 레코드
        #   시작이 틀려도 항상 통과한다. 「가장 가까운 포인터니까 안전」이라는 내 추론이
        #   틀렸다는 뜻이다.
        # ⇒ 「そして」류를 넣으려면 창을 넓히는 게 아니라 **레코드 경계를 실제로 판별**해야
        #   한다(한 레코드의 모든 런을 한 번에 치환하는 재설계 포함).
        rs = next((cur + d for d in range(0, -9, -1) if cur + d in slots), None)
        if rs is None:
            continue
        if bytes(rom[cur:cur + blen]) != encode_jp(jp):
            continue                       # the run drifted; never write blind
        out.append((rs, cur, blen, jp, ko))
    # ⛔⛔ SESSION 43 — 한 레코드를 두 런이 주장하면 **버린다**.
    # `apply()` 는 레코드 단위로 «앞부분 + 한국어 + 뒷부분» 을 새로 만들어 꼬리에 붙이고
    # 포인터를 돌린다. 같은 레코드에 런이 둘이면 각자 자기 버전을 붙이므로 포인터는
    # 하나만 이기고 나머지 사본은 죽은 채 남으며, 진 쪽의 한국어는 화면에 안 나온다.
    # 실측(v200): 창을 64바이트로 넓히자 0x451EE4 를 「スクリュー」와 「シンカー」가 함께
    # 주장했고, live read-back 게이트가 `0x021AAC19 decoded 'あいい   '` 로 잡았다.
    # ⚠ 근본 해결은 «한 레코드의 모든 런을 한 번에 치환»하는 것이지만, 그건 재배치
    #   경로를 다시 설계하는 일이라 지금은 안전하게 거부만 한다.
    import collections as _c
    _n = _c.Counter(rs for rs, _r, _b, _j, _k in out)
    return ([it for it in out if _n[it[0]] == 1],
            lo, ram, size, slots, shift)


def apply(rom, fid=FID, enc=None, verbose=True):
    enc = enc or koenc.Encoder()
    orig_lo = FILES[fid]
    items, lo, ram, size, slots, shift = plan(rom, fid)
    blob, made, bad = bytearray(), [], 0
    for rs, run, blen, jp, ko in items:
        end = record_end(rom, run + blen)
        if end < 0:
            bad += 1
            continue
        head, tail = bytes(rom[rs:run]), bytes(rom[run + blen:end + 1])
        # Round-trip proof: rebuilding with the ORIGINAL run must reproduce the
        # record byte for byte. If it does not, our idea of where the record
        # starts or ends is wrong and nothing may be written.
        if head + encode_jp(jp) + tail != bytes(rom[rs:end + 1]):
            bad += 1
            continue
        try:
            kb = enc.encode(ko)
        except KeyError:
            bad += 1
            continue
        rec = head + kb + tail
        made.append((rs, len(blob)))
        blob += rec

    if not made:
        if verbose:
            print(f"  file {fid}: nothing to repoint ({bad} rejected)")
        return {"written": 0, "skipped": bad, "pointers": 0}

    rom2, blob_ram, _ = X.expand(rom, fid, bytes(blob))
    rom[:] = rom2
    shift2 = X.u32(rom, X.u32(rom, 0x48) + fid * 8) - orig_lo
    written = 0
    for rs, rel in made:
        target = ram + (rs - shift - orig_lo)      # RAM address, move-invariant
        for a in slots.get(rs, []):
            slot = a - shift + shift2
            if X.u32(rom, slot) == target:
                X.w32(rom, slot, blob_ram + rel)
                written += 1
    if verbose:
        print(f"  file {fid}: {len(made)} records -> tail ({len(blob):,}B), "
              f"{written} pointers rewritten, {bad} rejected")
    return {"written": len(made), "skipped": bad, "pointers": written}


# ⛔⛔ SESSION 35: the user reports the SCENARIO WILL NOT START on v89, which
# carries both file-8 paths. Neither is proven innocent, so both are opt-in until
# an A/B says which one it is. `apply_relocate` has a known hole: `free_runs`
# rejects padding that a pointer POINTS INTO, but a stretch of zeros may itself
# BE a pointer array with null entries -- writing text over one sends the game to
# a garbage address, which is exactly "the scenario does not load".
SHIP_INPLACE = (8,) if os.environ.get("PPKP9_FILE8_INPLACE") == "1" else ()


def paired_sites(rom, jp, run, blen, lo, hi):
    """이 런과 «같은 문자열 + 같은 도입 오프코드»를 가진 다른 자리들.

    ⭐ SESSION 43 — 능력/인물 라벨 레코드는 증가(い)/감소(う) **쌍**으로 존재하는데
    워크리스트는 문자열당 한 행뿐이라, 기록된 쪽만 출하되어 화면이 반쪽이 됐다
    (「パワーが ５감소」 / 「미남が ５감소」). 세션38이 오버레이28에서 고친
    「모든 출현에 쓰기」를 파일 8 에도 적용한 것.

    ⚠ 모듈 레벨에 둔 이유: **게이트가 같은 규칙으로 다시 계산해야** 하기 때문이다.
    `verify_file8` 이 「포인터 워드만 바뀌어야 한다」를 검사하는데 짝 사이트를 모르면
    정당한 쓰기를 파손으로 신고한다(v196 에서 실제로 그랬다). 목록을 넘겨받는 대신
    같은 함수를 호출하게 해서 게이트가 계속 독립적으로 판정하게 한다.
    """
    want = encode_jp(jp)
    if len(want) != blen:
        return []
    op = bytes(rom[run - 2:run])           # 런을 도입한 래퍼
    if len(op) != 2 or op[0] != 0xF8:
        return []
    out, i = [], rom.find(bytes(want), lo, hi)
    while 0 <= i:
        if i != run and bytes(rom[i - 2:i]) == op:
            out.append(i)
        i = rom.find(bytes(want), i + 1, hi)
    return out


def apply_inplace(rom, fid=8, enc=None, verbose=True):
    """Write only the records whose Korean fits the run it replaces.

    ⭐ SESSION 35. The pointer path floods the ability panel (user A/B: the same
    screen is clean with `SHIP=()`), and the flood is KANA, not our Hangul -- so
    the tail we append past the overlay is not being read as we wrote it. But the
    same screenshot shows 「근력」 rendering CORRECTLY in Korean, so the panel's
    font is fine and only the relocation is the problem.

    So do not relocate. 99 of the 213 pointered records have Korean that fits the
    original run (katakana is 1 byte and Hangul 2, but plenty of these are short
    enough anyway), and writing those in place changes no length, moves no record
    and needs no overlay growth -- the contiguous `00 | F8 5A n | F8 08 text F8 09
    | F8 23 00 | FF` layout is preserved exactly.

    ⛔ The one real hazard of writing file 8 in place is session 29's save wipe:
    the file holds 54 pointer ARRAYS (the largest 812 entries) and an offset-driven
    write that lands in one shreds it -- that is precisely what happened to file 30
    at 0x325D93. So every target is refused if any aligned u32 overlapping it
    currently points into the overlay.
    """
    enc = enc or koenc.Encoder()
    items, lo, ram, size, slots, shift = plan(rom, fid)
    w = skip = refused = extra = 0

    # ⭐ SESSION 43 — THE PAIRED RECORD. The ability/stat labels exist TWICE,
    # once in the 「い」(increase) record and once in the 「う」(decrease) one:
    #     <F85A>い<F808>パワー<F809><F823> <FF>   <F85A>う<F808>パワー<F809><F823> <FF>
    # and the worklist holds only ONE row per distinct string, so whichever of
    # the pair the extractor happened to record is the only one that ships.
    # Measured on v182: 「パワー」 recorded the い record, 「ハンサム」 the う one --
    # so the decrease line came out 「パワーが ５감소」 / 「미남が ５감소」, half
    # Korean, which is what the user photographed.
    # This is session 38's 「공용 텍스트」 bug in a file that never got its fix:
    # `insert_extra.sites()` re-walks the ROM and writes EVERY occurrence, but
    # file 8 goes through this module and it only ever wrote the recorded offset.
    # Same remedy, same gates: an extra site is written only when the bytes there
    # still read as the recorded Japanese AND it carries the same introducing
    # opcode the worklist recorded, so nothing outside a text run is touched.
    def _extra_sites(jp, run, blen):
        return paired_sites(rom, jp, run, blen, lo, lo + size)

    def _write(run, blen, kb):
        """Write with the session-29 pointer-array guard. True if written."""
        lo_w = run & ~3
        if any(ram <= int.from_bytes(rom[a:a + 4], "little") < ram + size
               for a in range(lo_w, run + blen, 4)):
            return False                  # looks like a pointer array: do not touch
        rom[run:run + blen] = kb + b"\x00" * (blen - len(kb))
        return True

    for rs, run, blen, jp, ko in items:
        try:
            kb = enc.encode(ko)
        except KeyError:
            skip += 1
            continue
        if len(kb) > blen:
            skip += 1
            continue
        sites = _extra_sites(jp, run, blen)
        if not _write(run, blen, kb):
            refused += 1
            continue
        w += 1
        for s in sites:
            if _write(s, blen, kb):
                extra += 1
            else:
                refused += 1
    if verbose:
        print(f"  file {fid} in place: {w} written (+{extra} paired sites), "
              f"{skip} do not fit, {refused} refused (pointer array)")
    return {"written": w, "paired": extra, "skipped": skip, "refused": refused}


# ⛔⛔ SESSION 36: rows with NO POINTER were shipped by NOTHING.
# `plan()` starts from `pointer_slots()` and drops any row whose record start it
# cannot find (`rs is None: continue`), and BOTH `apply()` and `apply_inplace()`
# start from `plan()`. So a row in the worklist that no u32 points at fell through
# every path silently -- including 「上がった」/「下がった」, which every single
# training result prints, and which were therefore Japanese in every build ever
# made while the worklist said they were translated.
# They cannot be repointed (there is no pointer to rewrite), so the only option is
# the run itself, under exactly the guard `apply_inplace` uses.
SHIP_ORPHAN = ((8, 20) if os.environ.get("PPKP9_FILE8_ORPHAN", "1") != "0"
               else ())


def orphans(rom, fid=FID):
    """Rows the pointer plan cannot reach: [(live offset, length, jp, ko, pristine offset)].

    The pristine offset rides along because `insert_extra.needs_exact` keys on it
    -- the padding rule is decided per run, and only the pristine walk knows what
    introduced each one.

    Sites come from `insert_extra.sites`, i.e. EVERY occurrence of the string, not
    just the one offset the worklist recorded -- see the session-38 note there.
    Both guards below still run per site, so a duplicate is held to exactly the
    same standard as the recorded one.
    """
    import insert_extra as IX
    orig_lo = FILES[fid]
    fat = X.u32(rom, 0x48)
    lo = X.u32(rom, fat + fid * 8)
    hi = X.u32(rom, fat + fid * 8 + 4)
    _, _, ram, size = X.overlay_of_file(rom, fid)
    shift = lo - orig_lo
    slots = pointer_slots(rom, lo, hi, ram, size)
    out = []
    for off, blen, jp, ko in IX.WORK(fid):
        cur = off + shift
        if any(cur + d in slots for d in range(0, -9, -1)):
            continue                       # the pointer path owns this one
        if bytes(rom[cur:cur + blen]) != encode_jp(jp):
            continue                       # the run drifted; never write blind
        out.append((cur, blen, jp, ko, off))
    return out, ram, size


def apply_orphans(rom, fid=FID, enc=None, verbose=True):
    """Write the pointer-less rows inside their own run.

    ⛔ Session 29's save wipe is the hazard this shares with `apply_inplace`:
    file 8 holds 54 pointer ARRAYS (largest 812 entries) and an offset-driven
    write that lands in one shreds it. Same guard, not a weaker one -- refuse the
    target if ANY aligned u32 overlapping it currently points into the overlay.
    """
    enc = enc or koenc.Encoder()
    items, ram, size = orphans(rom, fid)
    w = skip = refused = 0
    for run, blen, jp, ko, off in items:
        try:
            kb = enc.encode(ko)
        except KeyError:
            skip += 1
            continue
        if len(kb) > blen:
            skip += 1
            continue
        # File 20 CONTAINS 0xFF-delimited chains, so the exact-length rule
        # `insert_extra` applies there applies here too: 0x00 is not a delimiter
        # and the renderer reads past the run (session 34's garbage screen).
        # ⚠ Session 41: the rule is now per RUN, not per file -- only the 31
        # file-20 rows the walk introduces with a raw `FF` (plus the 11 `MENU`
        # rows, whose delimiter no walk has proven) are chain entries; the other
        # 57 sit behind ordinary VM opcodes that carry their own terminator.
        # `PPKP9_FF_PAD=1` relaxes both passes together, never just one.
        import insert_extra as IX
        if IX.needs_exact(fid, off) and len(kb) != blen:
            skip += 1
            continue
        lo_w = run & ~3
        if any(ram <= int.from_bytes(rom[a:a + 4], "little") < ram + size
               for a in range(lo_w, run + blen, 4)):
            refused += 1
            continue
        rom[run:run + blen] = kb + b"\x00" * (blen - len(kb))
        w += 1
    if verbose and (w or skip or refused):
        print(f"  file {fid} orphan rows (no pointer): {w} written, "
              f"{skip} do not fit, {refused} refused (pointer array)")
    return {"written": w, "skipped": skip, "refused": refused}


SHIP_RELOC = (8,) if os.environ.get("PPKP9_FILE8_RELOC") == "1" else ()


def free_runs(rom, fid=8, minlen=12):
    """Padding inside the file that no live pointer names: [(offset, length)].

    ⭐ Why inside and not past the end: appending to the overlay is exactly what
    floods the ability panel (v80 A/B) and what the file-20 note recorded for ov9
    -- the bytes after an overlay belong to the game at runtime. Padding that is
    already *inside* the file is loaded with it and addressed as part of it.
    ⛔ A run is only offered if no aligned u32 in the file currently points into
    it: file 8 is full of pointer arrays and landing in one is session 29's save
    wipe.
    """
    lo = X.u32(rom, X.u32(rom, 0x48) + fid * 8)
    hi = X.u32(rom, X.u32(rom, 0x48) + fid * 8 + 4)
    _, _, ram, size = X.overlay_of_file(rom, fid)
    buf = rom[lo:hi]
    runs, n = [], 0
    for i, b in enumerate(buf):
        if b in (0x00, 0xFF):
            n += 1
        else:
            if n >= minlen:
                runs.append((i - n, n))
            n = 0
    if n >= minlen:
        runs.append((len(buf) - n, n))
    targets = set()
    for a in range(lo, hi - 3, 4):
        v = int.from_bytes(rom[a:a + 4], "little")
        if ram <= v < ram + size:
            targets.add(v - ram)
    return [(o, n) for o, n in runs
            if not any(o <= t < o + n for t in targets)]


def apply_relocate(rom, fid=8, enc=None, verbose=True):
    """Move the records that do NOT fit their run into that internal padding."""
    enc = enc or koenc.Encoder()
    items, lo, ram, size, slots, shift = plan(rom, fid)
    pool = sorted(free_runs(rom, fid), key=lambda t: -t[1])
    used = [0] * len(pool)
    placed = skipped = ptr = 0
    for rs, run, blen, jp, ko in items:
        try:
            kb = enc.encode(ko)
        except KeyError:
            continue
        if len(kb) <= blen:
            continue                      # apply_inplace already handled it
        end = record_end(rom, run + blen)
        if end < 0:
            skipped += 1
            continue
        head, tail = bytes(rom[rs:run]), bytes(rom[run + blen:end + 1])
        if head + encode_jp(jp) + tail != bytes(rom[rs:end + 1]):
            skipped += 1                  # our record framing is wrong; never write
            continue
        rec = head + kb + tail
        for i, (off, cap) in enumerate(pool):
            if cap - used[i] >= len(rec):
                at = lo + off + used[i]
                rom[at:at + len(rec)] = rec
                target = ram + (off + used[i])
                used[i] += len(rec)
                for a in slots.get(rs, []):
                    X.w32(rom, a, target)
                    ptr += 1
                placed += 1
                break
        else:
            skipped += 1
    if verbose:
        print(f"  file {fid} relocated into padding: {placed} records, "
              f"{ptr} pointers rewritten, {skipped} had no room")
    return {"written": placed, "pointers": ptr, "skipped": skipped}


def handled_offsets(rom, fids=None):
    """Run offsets insert_extra must NOT write in place -- we repoint them."""
    out = set()
    for fid in (fids or SHIP):
        try:
            items, *_ = plan(rom, fid)
        except Exception:
            continue
        out |= {run for _rs, run, _b, _j, _k in items}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    ap.parse_args()
    rom = bytearray(open(BASE + r"/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds",
                         "rb").read())
    print(apply(rom))


if __name__ == "__main__":
    main()
