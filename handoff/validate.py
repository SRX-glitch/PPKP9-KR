#!/usr/bin/env python3
"""Check a filled-in shard before sending it back. Python 3.8+, standard library only.

    python validate.py work/shard_001.tsv
    python validate.py work/*.tsv

Everything this catches is something that would otherwise fail late -- during a
40-minute ROM build, or worse, silently: a line that renders past the text box,
a character the game has no glyph for, or an id whose Japanese was edited and no
longer matches any line in the script.

Exit code 0 = clean, 1 = problems found.
"""
import sys, os, json, glob, unicodedata

# Error messages quote the Japanese source and the Korean translation, and this
# script gets piped to a file or a log at least as often as it gets read on a
# console. When stdout is not a console Python falls back to the locale encoding
# -- cp949 on a Korean Windows -- and the quotes come out as mojibake, or raise
# UnicodeEncodeError outright on a character the codepage lacks.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

HANGUL = range(0xAC00, 0xD7A4)
# ASCII look-alikes that have no charcode. The fullwidth twin is the fix, and
# naming it in the error is the difference between a 5-second and a 20-minute fix.
LOOKALIKE = {"(": "（", ")": "）", "~": "～", "%": "％", "—": "～",
             "!": "！", "?": "？", ",": "、", ".": "。", '"': "「",
             "'": "「", ":": "：", ";": "；"}


def load_master():
    master = {}
    path = os.path.join(DATA, "untranslated.tsv")
    with open(path, encoding="utf-8") as f:
        for ln in f.read().splitlines()[1:]:
            p = ln.split("\t")
            if len(p) >= 6:
                master[p[0]] = {"occ": int(p[1]), "max": int(p[2]), "jp": p[4]}
    return master


def load_allowed():
    with open(os.path.join(DATA, "allowed_chars.json"), encoding="utf-8") as f:
        return set(json.load(f)["chars"])


def check_file(path, master, allowed, seen_ids, syllables, seen_ko):
    errs, warns, n = [], [], 0
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    if not lines:
        return 0, [f"{path}: empty file"], []

    head = lines[0].split("\t")
    # `jp` is required, not optional: it is the second witness that proves an
    # id still points at the text the translator was looking at. Send back the
    # shard file with its ko column filled -- not a bare id/ko list.
    try:
        i_id, i_ko, i_jp = head.index("id"), head.index("ko"), head.index("jp")
    except ValueError:
        return 0, [f"{path}: header must contain 'id', 'jp' and 'ko' columns, "
                   f"got {head}. Fill in the shard file itself rather than "
                   f"building a new id/ko file."], []

    for lineno, ln in enumerate(lines[1:], 2):
        if not ln.strip():
            continue
        p = ln.split("\t")
        if len(p) <= max(i_id, i_ko):
            errs.append(f"{path}:{lineno}: too few columns")
            continue
        rid, ko = p[i_id].strip(), p[i_ko].strip()
        if not rid:
            continue
        if rid not in master:
            errs.append(f"{path}:{lineno}: id {rid!r} is not in the current "
                        f"worklist -- either it was mistyped, or someone else "
                        f"translated this line and it dropped out of "
                        f"data/untranslated.tsv after your shard was cut. "
                        f"Safe to delete the row.")
            continue
        m = master[rid]

        # If the jp drifted, the worker edited the source text and the id no
        # longer means what they think it does.
        if len(p) <= i_jp or p[i_jp] != m["jp"]:
            errs.append(f"{path}:{lineno}: {rid} jp column was modified -- "
                        f"never edit it; restore {m['jp']!r}")
            continue
        if not ko:
            continue                      # untranslated is allowed, just skipped

        n += 1
        if rid in seen_ids:
            errs.append(f"{path}:{lineno}: {rid} already translated in {seen_ids[rid]}")
            continue
        seen_ids[rid] = os.path.basename(path)

        if len(ko) > m["max"]:
            errs.append(f"{path}:{lineno}: {rid} is {len(ko)} glyphs, max {m['max']}"
                        f"  ->  {ko}")
        for ch in ko:
            if ch == " " or ord(ch) in HANGUL:
                continue
            if ch not in allowed:
                fix = LOOKALIKE.get(ch)
                hint = f" -- use {fix!r} instead" if fix else ""
                name = unicodedata.name(ch, "?")
                errs.append(f"{path}:{lineno}: {rid} has no glyph for {ch!r} "
                            f"({name}){hint}")
        for ch in ko:
            if 0x1100 <= ord(ch) <= 0x11FF or 0x3130 <= ord(ch) <= 0x318F:
                errs.append(f"{path}:{lineno}: {rid} contains a bare jamo {ch!r} -- "
                            f"only precomposed syllables exist in the font")
        # Every Japanese kanji is a legal game charcode, so source text left in
        # the ko column passes every check above and would ship as Japanese.
        # The worklist only contains lines with at least three meaningful
        # Japanese characters, so a translation with no Hangul at all is always
        # wrong -- whether what is left is source text or bare punctuation.
        # (Requiring CJK to be present here let 1,597 rows of "。" through.)
        # `・` (U+30FB) and `ー` (U+30FC) sit in the katakana block but are the
        # punctuation this project is required to use -- the policy says match
        # the source's ellipsis dots, and every existing translation does.
        # Treating the whole block as "Japanese" flags correct work.
        cjk = [c for c in ko if "一" <= c <= "鿿"
               or "ぁ" <= c <= "ゖ" or "ァ" <= c <= "ヺ"]
        if not any(ord(c) in HANGUL for c in ko):
            what = "source text" if cjk else "punctuation only"
            errs.append(f"{path}:{lineno}: {rid} has no Hangul at all "
                        f"({what}), not a translation: {ko!r}")
        elif cjk:
            # A choice-index marker is kana at the very start of the line, kept
            # verbatim per policy ("い読む" -> "い읽는다"). Anything Japanese
            # after that is contamination. Matching by position rather than by a
            # list of allowed kana is what makes "ふふ"/"へへ" markers pass too.
            body = ko
            while body and ("ぁ" <= body[0] <= "ゖ" or "ァ" <= body[0] <= "ヺ"):
                body = body[1:]
            rest = [c for c in body if "一" <= c <= "鿿"
                    or "ぁ" <= c <= "ゖ" or "ァ" <= c <= "ヺ"]
            if rest:
                errs.append(f"{path}:{lineno}: {rid} mixes Japanese into Korean "
                            f"({''.join(rest)}): {ko!r}")
        if ko == m["jp"]:
            errs.append(f"{path}:{lineno}: {rid} ko is identical to jp")

        # Two cheap smells for the failure this package cannot check directly:
        # Korean that reads fine but belongs to a different line. Warnings, not
        # errors -- both have honest exceptions -- but in the rejected first
        # round they fired on hundreds of rows.
        seen_ko.setdefault(ko, []).append((path, lineno, m["jp"]))
        src = [c for c in m["jp"] if c not in "・。、！？（）「」…～"]
        dst = [c for c in ko if c not in "・。、！？（）「」…～"]
        if len(src) >= 8 and len(dst) <= len(src) * 0.35:
            warns.append(f"{path}:{lineno}: {rid} is far shorter than the source "
                         f"({len(src)} -> {len(dst)} chars) -- is the whole line "
                         f"translated?  {m['jp']!r} -> {ko!r}")
        syllables.update(c for c in ko if ord(c) in HANGUL)
    return n, errs, warns


