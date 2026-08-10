#!/usr/bin/env python3
"""Translation workbench: draft -> check -> stage, with no ROM build in the loop.

The build is deliberately not part of this cycle. Under the agreed order we
translate everything first, apply once, then test -- so staged work accumulates
in `translation/pending/` where the build cannot see it, and `finalize` promotes
it to a real batch when the text is done.

    python tools/tl.py status
    python tools/tl.py next 200            # emit the next chunk to translate
    python tools/tl.py check 005           # verify a filled-in draft
    python tools/tl.py stage 005           # accept it into translation/pending/
    python tools/tl.py finalize --batch 120

Two things made the last 200-line pass slow, and both are gone here:
  * ids are 11-character hashes; retyping one per line is pure overhead and a
    transcription risk. Drafts are keyed by a short per-file number instead, and
    this tool maps them back to the stable id.
  * glyph budgets were counted by hand, line by line, before writing anything.
    `check` counts them, so the budget is enforced after the fact on the few
    lines that actually overflow rather than guessed on all of them.
"""
import sys, io, os, re, glob, json, hashlib, argparse, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P
from layout_audit import rows as display_rows

BASE = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"
WORK = f"{BASE}/translation/work"
PENDING = f"{BASE}/translation/pending"
HANGUL = range(0xAC00, 0xD7A4)
PUNCT = "・。、！？～）（「」・…゛゜ー"
LOOKALIKE = {"(": "（", ")": "）", "~": "～", "%": "％", "—": "～",
             "!": "！", "?": "？", ",": "、", ".": "。", '"': "「", "'": "「",
             # Dashes are the trap: six codepoints look identical in an editor
             # and only U+FF5E (～) and U+30FC (ー) have glyphs. U+2015 cost a
             # staging round, so every look-alike now names its replacement.
             "―": "～", "–": "～", "─": "～", "-": "～", "〜": "～",
             "‥": "・・", ":": "・", ";": "、"}


def rid(jp):
    return "L" + hashlib.sha1(jp.encode("utf-8")).hexdigest()[:10]


def meaningful(c):
    return c not in PUNCT and (0x3040 <= ord(c) <= 0x30FF or 0x4E00 <= ord(c) <= 0x9FFF)


# Runs whose leading bytes the extractor decoded as text but almost certainly
# are not: a stray kanji/katakana glued to an otherwise clean sentence, with no
# reading that fits the scene. Re-encoding them would emit the *character's*
# charcode where the ROM had something else, so the run must be left alone --
# the same reason `尅㎞` is excluded above. Listed literally rather than matched
# by a heuristic because there are exactly five and a heuristic loose enough to
# catch them also catches real dialogue that opens on a katakana interjection.
CORRUPT = ("鷺ヒあ", "盛ヒい", "きぬピ", "ユせるよ", "ィこうか")

# Two-kana runs left over once every real line was translated. Each is half of a
# name-insert seam or a menu index the extractor split mid-word -- none of them
# is a word, and none reads as anything in its scene. They are listed rather
# than matched by shape because "two kana" also describes うん / はい / いた,
# which are ordinary dialogue. With these named, `next --real` reports the
# worklist as genuinely finished instead of always trailing 25 unusable rows.
FRAGMENTS = ("そ杵", "あい", "う７", "えじ", "える", "うえ", "おか", "めか",
             "えは", "えひ", "いか", "いう", "いき", "あえ", "めと", "ぃい",
             "うゴ", "うユ", "あき", "あゅ", "いこ", "あか", "お何・・・",
             "あお", "ィ屋！")


def corrupt(jp):
    return jp in FRAGMENTS or any(jp.startswith(c) for c in CORRUPT)


def load_done():
    """jp -> ko from committed batches AND staged pending work."""
    done = {}
    files = ([f"{BASE}/translation/common_lines.tsv"]
             + sorted(glob.glob(f"{BASE}/translation/batch*.tsv"),
                      key=lambda p: int(re.search(r"batch(\d+)", p).group(1)))
             + sorted(glob.glob(f"{PENDING}/*.tsv")))
    for p in files:
        if not os.path.exists(p):
            continue
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            q = ln.split("\t")
            if len(q) >= 2 and q[0].strip() and q[1].strip():
                done[q[0].strip()] = q[1].strip()
    return done


def load_corpus():
    runs = []
    for ln in open(f"{BASE}/survey/ov28/dialogue_runs.tsv", encoding="utf-8").read().splitlines():
        q = ln.split("\t")
        if len(q) >= 4:
            runs.append((int(q[0], 16), q[3]))
    runs.sort()
    return runs


