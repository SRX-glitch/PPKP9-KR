#!/usr/bin/env python3
"""Read the extra worklist the way the PLAYER reads it: in offset order, whole
message boxes at a time, so a sentence split across two runs can be judged.

Why this exists: `extra_worksheet.py` sorts by occurrence and byte budget, so the
lines of one sentence land in different batches and get translated in isolation.
27% of file 4's translated rows are mid-sentence continuations -- those only read
correctly if the neighbouring line was written to match. This dumps the groups so
that can actually be checked, and prints the byte budget of every line so a
revision can be sized before it goes into translation/extra_overrides.tsv.

    python3 tools/flow_review.py 4 --n 60            # first 60 risky groups
    python3 tools/flow_review.py 4 --n 60 --skip 60
    python3 tools/flow_review.py 4 --all             # every group, not just risky

A group is a run of rows whose offsets are within --gap bytes of each other, i.e.
one message box. "Risky" = the group contains a translated row whose Japanese does
not end in sentence-final punctuation, so the sentence carries into the next line.
"""
import argparse, csv, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

JP_SENT_END = ('。', '！', '？', '」', '）', '～', '、')


def load(fid):
    path = os.path.join(HERE, '..', 'survey', 'common', f'file{fid}_extra.tsv')
    rows = list(csv.reader(open(path, encoding='utf-8'), delimiter='\t'))
    h = rows[0]
    oi, ji, ki, bi = h.index('offset'), h.index('jp'), h.index('ko'), h.index('budget')
    out = []
    for r in rows[1:]:
        if len(r) <= ki:
            continue
        out.append((int(r[oi], 16), int(r[bi]), r[ji], r[ki].strip()))
    out.sort()
    return out


def group(data, gap):
    groups, cur = [], [data[0]]
    for prev, nxt in zip(data, data[1:]):
        if nxt[0] - prev[0] <= gap:
            cur.append(nxt)
        else:
            groups.append(cur)
            cur = [nxt]
    groups.append(cur)
    return groups


def risky(g):
    """Does this group contain a translated line whose sentence runs on?"""
    for i, (o, b, jp, ko) in enumerate(g[:-1]):
        if ko and not jp.strip().endswith(JP_SENT_END):
            return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('fid', type=int)
    ap.add_argument('--n', type=int, default=60)
    ap.add_argument('--skip', type=int, default=0)
    ap.add_argument('--gap', type=int, default=40)
    ap.add_argument('--all', action='store_true', help='include groups with no run-on line')
    a = ap.parse_args()

    data = load(a.fid)
    groups = group(data, a.gap)
    sel = groups if a.all else [g for g in groups if risky(g)]
    total = len(sel)
    sel = sel[a.skip:a.skip + a.n]

    print(f'# file {a.fid}: {total} groups to review; showing {a.skip}..{a.skip + len(sel)}')
    print('# budget is per LINE -- a revision must fit the same line it replaces.\n')
    for g in sel:
        print(f'--- 0x{g[0][0]:X} ---')
        for o, b, jp, ko in g:
            run_on = '' if jp.strip().endswith(JP_SENT_END) else '  <<continues'
            print(f'  [{b:>2}] {jp}{run_on}')
            print(f'       {ko if ko else "(untranslated)"}')
        print()


if __name__ == '__main__':
    main()
