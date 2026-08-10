#!/usr/bin/env python3
"""Sweep EVERY translated line in the project for the defect classes that a
line-by-line workflow produces, and that no build gate can see.

The build gates prove the bytes land where the game reads them. They say nothing
about whether the Korean is Korean. These checks are the ones that actually
caught defects in file 4:

  A leak      Japanese kana/kanji left inside the Korean field
  B register  report-style ~됨/~함/~음 used in spoken dialogue (menu-only forms)
  C clash     한 줄 안에서 반말 호칭 + 존댓말 종결
  D echo      Korean identical to the Japanese (marked translated but is not)
  E spacing   doubled spaces / space before punctuation
  F nakaguro  ・ used where the Japanese had no ・ (Korean list separator is fine,
              but a ・ we invented is usually a dropped 와/과)

    python3 tools/tl_audit.py            # counts + 8 samples each
    python3 tools/tl_audit.py --show 40  # more samples
    python3 tools/tl_audit.py --only B,C

Sources swept: translation/batch*.tsv (main scenario) and every survey worklist
that has a `ko` column. Fixes go to the same place the build reads them from --
batch files for scenario lines, translation/extra_overrides.tsv for extra rows.
"""
import argparse, csv, glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')

# ・(30FB) ～(FF5E) ー(30FC) are punctuation the Korean text legitimately reuses.
KANA = re.compile(r'[぀-ゟ゠-ヺヽ-ヿ一-鿿]')
NOUN_FINAL = re.compile(r'(음|함|됨)[。！？]?$')
BANMAL = re.compile(r'(^|[ 、])(너|넌|네가|니가|너희|너흰|자네|얘|걔)([ 을를는도야가]|$)')
POLITE = re.compile(r'(요|니다|세요|시죠|십시오)[。！？]?$')
NOUN_OK = re.compile(r'(처음|마음|다음|사람|이름|보물|얼음|믿음|웃음|죽음|울음|그림)[。！？]?$')


def sources():
    """(label, jp, ko) triples from everything that ships."""
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, 'translation', 'batch*.tsv')),
                    key=lambda x: int(re.search(r'batch(\d+)', x).group(1))):
        for r in csv.reader(open(p, encoding='utf-8'), delimiter='\t'):
            if len(r) >= 2 and r[0].strip() and r[1].strip() and r[0].strip() != 'jp':
                out.append((os.path.basename(p), r[0], r[1]))
    for p in sorted(glob.glob(os.path.join(ROOT, 'survey', 'common', '*.tsv'))):
        rows = list(csv.reader(open(p, encoding='utf-8'), delimiter='\t'))
        if not rows or 'ko' not in rows[0] or 'jp' not in rows[0]:
            continue
        ji, ki = rows[0].index('jp'), rows[0].index('ko')
        for r in rows[1:]:
            if len(r) > ki and r[ki].strip():
                out.append((os.path.basename(p), r[ji], r[ki].strip()))
    return out


CHECKS = {
    'A': ('일본어 잔존 (한국어 칸에 가나·한자)',
          lambda jp, ko: bool(KANA.search(ko))),
    'B': ('대사인데 ~됨/~함/~음 (보고체, 메뉴 전용)',
          lambda jp, ko: bool(NOUN_FINAL.search(ko)) and not NOUN_OK.search(ko)
                         and len(re.sub(r'[。！？～・ ]', '', ko)) > 3
                         and jp.strip().endswith(('。', '！', '？'))),
    'C': ('한 줄에 반말 호칭 + 존댓말 종결',
          lambda jp, ko: bool(BANMAL.search(ko)) and bool(POLITE.search(ko))),
    'D': ('번역이 원문과 동일 (사실상 미번역)',
          lambda jp, ko: jp.strip() == ko.strip()),
    'E': ('띄어쓰기 오류 (중복 공백 / 부호 앞 공백)',
          lambda jp, ko: '  ' in ko or re.search(r' [。、！？）」]', ko) is not None),
    'F': ('원문에 없는 ・ (대개 와/과가 빠진 자리)',
          lambda jp, ko: '・' in ko and '・' not in jp and '…' not in jp),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--show', type=int, default=8)
    ap.add_argument('--only', default='')
    a = ap.parse_args()
    keys = [k.strip().upper() for k in a.only.split(',') if k.strip()] or list(CHECKS)

    data = sources()
    print(f'# 검사 대상 {len(data):,}줄 '
          f'({len({d[0] for d in data})}개 파일)\n')
    for k in keys:
        label, fn = CHECKS[k]
        hits = [(src, jp, ko) for src, jp, ko in data if fn(jp, ko)]
        print(f'[{k}] {label}: {len(hits):,}건')
        for src, jp, ko in hits[:a.show]:
            print(f'      {src}  {jp}  ->  {ko}')
        print()


if __name__ == '__main__':
    main()