def worklist():
    """Untranslated lines worth a translator's time, most-seen first."""
    runs = load_corpus()
    done = load_done()
    occ = collections.Counter(jp for _, jp in runs)
    first = {}
    for i, (_, jp) in enumerate(runs):
        first.setdefault(jp, i)

    rows = []
    for jp, n in occ.items():
        if jp in done:
            continue
        # Only pure punctuation is dropped. This used to be "fewer than 3
        # meaningful characters", which looked like a way to skip fragments not
        # worth a translator's time -- but a character name is two kanji, so the
        # rule silently withheld 維織 (411 occurrences), 准 (130) and every other
        # name from the worklist for the whole project. Coverage read 82% while
        # the heroine's name still drew as kanji next to the Korean. Short runs
        # that really are unsafe to translate (mid-word kana splits, the doubled-
        # kana branch markers) are now *flagged* by _skippable instead, so the
        # call is visible and mine to make rather than made silently here.
        if not any(meaningful(c) for c in jp):
            continue
        if jp[-1] in "見投打昨喫" or any(c in jp for c in "尅㎞"):
            continue
        if corrupt(jp):
            continue
        i = first[jp]
        rows.append({"id": rid(jp), "occ": n, "pos": i,
                     "max": 19 * display_rows(jp),
                     "prev": runs[i - 1][1] if i else "",
                     "jp": jp,
                     "next": runs[i + 1][1] if i + 1 < len(runs) else ""})
    # Script order, not frequency. Frequency ordering earned its keep while the
    # common lines were still untranslated; 6,210 of the 6,213 that remain occur
    # exactly once, so it now just shuffles unrelated lines together. Sorted by
    # position instead, 43% of consecutive entries are script neighbours, which
    # means whole scenes get translated in one pass -- better context, and the
    # neighbour lines stop needing to be printed twice.
    rows.sort(key=lambda r: r["pos"])
    return rows, runs, done


def _norm(s):
    """A line stripped of punctuation -- what makes two lines the same wording."""
    return re.sub(r"[。、！？・…～）（「」\s]", "", s)


def _skippable(jp, prev):
    """Lines that are not dialogue and should be left blank, flagged not removed.

    Judging them is contextual (a debug menu looks like ordinary text), so this
    only marks candidates; the call stays with the translator.
    """
    if "あいうえお" in jp or "デバッグ" in jp:
        return True
    if "シナリオテスト" in prev or "デバッグ" in prev:
        return True
    core = re.sub(r"[。、！？・…～）（「」\s]", "", jp)
    # A lone kana is never a word here -- it is one half of a name-insert seam
    # (「お」+「兄ちゃん」), and translating it would break the join.
    if len(core) == 1 and ("ぁ" <= core <= "ゖ" or "ァ" <= core <= "ヺ"):
        return True
    # のの / はは / ひひ / むむ select a branch of a multiple-choice line; they
    # are structure the extractor decoded as text, not dialogue. See the
    # 「今日は、○○に行く約束」 menu, where 「むむに」 carries the shared 「に」.
    if len(core) == 2 and core[0] == core[1] and "ぁ" <= core[0] <= "ヺ":
        return True
    return False


def load_glossary():
    p = f"{BASE}/handoff/data/glossary_terms.tsv"
    g = {}
    if os.path.exists(p):
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            q = ln.split("\t")
            if len(q) >= 3:
                g[q[1]] = q[2]
    return g


# ---------------------------------------------------------------- commands


def cmd_status(a):
    rows, runs, done = worklist()
    hit = sum(1 for _, jp in runs if jp in done)
    staged = sum(len(open(p, encoding="utf-8").read().splitlines()) - 1
                 for p in glob.glob(f"{PENDING}/*.tsv"))
    print(f"coverage {hit}/{len(runs)} = {100*hit/len(runs):.2f}%  "
          f"(staged but not built: {staged} lines)")
    print(f"remaining worklist: {len(rows)} lines / "
          f"{sum(r['occ'] for r in rows)} occurrences")
    drafts = sorted(glob.glob(f"{WORK}/draft_*.tsv"))
    if drafts:
        print("\ndrafts:")
        for p in drafts:
            tag = os.path.basename(p)[6:-4]
            ko = f"{WORK}/draft_{tag}.ko"
            n = len(open(ko, encoding="utf-8").read().split("\n")) if os.path.exists(ko) else 0
            print(f"  {tag}: {'filled' if n else 'empty'}"
                  f"{'  (staged)' if os.path.exists(f'{PENDING}/{tag}.tsv') else ''}")