def main(argv):
    paths = []
    for a in argv:
        paths.extend(sorted(glob.glob(a)) or [a])
    if not paths:
        print(__doc__)
        return 1

    master, allowed = load_master(), load_allowed()
    with open(os.path.join(DATA, "font_budget.json"), encoding="utf-8") as f:
        budget = json.load(f)

    seen, syllables, seen_ko = {}, set(), {}
    total, all_errs, all_warns = 0, [], []
    for p in paths:
        n, e, w = check_file(p, master, allowed, seen, syllables, seen_ko)
        total += n
        all_errs += e
        all_warns += w

    # The same Korean filed against several different Japanese lines means one
    # sentence was smeared across unrelated rows -- 557 rows did this in the
    # rejected first round.
    for ko, hits in sorted(seen_ko.items()):
        if len(hits) > 1 and len(ko) > 4:
            all_warns.append(
                f"{hits[0][0]}:{hits[0][1]}: {ko!r} is used for {len(hits)} "
                f"different source lines, e.g. " +
                " / ".join(repr(h[2]) for h in hits[:3]))

    for w in all_warns:
        print("WARN  " + w)
    for e in all_errs:
        print("ERROR " + e)

    occ = sum(master[i]["occ"] for i in seen)
    print(f"\n{total} translated lines, {occ} in-game occurrences")

    # Only syllables the project does not already have consume a font slot.
    # Printing the submission's raw syllable count next to the free-slot count
    # reads as "937 needed, 551 available" when the true cost is a few dozen.
    in_use = set(budget.get("syllables_in_use", ""))
    added = syllables - in_use if in_use else syllables
    print(f"new Hangul syllables added by this submission: {len(added)} "
          f"(free font slots: {budget['syllables_free']} of {budget['font_slots']})")
    if len(added) > budget["syllables_free"]:
        print("  WARNING: this exceeds the free font slots -- tell the maintainer.")
    if all_errs:
        print(f"\n{len(all_errs)} error(s) -- fix these before sending the file back.")
        return 1
    print("\nOK - no errors.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
