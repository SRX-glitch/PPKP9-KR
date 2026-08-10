#!/usr/bin/env python3
"""Apply verbal-tic (語尾) consistency fixes across the worklists.

A character's tic is their voice. When the same tic is rendered one way in the
batches and another way in a shared file, the character stops sounding like one
person -- which is what `tools/tics.py` surfaced:

  ですぞ  12 lines -- 11 flattened to 「~습니다」, 1 already 하오체 「없소」.
          An old-fashioned emphatic-polite register; 하오체 is its Korean
          counterpart, it matches the line that was already right, and it is
          SHORTER than 습니다 so no budget can regress.
  っす    the batches use casual-polite 「~요」 (correct: it is junior/underling
          speech), but file4 rendered the same tic as deferential 「~습니까」,
          two registers for one character. Also shorter.

Every edit is keyed on the exact Japanese AND the exact current Korean, so a row
that has since been re-translated is reported rather than silently overwritten.
"""
import os, sys, glob, collections

BASE = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"

# (japanese, current korean, new korean)
FIXES = [
    # ですぞ -> 하오체
    ("これは、お近づきの印ですぞ。", "이건、친해지자는 표시입니다。", "이건、친해지자는 표시요。"),
    ("これを食べるといいですぞ。", "이걸 드시면 좋습니다。", "이걸 드시면 좋소。"),
    ("ですぞ。", "입니다。", "이오。"),
    ("君もまだまだですぞ。", "자네도 아직 멀었습니다。", "자네도 아직 멀었소。"),
    ("料理のレシピは、秘密ですぞ？", "요리 레시피는、비밀입니다？", "요리 레시피는、비밀이오？"),
    ("食べるとよいですぞ。", "드시면 좋습니다。", "드시면 좋소。"),
    ("こっちに勝ち目はないですぞ。", "이쪽에 승산은 없습니다。", "이쪽에 승산은 없소。"),
    ("これを、食べるといいですぞ。", "이걸 드시면 좋습니다。", "이걸 드시면 좋소。"),
    ("そう、アナタですぞ。", "그래、당신입니다。", "그렇소、당신이오。"),
    ("おいしいですぞ。", "맛있습니다。", "맛있소。"),
    ("大丈夫ですぞ。", "괜찮습니다。", "괜찮소。"),
    # っす -> casual-polite 「~요」, matching the 21 batch lines
    ("まだ、いるっすか？", "아직、있습니까？", "아직、있어요？"),
    ("今日はどうするっすか？", "오늘은 어떻게 합니까？", "오늘은 어떻게 해요？"),
    ("まじっすか！", "진심입니까！", "진심이에요！"),
    ("おもしろそうじゃないっすか！", "재미있어 보이잖습니까！", "재미있어 보이잖아요！"),
    ("おっす！", "옷스！", "안녕！"),
]


def files():
    return (sorted(glob.glob(BASE + "/translation/*.tsv"))
            + sorted(glob.glob(BASE + "/survey/common/file*_runs.tsv")))


def main():
    want = {(jp, old): new for jp, old, new in FIXES}
    done = collections.Counter()
    for fn in files():
        raw = open(fn, encoding="utf-8").read()
        lines = raw.splitlines()
        out, changed = [lines[0]], 0
        for ln in lines[1:]:
            p = ln.split("\t")
            if len(p) >= 2:
                # batches are (jp, ko); *_runs.tsv is (…, …, jp, ko, …)
                ji, ki = (0, len(p) - 1) if len(p) == 2 else (2, 3)
                if len(p) > max(ji, ki):
                    key = (p[ji], p[ki])
                    if key in want:
                        p[ki] = want[key]
                        ln = "\t".join(p)
                        done[key] += 1
                        changed += 1
            out.append(ln)
        if changed:
            open(fn, "w", encoding="utf-8", newline="").write(
                "\n".join(out) + ("\n" if raw.endswith("\n") else ""))
            print(f"{os.path.basename(fn):22s} {changed} line(s)")

    print()
    missed = [k for k in want if k not in done]
    print(f"applied {sum(done.values())} edits across {len(FIXES)} rules")
    for jp, old in missed:
        print(f"  NOT FOUND (re-translated since?): {jp!r} / {old!r}")
    return 1 if missed else 0


if __name__ == "__main__":
    sys.exit(main())
