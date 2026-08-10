#!/usr/bin/env python3
"""Find lines where the original's content word was dropped or swapped for a
paraphrase -- the defect the "직역 우선" 기조 (session 34) exists to catch.

`tl_audit.py` asks "is the Korean Korean?". This asks a different question:
**"is the Korean the ORIGINAL's Korean?"** A line can be fluent, in-budget and
still have quietly replaced 「報告」 with 「알리다」 or dropped 「宇宙船」 entirely.

Method: a glossary of the corpus's most frequent kanji compounds mapped to the
Korean forms that count as a literal rendering. A line is flagged when the
Japanese has the term and the Korean has none of its accepted forms.

    python3 tools/literal_audit.py                 # counts per term
    python3 tools/literal_audit.py --term 報告     # every hit for one term
    python3 tools/literal_audit.py --show 20       # samples for every term

⚠ 예산 주의: 본편 대사(batch*.tsv)는 대부분 이미 리다이렉트라 **글자를 늘리면
리전을 먹고 다른 줄을 일본어로 되돌린다**(세션34 실측: 44줄 추가 -> 25줄 밀려남).
그러니 이 목록은 «길이가 같거나 줄어드는 교체»부터 처리한다. 늘리는 수정을 했으면
빌드 후 `left Japanese` 수치를 반드시 확인할 것.
"""
import argparse, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tl_audit

