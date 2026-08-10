#!/usr/bin/env python3
"""Move the encyclopedia's NAME records onto the pointer path.

The `<name>（<reading>）` rows are the maroon bar under the portrait. They were
left to `insert_tables`' in-place path and 120 of them already have Korean there,
so this reuses that instead of retranslating -- which is also what keeps the
spellings identical between the name bar and the index.

Through the pointer array their length is free, so the spacing convention can be
honoured everywhere (`마키무라 코조（마키무라코조）` -- surname and given name spaced
in the display form, run together inside the parentheses).

FIX carries the corrections that could not be applied in place because they made
the string longer, plus the ones that were simply wrong.

    python tools/gen_name_ko.py     -> appends to translation/profiles_ko.tsv
"""
import io, os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMON = os.path.join(BASE, "survey", "common")
WORK = os.path.join(COMMON, "file30_profiles.tsv")
TABLE = os.path.join(COMMON, "file30_table.tsv")
OUT = os.path.join(BASE, "translation", "profiles_ko.tsv")
NUL = "\\0"

# ⚠ Long vowels are NOT doubled -- 大村 is 오무라, established in session 30 and
# already shipped that way in the intro. The table path had 오오무라/오오타/오오가미.
# The rest are the surname/given-name space the in-place budget could not afford.
FIX = {
    "오오무라 테츠하루": "오무라 테츠하루",
    "오오무라 장관": "오무라 장관",
    "오오타 히로마사": "오타 히로마사",
    "오오가미 회장": "오가미 회장",
    "키가와노리오（키가와노리오）": "키가와 노리오（키가와노리오）",
    "아오시마사부로（아오시마사부로）": "아오시마 사부로（아오시마사부로）",
    "누쿠미즈치요（누쿠미즈치요）": "누쿠미즈 치요（누쿠미즈치요）",
    "본다다이스케（본다다이스케）": "본다 다이스케（본다다이스케）",
    "산다테루이에（산다테루이에）": "산다 테루이에（산다테루이에）",
    "곤다 마사오（곤다마사오）": "곤다 마사오（곤다마사오）",
}
# rows the table path never had
EXTRA = {
    "夏目准（なつめじゅん）": "나츠메 준（나츠메준）",
    "シルバー（＋ゴールド）": "실버（＋골드）",
    "リン": "린",
}


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    tbl = {}
    for ln in open(TABLE, encoding="utf-8").read().splitlines()[1:]:
        f = ln.split("\t")
        if len(f) >= 6 and f[5].strip():
            tbl[f[4]] = f[5].strip()

    done = {ln.split("\t")[0].strip().upper()
            for ln in open(OUT, encoding="utf-8").read().splitlines()[1:]}
    out, miss = [], []
    for ln in open(WORK, encoding="utf-8").read().splitlines()[1:]:
        f = ln.split("\t")
        if (len(f) > 5 and f[5].strip()) or f[0].strip().upper() in done:
            continue
        jp = f[4]
        core = jp.replace(NUL, "")
        ko = EXTRA.get(core) or tbl.get(core)
        if not ko:
            miss.append(core)
            continue
        ko = FIX.get(ko, ko)
        # keep the record's trailing padding so the field keeps its width
        m = re.search(r"((?:%s)+)$" % re.escape(NUL), jp)
        out.append(f"{f[0]}\t{ko}{m.group(1) if m else ''}")

    with open(OUT, "a", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"appended {len(out)} name records")
    if miss:
        print(f"  {len(miss)} without Korean: {miss[:6]}")


if __name__ == "__main__":
    main()