def cmd_next(a):
    rows, _, _ = worklist()
    if getattr(a, "real", False):
        # The flagged fragments are permanent -- they are never going to be
        # translated, so they sit at the head of the worklist and re-fill the
        # first ~80 lines of every chunk. --real drops them so a 500-line chunk
        # is 500 lines of actual work; they stay in the worklist and in the
        # coverage figures, they just stop being printed.
        rows = [r for r in rows if not _skippable(r["jp"], r["prev"])]
    if not rows:
        print("nothing left")
        return
    chunk = rows[:a.count]
    os.makedirs(WORK, exist_ok=True)
    tag = a.tag or f"{len(glob.glob(f'{WORK}/draft_*.tsv')) + 1:03d}"
    path = f"{WORK}/draft_{tag}.tsv"
    with open(path, "w", encoding="utf-8") as f:
        f.write("n\tid\tocc\tmax\tprev\tjp\tnext\n")
        for i, r in enumerate(chunk, 1):
            f.write(f"{i}\t{r['id']}\t{r['occ']}\t{r['max']}\t"
                    f"{r['prev']}\t{r['jp']}\t{r['next']}\n")

    gl = load_glossary()
    used = {}
    for r in chunk:
        for term, ko in gl.items():
            if term in r["jp"]:
                used[term] = ko
    if used:
        print(f"# 확정 용어 ({len(used)}) — 반드시 이대로")
        print("  " + " / ".join(f"{k}={v}" for k, v in sorted(used.items())))
        print()
    # Everything below is about not printing what I can already infer.
    # Context is only worth its tokens when the line cannot stand alone, and
    # after sorting by script position the neighbour is usually the very next
    # line in this same chunk.
    done_norm = {_norm(k): v for k, v in load_done().items()}
    print(f"# draft_{tag}: {len(chunk)}줄. `n<TAB>번역`을 {WORK}/draft_{tag}.ko 에 쓴다.")
    print("# 스크립트 순. 최대글자수는 19일 때 생략. ≈는 기번역 재활용 제안, ✗는 번역 제외 후보.")
    prev_jp = None
    for i, r in enumerate(chunk, 1):
        head = f"{i}" + ("" if r["max"] == 19 else f"|{r['max']}")
        complete = r["jp"][-1] in "。！？）」"
        bits = []
        if r["prev"] and r["prev"] != prev_jp and not r["jp"][0] in "（「":
            bits.append(r["prev"])
        bits.append(f"⟪{r['jp']}⟫")
        if not complete and r["next"]:
            bits.append(r["next"])
        line = f"{head} " + " ".join(bits)
        sug = done_norm.get(_norm(r["jp"]))
        if sug:
            line += f"   ≈{sug}"
        elif _skippable(r["jp"], r["prev"]):
            line += "   ✗"
        print(line)
        prev_jp = r["jp"]


def _read_draft(tag):
    path = f"{WORK}/draft_{tag}.tsv"
    if not os.path.exists(path):
        sys.exit(f"no such draft: {path}")
    rows = {}
    for ln in open(path, encoding="utf-8").read().splitlines()[1:]:
        q = ln.split("\t")
        if len(q) >= 7:
            rows[q[0]] = {"id": q[1], "max": int(q[3]), "jp": q[5]}
    ko = {}
    kp = f"{WORK}/draft_{tag}.ko"
    if os.path.exists(kp):
        for ln in open(kp, encoding="utf-8").read().splitlines():
            if "\t" in ln:
                n, v = ln.split("\t", 1)
                if v.strip():
                    ko[n.strip()] = v.strip()
    return rows, ko


