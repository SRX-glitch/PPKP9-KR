#!/usr/bin/env python3
"""Quality audit for a returned handoff submission.

`handoff/validate.py` proves a file is *mechanically* loadable: right ids, legal
glyphs, inside the width budget. It deliberately says nothing about whether the
Korean is a translation at all -- and it cannot, because every Japanese kanji is
a legal game charcode, so source text pasted into the `ko` column passes every
mechanical check and would ship as Japanese.

This is the second gate: does the submission actually contain Korean, and does
it follow the policy the package shipped with?

    python tools/qa_submission.py handoff/work/*.tsv
    python tools/qa_submission.py handoff/work/*.tsv --write-clean clean.tsv
"""
import sys, io, os, glob, argparse, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HANGUL = range(0xAC00, 0xD7A4)


def is_han(c):
    return ord(c) in HANGUL


def is_kanji(c):
    return "一" <= c <= "鿿"


def is_kana(c):
    # Deliberately excludes U+30FB `・` and U+30FC `ー`: they live in the
    # katakana block but are the punctuation every translation here is
    # supposed to use, so counting them as Japanese flags correct work.
    return "ぁ" <= c <= "ゖ" or "ァ" <= c <= "ヺ"


# (label, does the jp line trigger this rule, does the ko line satisfy it)
TICS = [
    ("でやんす",  lambda jp: "でやんす" in jp,
                  lambda ko: any(t in ko for t in ("죠", "쇼"))),
    ("カニ 어미", lambda jp: "カニ" in jp,
                  lambda ko: "게" in ko),
    ("ムシャ",    lambda jp: "ムシャ" in jp,
                  lambda ko: "우걱" in ko),
    ("ボ～ク",    lambda jp: "ボ～ク" in jp,
                  lambda ko: "나～" in ko or "내～" in ko),
    # ちゃんと is the adverb "properly", not the honorific -- counting it as a
    # 짱 violation produces a flood of false positives.
    ("ちゃん 호칭", lambda jp: "ちゃん" in jp and "ちゃんと" not in jp
                             and not any(t in jp for t in
                                 ("おじちゃん", "おばちゃん", "おじいちゃん",
                                  "おばあちゃん", "じいちゃん", "ばあちゃん",
                                  "母ちゃん", "父ちゃん", "兄ちゃん", "姉ちゃん")),
                  lambda ko: "짱" in ko),
]


def load(paths):
    rows = []
    for p in paths:
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            q = ln.split("\t")
            if len(q) >= 7 and q[0].strip():
                rows.append({"file": os.path.basename(p), "id": q[0],
                             "prev": q[3], "jp": q[4], "next": q[5],
                             "ko": q[6].strip()})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--write-clean", metavar="PATH",
                    help="write only the rows that pass every hard check")
    ap.add_argument("--show", type=int, default=6)
    a = ap.parse_args()

    paths = []
    for pat in a.files:
        paths.extend(sorted(glob.glob(pat)) or [pat])
    rows = load(paths)
    tr = [r for r in rows if r["ko"]]
    print(f"{len(rows)} rows, {len(tr)} translated, {len(rows) - len(tr)} blank\n")

    # ---- hard defects: these are not translations ------------------------
    no_hangul, mixed, echoed = [], [], []
    for r in tr:
        ko, jp = r["ko"], r["jp"]
        han = any(is_han(c) for c in ko)
        cjk = [c for c in ko if is_kanji(c) or is_kana(c)]
        if cjk and not han:
            no_hangul.append(r)
        elif cjk and han:
            mixed.append(r)
        if ko == jp:
            echoed.append(r)

    def dump(title, items, fmt):
        print(f"■ {title}: {len(items)}줄")
        for r in items[:a.show]:
            print("   " + fmt(r))
        if len(items) > a.show:
            print(f"   ... 외 {len(items) - a.show}줄")
        print()

    dump("한글이 전혀 없음 (원문 조각을 그대로 둠 — 번역 아님)", no_hangul,
         lambda r: f"{r['jp']}  ->  {r['ko']}")
    dump("한글 단어 속에 한자가 섞임 (깨진 출력)", mixed,
         lambda r: f"{r['jp']}  ->  {r['ko']}")
    if echoed:
        dump("ko가 jp와 완전히 동일", echoed, lambda r: r["ko"])

    # ---- policy adherence -------------------------------------------------
    print("■ 말버릇 방침 준수")
    for label, trig, ok in TICS:
        hit = [r for r in tr if trig(r["jp"])]
        bad = [r for r in hit if not ok(r["ko"])]
        pct = f"{100 * (len(hit) - len(bad)) / len(hit):.0f}%" if hit else "-"
        print(f"   {label:<12} 대상 {len(hit):>4}줄  미반영 {len(bad):>4}줄  준수율 {pct}")
    print()

    # ---- the leading choice-index kana the policy says to keep ------------
    # A real marker is a lone kana welded straight onto a kanji word ("い読む"),
    # which ordinary Japanese does not produce. Testing only "starts with a
    # kana" instead flags いつも/いったい and reports every sentence in the file.
    # `お` is the honorific prefix (お前/お宝/お嬢様), not a choice index --
    # including it made this check report every sentence in the file.
    MARK = "いうえかきくけこさしすせそ"
    markers = [r for r in tr
               if len(r["jp"]) > 2 and r["jp"][0] in MARK and is_kanji(r["jp"][1])]
    lost = [r for r in markers if not r["ko"] or r["ko"][0] not in MARK]
    print(f"■ 선택지 마커 가나: 후보 {len(markers)}줄 중 마커 소실 {len(lost)}줄")
    for r in lost[:3]:
        print(f"   {r['jp']}  ->  {r['ko']}")
    print()

    # ---- a translation of the NEXT line, mis-filed on this row ------------
    shifted = []
    for r in tr:
        kj = {c for c in r["ko"] if is_kanji(c)}
        if kj and len(kj & set(r["next"])) > len(kj & set(r["jp"])):
            shifted.append(r)
    dump("이웃 줄 내용으로 보이는 번역 (행 밀림 의심)", shifted,
         lambda r: f"jp={r['jp']} | next={r['next']} | ko={r['ko']}")

    bad_ids = {r["id"] for r in no_hangul} | {r["id"] for r in mixed} \
        | {r["id"] for r in shifted} | {r["id"] for r in echoed}
    print(f"=> 확실히 폐기해야 할 줄: {len(bad_ids)} / {len(tr)} "
          f"({100 * len(bad_ids) / len(tr):.1f}%)")

    if a.write_clean:
        keep = [r for r in tr if r["id"] not in bad_ids]
        with open(a.write_clean, "w", encoding="utf-8") as f:
            f.write("id\tocc\tmax\tprev\tjp\tnext\tko\n")
            for r in keep:
                f.write(f"{r['id']}\t\t\t{r['prev']}\t{r['jp']}\t{r['next']}\t{r['ko']}\n")
        print(f"\nwrote {a.write_clean}: {len(keep)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
