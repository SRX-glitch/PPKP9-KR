#!/usr/bin/env python3
"""Fold shards returned by an outside translator back into `translation/`.

    python tools/merge_handoff.py handoff/work/shard_00*.tsv --batch 119

Re-runs every check `handoff/validate.py` does -- returned files have been round
tripped through someone else's editor or spreadsheet, so the id -> jp binding is
re-verified against the corpus here rather than trusted.

Writes `translation/batch<N>.tsv` and prints the loader line to paste into
build_kr.main(). Nothing is written if any line fails.
"""
import os, sys, glob, argparse, collections

sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P
from layout_audit import rows as display_rows

BASE = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"
HANGUL = range(0xAC00, 0xD7A4)


def corpus_keys():
    keys = collections.Counter()
    for ln in open(f"{BASE}/survey/ov28/dialogue_runs.tsv", encoding="utf-8").read().splitlines():
        p = ln.split("\t")
        if len(p) >= 4:
            keys[p[3]] += 1
    return keys


def master_ids():
    """id -> jp, from the handoff worklist that was actually shipped."""
    m = {}
    path = f"{BASE}/handoff/data/untranslated.tsv"
    for ln in open(path, encoding="utf-8").read().splitlines()[1:]:
        p = ln.split("\t")
        if len(p) >= 6:
            m[p[0]] = p[4]
    return m


def already_translated():
    done = set()
    for p in glob.glob(f"{BASE}/translation/batch*.tsv") + [f"{BASE}/translation/common_lines.tsv"]:
        if not os.path.exists(p):
            continue
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            if "\t" in ln:
                jp, ko = (ln.split("\t") + [""])[:2]
                if jp.strip() and ko.strip():
                    done.add(jp.strip())
    return done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--batch", type=int, required=True, help="output batch number")
    a = ap.parse_args()

    paths = []
    for pat in a.files:
        paths.extend(sorted(glob.glob(pat)) or [pat])

    keys, master, done = corpus_keys(), master_ids(), already_translated()
    pairs, errs, seen = [], [], {}

    for path in paths:
        lines = open(path, encoding="utf-8").read().splitlines()
        if not lines:
            continue
        head = lines[0].split("\t")
        # `jp` is mandatory here even though `id` alone would look sufficient.
        # It is the independent second witness: if a shard was cut from an older
        # handoff copy, or an id was mistyped, the jp comparison below is what
        # turns that into a loud error instead of the wrong Korean landing on
        # the wrong line. Accepting a bare id/ko file would remove that check
        # exactly when it is most needed.
        try:
            i_id, i_ko, i_jp = head.index("id"), head.index("ko"), head.index("jp")
        except ValueError:
            errs.append(f"{path}: header needs 'id', 'jp' and 'ko' columns "
                        f"(got {head}). Fill the ko column of the original "
                        f"shard file rather than sending a bare id/ko list.")
            continue

        for n, ln in enumerate(lines[1:], 2):
            if not ln.strip():
                continue
            p = ln.split("\t")
            if len(p) <= max(i_id, i_ko):
                continue
            rid, ko = p[i_id].strip(), p[i_ko].strip()
            if not rid or not ko:
                continue
            if rid not in master:
                # Most "unknown" ids are not typos: the line was translated by
                # someone else and dropped out of the worklist after this shard
                # was cut. Saying so turns a scary error into a shrug.
                shard_jp = p[i_jp].strip() if len(p) > i_jp else ""
                if shard_jp in done:
                    errs.append(f"{path}:{n}: {rid} was translated by someone "
                                f"else since this shard was cut -- delete this "
                                f"row and re-merge")
                else:
                    errs.append(f"{path}:{n}: unknown id {rid}")
                continue
            jp = master[rid]
            if len(p) <= i_jp or p[i_jp] != jp:
                errs.append(f"{path}:{n}: {rid} jp column does not match the "
                            f"worklist -- expected {jp!r}")
                continue
            if jp not in keys:
                errs.append(f"{path}:{n}: {rid} jp not found in corpus")
                continue
            if rid in seen:
                errs.append(f"{path}:{n}: {rid} duplicated (also {seen[rid]})")
                continue
            seen[rid] = f"{os.path.basename(path)}:{n}"
            if jp in done:
                errs.append(f"{path}:{n}: {rid} was already translated in an earlier batch")
                continue
            cap = 19 * display_rows(jp)
            if len(ko) > cap:
                errs.append(f"{path}:{n}: {rid} {len(ko)} glyphs > {cap}  -> {ko}")
            for ch in ko:
                if ch == " " or ord(ch) in HANGUL:
                    continue
                if P.CH2CC.get(ch) is None:
                    errs.append(f"{path}:{n}: {rid} no glyph for {ch!r} -> {ko}")
            pairs.append((jp, ko))

    for e in errs:
        print("ERROR " + e)
    if errs:
        print(f"\n{len(errs)} error(s); nothing written.")
        return 1

    dst = f"{BASE}/translation/batch{a.batch}.tsv"
    if os.path.exists(dst):
        print(f"ERROR {dst} already exists; pick another --batch")
        return 1
    with open(dst, "w", encoding="utf-8") as f:
        f.write("jp\tko\n")
        for jp, ko in pairs:
            f.write(f"{jp}\t{ko}\n")

    occ = sum(keys[jp] for jp, _ in pairs)
    print(f"wrote {dst}: {len(pairs)} lines, {occ} occurrences")
    print(f'\nAdd to build_kr.main() loader:  "batch{a.batch}.tsv",')
    print("Then: python tools/build_kr.py && python tools/layout_list.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