def _problems(rows, ko):
    errs = []
    for n, v in sorted(ko.items(), key=lambda kv: int(kv[0])):
        if n not in rows:
            errs.append(f"{n}: no such line number")
            continue
        r = rows[n]
        if len(v) > r["max"]:
            errs.append(f"{n}: {len(v)} glyphs > {r['max']}  {v}")
        for ch in v:
            if ch == " " or ord(ch) in HANGUL:
                continue
            if P.CH2CC.get(ch) is None:
                fix = LOOKALIKE.get(ch)
                errs.append(f"{n}: no glyph {ch!r}"
                            + (f" -- use {fix!r}" if fix else "") + f"  {v}")
            elif 0x1100 <= ord(ch) <= 0x11FF or 0x3130 <= ord(ch) <= 0x318F:
                errs.append(f"{n}: bare jamo {ch!r}  {v}")
        body = v
        while body and ("ぁ" <= body[0] <= "ゖ" or "ァ" <= body[0] <= "ヺ"):
            body = body[1:]
        if [c for c in body if "一" <= c <= "鿿" or "ぁ" <= c <= "ゖ" or "ァ" <= c <= "ヺ"]:
            errs.append(f"{n}: Japanese left in Korean  {v}")
        if not any(ord(c) in HANGUL for c in v):
            errs.append(f"{n}: no Hangul at all  {v!r}")
    dup = collections.Counter(v for v in ko.values() if len(v) > 4)
    for v, c in dup.items():
        if c > 1:
            errs.append(f"same translation on {c} different lines: {v!r}")
    errs += _shifted(rows, ko)
    return errs


def _tail(s):
    m = re.search(r"[。、！？）」]+$|・+$", s)
    return m.group(0) if m else ""


def _shifted(rows, ko):
    """Is a stretch of this draft translated one line off?

    The defect that survived every other check: write one line's Korean against
    the next line's number and everything after it shifts, silently, because
    both sides are still perfectly good Korean. Two of my own staged chunks
    shipped that way and it was only caught by playing the game.

    Trailing punctuation is the signal -- 。/？/！/、/・・・ echo across the
    translation, so if ko[i] agrees with jp[i+1]'s ending more often than with
    jp[i]'s across a window, the window is shifted.
    """
    ns = sorted((int(n) for n in ko if n in rows))
    if len(ns) < 30:
        return []
    jp = [rows[str(n)]["jp"] for n in ns]
    kk = [ko[str(n)] for n in ns]
    ali = [1 if _tail(jp[i]) == _tail(kk[i]) else 0 for i in range(len(kk))]
    off = [1 if i + 1 < len(jp) and _tail(jp[i + 1]) == _tail(kk[i]) else 0
           for i in range(len(kk))]
    W, bad = 15, []
    for i in range(len(kk) - W):
        if sum(off[i:i + W]) > sum(ali[i:i + W]):
            bad.append(ns[i])
    if not bad:
        return []
    return [f"ROW SHIFT suspected around draft line {bad[0]}"
            f" ({len(bad)} windows read better one line later)"
            f" -- check that line's number against the draft"]


def cmd_check(a):
    rows, ko = _read_draft(a.tag)
    errs = _problems(rows, ko)
    for e in errs:
        print("ERROR " + e)
    print(f"\n{len(ko)}/{len(rows)} filled, {len(errs)} problem(s)")
    return 1 if errs else 0


def cmd_stage(a):
    rows, ko = _read_draft(a.tag)
    errs = _problems(rows, ko)
    if errs:
        for e in errs:
            print("ERROR " + e)
        print(f"\n{len(errs)} problem(s); nothing staged.")
        return 1
    os.makedirs(PENDING, exist_ok=True)
    dst = f"{PENDING}/{a.tag}.tsv"
    with open(dst, "w", encoding="utf-8") as f:
        f.write("jp\tko\n")
        for n, v in sorted(ko.items(), key=lambda kv: int(kv[0])):
            f.write(f"{rows[n]['jp']}\t{v}\n")
    print(f"staged {len(ko)} lines -> {dst}")
    return 0


def cmd_lookup(a):
    """How has this Japanese been rendered before?

    Written after the fifth chunk in a row where the slow part was not the
    translating but grepping the batches to find whether ちゃん was 짱 or 쨩,
    whether ボ～ク was 나～ or 내～, what `ました）` had to end in. Ranked by
    frequency so the established rendering is the first line, not the tenth.
    """
    done = load_done()
    hits = [(jp, ko) for jp, ko in done.items() if a.term in jp]
    if not hits:
        print(f"no existing translation contains {a.term!r}")
        return
    # A fragment's rendering matters most when the fragment *starts* the line:
    # that is the name-insert seam where the particle convention lives.
    lead = [h for h in hits if h[0].startswith(a.term)]
    rest = [h for h in hits if not h[0].startswith(a.term)]
    for label, group in (("line-initial", lead), ("elsewhere", rest)):
        if not group:
            continue
        print(f"# {label} ({len(group)})")
        for jp, ko in sorted(group, key=lambda h: len(h[0]))[:a.limit]:
            print(f"  {jp}\t{ko}")


