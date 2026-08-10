#!/usr/bin/env python3
"""Rank `flow_review` groups by how likely the Korean is actually broken.

`flow_review.py` dumps every group whose Japanese runs on past the line break --
1,573 of them across files 4/25/27, ~17,500 printed lines. Reading all of them in
order is not a plan; most are already fine. This scores them so the ones that are
mechanically wrong come first.

The detectors session 34 wrote covered two classes (dropped connective particle,
report-style 되/함/음 endings in dialogue). Two more show up when you read the
dumps, and neither was ever measured:

  [E] a mid-sentence line whose Korean ends in a SENTENCE-FINAL ending
      (~다 ~요 ~죠 ~까 ~네 ~군 ~야 ~지). The player sees the sentence close and
      then the next box starts with its tail. 「돌아왔다 / 나는」.
  [F] a mid-sentence line whose Korean ends in a NOUN with no particle while the
      Japanese ended in a real particle. Same defect session 34 chased, but its
      detector only looked at the FOLLOWING line's opening; this looks at the
      line's own tail, which catches the other half.

    python3 tools/flow_rank.py 4 --n 40            # 40 worst groups, flow format
    python3 tools/flow_rank.py 4 --n 40 --skip 40
    python3 tools/flow_rank.py 4 --counts          # just the class histogram
"""
import argparse, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import flow_review as FR

# Sentence-final Korean endings. Deliberately anchored to the very last syllable
# plus optional punctuation -- 「~한다」 mid-sentence is fine as a modifier
# (「~한다는」) but never as the last thing on the line.
FINAL = re.compile(
    r'(다|요|죠|까|네|군|야|지|어|워|해|줘|봐|자|랴|니|나|damn)[。．\.！!？\?~～…、]*$')
# ...minus the ones that legitimately continue: 「~다는」 is already excluded by the
# anchor, but a connective 「~고」「~서」「~며」「~면」「~데」「~니까」 must NOT score.
CONT_END = re.compile(r'(고|서|며|면|데|까|나|자|든|든지|거나|지만|는데|니까|어서|아서|'
                      r'려고|러|도록|듯|처럼|같이|보다|부터|까지|에서|으로|로|와|과|'
                      r'의|을|를|이|가|은|는|도|만|에|께|한테|더러|보고)$')

# Japanese particles that guarantee the sentence keeps going.
JP_CONN = ('の', 'が', 'は', 'を', 'に', 'で', 'と', 'も', 'から', 'まで', 'より',
           'へ', 'や', 'ば', 'て', 'ても', 'たら', 'なら', 'けど', 'けれど', 'し',
           'ながら', 'ので', 'のに', 'って', 'という', 'な')
# Korean particles / connective endings that legitimately close a mid-sentence line.
KO_PARTICLE = ('은', '는', '이', '가', '을', '를', '의', '에', '에서', '으로', '로',
               '와', '과', '도', '만', '부터', '까지', '보다', '한테', '께', '라',
               '고', '서', '며', '면', '데', '지만', '는데', '니까', '아서', '어서',
               '려고', '러', '든', '거나', '처럼', '같이', '대로', '뿐', '밖에')

HANGUL = re.compile(r'[가-힣]')


def classes(g):
    """{class letter} for one group."""
    out = set()
    for i, (o, b, jp, ko) in enumerate(g[:-1]):
        if not ko or not HANGUL.search(ko):
            continue
        jps = jp.strip()
        if jps.endswith(FR.JP_SENT_END):
            continue                      # not a run-on line
        nxt = g[i + 1][3].strip()
        if not nxt or not HANGUL.search(nxt):
            continue                      # neighbour untranslated: nothing to judge
        k = ko.strip().rstrip('　 ')
        if CONT_END.search(k):
            continue                      # ends on a connective: fine
        if FINAL.search(k):
            out.add('E')
            continue
        if jps.endswith(JP_CONN) and not k.endswith(KO_PARTICLE):
            out.add('F')
    return out


def score(cls):
    return 3 * ('E' in cls) + 2 * ('F' in cls)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('fid', type=int)
    ap.add_argument('--n', type=int, default=40)
    ap.add_argument('--skip', type=int, default=0)
    ap.add_argument('--gap', type=int, default=40)
    ap.add_argument('--counts', action='store_true')
    a = ap.parse_args()

    groups = [g for g in FR.group(FR.load(a.fid), a.gap) if FR.risky(g)]
    ranked = []
    hist = {}
    for g in groups:
        c = classes(g)
        if not c:
            continue
        hist[''.join(sorted(c))] = hist.get(''.join(sorted(c)), 0) + 1
        ranked.append((-score(c), g[0][0], ''.join(sorted(c)), g))
    ranked.sort()

    if a.counts:
        print(f'# file {a.fid}: {len(groups)} run-on groups, '
              f'{len(ranked)} flagged')
        for k in sorted(hist):
            print(f'  {k}: {hist[k]}')
        return

    sel = ranked[a.skip:a.skip + a.n]
    print(f'# file {a.fid}: {len(ranked)} flagged groups; '
          f'showing {a.skip}..{a.skip + len(sel)}')
    for _s, _o, cls, g in sel:
        print(f'--- 0x{g[0][0]:X}  [{cls}] ---')
        for o, b, jp, ko in g:
            run_on = '' if jp.strip().endswith(FR.JP_SENT_END) else '  <<'
            print(f'  0x{o:X} [{b:>2}] {jp}{run_on}')
            print(f'          {ko if ko else "(untranslated)"}')
        print()


if __name__ == '__main__':
    main()
