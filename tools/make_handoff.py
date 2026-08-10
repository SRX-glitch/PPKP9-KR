#!/usr/bin/env python3
"""Build `handoff/` -- a self-contained package another translator (or an AI
running for them) can work from without this repo, the ROM, or an emulator.

What makes the package safe to hand out is that the Japanese is never retyped:
every line carries a stable `id`, the worker fills only the `ko` column, and
`handoff/validate.py` re-checks the id -> jp binding before anything comes back.
That is the same guard `tools/mkbatch.py` gave the in-repo workflow, after an
earlier batch silently lost 9 lines to invented Japanese.
"""
import os, sys, glob, json, hashlib, collections, datetime

sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P
from layout_audit import rows as display_rows

BASE = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"
OUT = f"{BASE}/handoff"
DATA = f"{OUT}/data"

# Lines the in-repo worksheet has always refused to surface: they would either
# corrupt the build or waste a translator's time. Kept identical to
# make_worksheet.py so the two views of "translatable" cannot drift.
PUNCT = "・。、！？～）（「」・…゛゜ー"


def meaningful(c):
    return c not in PUNCT and (0x3040 <= ord(c) <= 0x30FF or 0x4E00 <= ord(c) <= 0x9FFF)


def load_translated():
    """jp -> ko across every batch, last-wins, exactly like the build loader."""
    done = {}
    names = ["common_lines"] + sorted(
        (os.path.splitext(os.path.basename(p))[0]
         for p in glob.glob(f"{BASE}/translation/batch*.tsv")),
        key=lambda n: int(n[5:]))
    for name in names:
        p = f"{BASE}/translation/{name}.tsv"
        if not os.path.exists(p):
            continue
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            if "\t" not in ln:
                continue
            parts = ln.split("\t")
            jp, ko = parts[0].strip(), parts[1].strip()
            if jp and ko:
                done[jp] = ko
    return done


def load_corpus():
    runs = []
    for ln in open(f"{BASE}/survey/ov28/dialogue_runs.tsv", encoding="utf-8").read().splitlines():
        p = ln.split("\t")
        if len(p) >= 4:
            runs.append((int(p[0], 16), int(p[1]), p[3]))
    runs.sort()
    return runs


def main():
    os.makedirs(DATA, exist_ok=True)
    done = load_translated()
    runs = load_corpus()

    occ = collections.Counter(jp for _, _, jp in runs)
    first_at = {}
    for i, (off, _, jp) in enumerate(runs):
        first_at.setdefault(jp, i)

    # ---- untranslated worklist -------------------------------------------
    rows = []
    for jp, n in occ.items():
        if jp in done:
            continue
        if len([c for c in jp if meaningful(c)]) < 3:
            continue                      # symbols, ellipses, single kana
        if jp[-1] in "見投打昨喫":
            continue                      # typical parser-cut endings
        if any(c in jp for c in "尅㎞"):
            continue                      # gaiji / mis-decoded artifacts
        rows.append((n, jp))
    rows.sort(key=lambda r: (-r[0], -len(r[1])))

    # The id is derived from the Japanese itself, never from position in this
    # list. A sequential id would be reassigned to a DIFFERENT line every time
    # this file is regenerated (each merged batch removes lines and pulls the
    # rest up), so a shard still out with a translator would silently bind to
    # the wrong source text on the way back. A content hash is stable forever
    # and needs no state carried between runs.
    def rid(jp):
        return "L" + hashlib.sha1(jp.encode("utf-8")).hexdigest()[:10]

    clash = collections.Counter(rid(jp) for _, jp in rows)
    dupes = [i for i, c in clash.items() if c > 1]
    if dupes:                              # 40 bits over ~7k lines: ~1-in-25000
        raise SystemExit(f"id collision: {dupes} -- widen the hash slice")

    with open(f"{DATA}/untranslated.tsv", "w", encoding="utf-8") as f:
        f.write("id\tocc\tmax\tprev\tjp\tnext\tko\n")
        for n, jp in rows:
            i = first_at[jp]
            prev = runs[i - 1][2] if i > 0 else ""
            nxt = runs[i + 1][2] if i + 1 < len(runs) else ""
            f.write(f"{rid(jp)}\t{n}\t{19 * display_rows(jp)}\t{prev}\t{jp}\t{nxt}\t\n")
    print(f"untranslated.tsv: {len(rows)} lines, {sum(n for n, _ in rows)} occurrences")

    json.dump({
        "generated": datetime.date.today().isoformat(),
        "untranslated_lines": len(rows),
        "untranslated_occurrences": sum(n for n, _ in rows),
        "translated_lines": len(done),
        "coverage_runs": f"{len(runs) - sum(occ[jp] for jp in occ if jp not in done)}"
                         f"/{len(runs)}",
        "id_scheme": "L + sha1(jp)[:10] -- stable across regenerations, so a "
                     "shard cut from an older copy still merges correctly",
    }, open(f"{DATA}/manifest.json", "w", encoding="utf-8"),
        ensure_ascii=False, indent=1)

    # ---- reference: everything already translated ------------------------
    with open(f"{DATA}/reference_translations.tsv", "w", encoding="utf-8") as f:
        f.write("jp\tko\n")
        for jp in sorted(done, key=lambda s: -occ.get(s, 0)):
            f.write(f"{jp}\t{done[jp]}\n")
    print(f"reference_translations.tsv: {len(done)} lines")

    # ---- glossary: short, frequent, already-settled renderings ------------
    # A short line that recurs is in practice a term: a name, a shout, a menu
    # label. Shipping them as a glossary is what keeps a second translator's
    # output consistent with 12k lines they will never read.
    gl = [(occ[jp], jp, ko) for jp, ko in done.items()
          if jp in occ and len(jp) <= 8 and occ[jp] >= 3]
    gl.sort(key=lambda r: (-r[0], r[1]))
    with open(f"{DATA}/glossary_auto.tsv", "w", encoding="utf-8") as f:
        f.write("occ\tjp\tko\n")
        for n, jp, ko in gl:
            f.write(f"{n}\t{jp}\t{ko}\n")
    print(f"glossary_auto.tsv: {len(gl)} recurring short terms")

    # ---- the character whitelist the encoder will actually accept ---------
    allowed = sorted(P.CH2CC)
    json.dump({
        "note": "Hangul syllables U+AC00..U+D7A3 and the space are always OK. "
                "Everything else must appear in `chars`.",
        "chars": "".join(allowed),
    }, open(f"{DATA}/allowed_chars.json", "w", encoding="utf-8"),
        ensure_ascii=False, indent=1)
    print(f"allowed_chars.json: {len(allowed)} non-Hangul characters")

    # ---- syllable budget snapshot ----------------------------------------
    used = {c for ko in done.values() for c in ko if 0xAC00 <= ord(c) <= 0xD7A3}
    json.dump({
        "font_slots": 1658,
        "syllables_used_now": len(used),
        "syllables_free": 1658 - len(used),
        # The set itself, so validate.py can report how many syllables a
        # submission ADDS. Reporting its raw syllable count instead invites a
        # comparison against the free slots that is wrong by an order of
        # magnitude -- most of a submission's syllables are already in use.
        "syllables_in_use": "".join(sorted(used)),
        "note": "Distinct Hangul syllables across ALL translations must stay "
                "under font_slots. The build aborts loudly if it does not.",
    }, open(f"{DATA}/font_budget.json", "w", encoding="utf-8"),
        ensure_ascii=False, indent=1)
    print(f"font_budget.json: {len(used)}/1658 syllables used")


if __name__ == "__main__":
    main()