def cmd_audit(a):
    """Same jp, two different ko -- whichever file loads last silently wins."""
    seen, conf = {}, []
    files = ([f"{BASE}/translation/common_lines.tsv"]
             + sorted(glob.glob(f"{BASE}/translation/batch*.tsv"),
                      key=lambda p: int(re.search(r"batch(\d+)", p).group(1)))
             + sorted(glob.glob(f"{PENDING}/*.tsv")))
    for p in files:
        if not os.path.exists(p):
            continue
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            q = ln.split("\t")
            if len(q) < 2 or not q[0].strip() or not q[1].strip():
                continue
            jp, ko = q[0].strip(), q[1].strip()
            if jp in seen and seen[jp][1] != ko:
                conf.append((jp, seen[jp], (os.path.basename(p), ko)))
            elif jp not in seen:
                seen[jp] = (os.path.basename(p), ko)
    for jp, (f1, k1), (f2, k2) in conf:
        print(f"{jp}\n   {f1}: {k1}\n   {f2}: {k2}")
    print(f"\n{len(seen)} unique jp, {len(conf)} conflicting")
    return 0


def cmd_font(a):
    """Will every syllable the translation uses get a glyph slot?

    build_kr re-runs build_fontpack every build and its first priority is the
    syllables in translation/batch*.tsv, so the check that matters is not
    "is it in the current map" but "does the post-finalize set still fit".
    """
    cap = len(json.load(open(f"{BASE}/survey/font/kr_font_map.json",
                             encoding="utf-8")))
    def syls(paths, skip_header):
        s = set()
        for p in paths:
            if not os.path.exists(p):
                continue
            body = open(p, encoding="utf-8").read().splitlines()
            for ln in (body[1:] if skip_header else body):
                q = ln.split("\t")
                if q:
                    s.update(c for c in q[-1] if ord(c) in HANGUL)
        return s
    built = syls([f"{BASE}/translation/common_lines.tsv",
                  f"{BASE}/translation/intro_lines.tsv"]
                 + glob.glob(f"{BASE}/translation/batch*.tsv"), True)
    staged = syls(sorted(glob.glob(f"{PENDING}/*.tsv")), True)
    total = built | staged
    print(f"font pack capacity   {cap}")
    print(f"built batches use    {len(built)}")
    print(f"pending adds         {len(staged - built)}")
    print(f"post-finalize total  {len(total)}   headroom {cap - len(total)}")
    if len(total) > cap:
        print(f"\nOVER CAPACITY by {len(total) - cap} -- build would abort")
        return 1
    return 0


def cmd_finalize(a):
    files = sorted(glob.glob(f"{PENDING}/*.tsv"))
    if not files:
        sys.exit("nothing staged")
    dst = f"{BASE}/translation/batch{a.batch}.tsv"
    if os.path.exists(dst):
        sys.exit(f"{dst} exists; pick another --batch")
    seen, out = set(), []
    for p in files:
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            q = ln.split("\t")
            if len(q) >= 2 and q[0].strip() and q[1].strip() and q[0] not in seen:
                seen.add(q[0])
                out.append((q[0], q[1]))
    with open(dst, "w", encoding="utf-8") as f:
        f.write("jp\tko\n")
        for jp, ko in out:
            f.write(f"{jp}\t{ko}\n")
    print(f"wrote {dst}: {len(out)} lines from {len(files)} staged file(s)")
    # build_kr globs translation/batch*.tsv now, so there is no loader list to
    # edit and no way to forget one.
    print("\nNext: python tools/tl.py font && python tools/build_kr.py"
          " && python tools/layout_list.py")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    p = sub.add_parser("next"); p.add_argument("count", type=int, nargs="?", default=200)
    p.add_argument("--tag"); p.add_argument("--real", action="store_true",
                   help="omit the permanently-flagged fragments")
    p.set_defaults(fn=cmd_next)
    for name, fn in (("check", cmd_check), ("stage", cmd_stage)):
        p = sub.add_parser(name); p.add_argument("tag"); p.set_defaults(fn=fn)
    p = sub.add_parser("lookup"); p.add_argument("term")
    p.add_argument("--limit", type=int, default=12); p.set_defaults(fn=cmd_lookup)
    sub.add_parser("audit").set_defaults(fn=cmd_audit)
    sub.add_parser("font").set_defaults(fn=cmd_font)
    p = sub.add_parser("finalize"); p.add_argument("--batch", type=int, required=True)
    p.set_defaults(fn=cmd_finalize)
    a = ap.parse_args()
    sys.exit(a.fn(a) or 0)


if __name__ == "__main__":
    main()