# JP 한자어 -> 직역으로 인정되는 한국어 표기들(정규식 대안).
# 문맥 의존이 심한 말(自分・一緒・出来・仕方 등)은 오탐이 많아 넣지 않았다.
GLOSS = {
    '今日': '오늘', '商店街': '상점가', '本当': '정말|진짜|사실|참|참말|다며|라며|정녕',
    '練習': '연습', '野球': '야구', '人間': '인간|사람|놈|자|인류|이들|누구|아무|외부인|행성인|인', '大丈夫': '괜찮',
    '宇宙船': '우주선', '宇宙港': '우주항', '宇宙': '우주', '試合': '시합|경기',
    '貴方': '당신|그대|너|자네', '仕事': '일|업무|작업', '時間': '시간',
    '必要': '필요', '場所': '장소|곳|데|자리|위치|여기|거기|저기', '大変': '힘들|힘드|힘든|큰일|대단|고생|난리|벅차|큰|엄청',
    '名前': '이름', '変化球': '변화구', '問題': '문제|괜찮|탈|이상', '絶対': '절대|반드시|꼭|결코|분명|틀림없|확실',
    '意味': '의미|뜻|무슨 말|무슨 소리|이해|소린지|말인지', '連中': '놈들|녀석들|무리|것들|애들|자식들|녀석|놈', '部屋': '방',
    '子供': '아이|애|어릴|어린|어렸|꼬마|자식|새끼|아기', '普通': '보통|평범|평소|여느', '会長': '회장',
    '気持': '기분|마음|기색|심정|심경|맘|생각|느낌|징그럽|편하|편해|기꺼', '今回': '이번', '相手': '상대',
    '世界': '세계|세상', '情報': '정보', '心配': '걱정|염려', '先生': '선생',
    '修行': '수행|수련', '仲間': '동료|친구|일행|한패|끼워|같이|편', '今度': '이번|다음',
    '全部': '전부|다|모두|모든|온', '最後': '마지막|최후|끝', '最近': '최근|요즘',
    '惑星': '행성', '元気': '기운|건강|활기|잘|팔팔|괜찮|기력|힘|씩씩|쌩쌩', '大事': '중요|소중|큰일|귀중|아끼',
    '危険': '위험', '正義': '정의', '生活': '생활|삶|살|일상|지내', '彼女': '그녀|여친|애인|그 여자',
    '最初': '처음|최초|첫|애초|원래', '勝負': '승부', '料理': '요리', '以上': '이상|더|넘|위',
    '約束': '약속|하기로|기로 했|뻔한', '味方': '아군|편|사도|우리', '身体': '몸|신체', '用意': '준비|채비|마련',
    '協力': '협력|협조|도와|돕', '芝居': '연극|연기', '失礼': '실례|무례|떠나|떠날|가볼',
    '冗談': '농담', '関係': '관계|상관|관련|사이|무관|친밀', '攻撃': '공격', '公演': '공연',
    '会社': '회사', '大統領': '대통령', '機械': '기계', '明日': '내일',
    '当然': '당연', '理由': '이유', '残念': '아쉽|유감|안타|아깝',
    '能力': '능력', '自信': '자신', '言葉': '말|언어|인사|소리', '行動': '행동',
    '興味': '흥미|관심', '先輩': '선배', '倉庫': '창고', '調子': '상태|컨디션|가락|몸|기세|잘|어때|기고만장|들뜨|들떴|신나|그거야|그렇게',
    '破壊': '파괴|부수|부순|부술|부쉈|부숴', '迷惑': '민폐|폐|귀찮', '回復': '회복',
    '無駄': '낭비|헛|쓸데|소용없|보람|의미없|무의미|괜히', '簡単': '간단|쉽|쉬우|수월', '本気': '진심|진짜|본심',
    '息子': '아들|아드님', '毎日': '매일|날마다', '存在': '존재', '体力': '체력',
    '監督': '감독', '目的': '목적', '食事': '식사|밥', '説明': '설명',
    '学校': '학교', '勉強': '공부', '状況': '상황', '昨日': '어제',
    '配達': '배달', '失敗': '실패|실수', '感謝': '감사|고마', '武器': '무기',
    '連邦': '연방', '劇団': '극단', '主人公': '주인공', '賞金稼': '현상금|현상범|현상|사냥꾼',
    '主人様': '주인님', '嬢様': '아가씨', '頑張': '힘내|힘낸|힘낼|힘쓰|애쓰|애썼|열심|분발|노력|버텨|버티|기운',
    '手伝': '돕|도울|도우|도와|거들', '間違': '틀리|틀렸|틀림없|잘못|실수|아니|어긋|오산|착각|확실|맞', '勝手': '멋대로|맘대로|제멋',
    '報告': '보고|알리|알림', '修理': '수리|고치|고쳐', '移動': '이동|옮기|옮겨|옮겼|이사',
    '確認': '확인', '検査': '검사', '禁止': '금지', '法律': '법률|법',
    '登録': '등록', '選択': '선택|고르|골라', '契約': '계약', '報酬': '보수|보상',
    '依頼': '의뢰|부탁', '調査': '조사', '発見': '발견', '到着': '도착',
    '出発': '출발', '準備': '준비', '完成': '완성', '製造': '제조',
    '販売': '판매|팔', '購入': '구입|사', '価格': '가격|값', '値段': '값|가격|비싸|비싼|싸',
}
COMPILED = {k: re.compile(v) for k, v in GLOSS.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--show', type=int, default=0, help='samples per term')
    ap.add_argument('--term', default='', help='dump every hit for one term')
    ap.add_argument('--min', type=int, default=3, help='hide terms below this count')
    a = ap.parse_args()

    data = tl_audit.sources()
    hits = {k: [] for k in GLOSS}
    for src, jp, ko in data:
        for term, rx in COMPILED.items():
            if term in jp and not rx.search(ko):
                hits[term].append((src, jp, ko))

    if a.term:
        for src, jp, ko in hits.get(a.term, []):
            print(f'  {src}\n    {jp}\n    {ko}')
        print(f'\n{a.term}: {len(hits.get(a.term, []))}건')
        return

    ranked = sorted(((len(v), k) for k, v in hits.items()), reverse=True)
    total = sum(n for n, _ in ranked)
    print(f'# {len(data):,}줄 중 «원문 한자어가 한국어에 없는» 줄: 연 {total:,}건\n')
    for n, k in ranked:
        if n < a.min:
            continue
        print(f'  {k:<5} {n:>4}건  (기대 표기: {GLOSS[k]})')
        for src, jp, ko in hits[k][:a.show]:
            print(f'        {jp}  ->  {ko}')


if __name__ == '__main__':
    main()
