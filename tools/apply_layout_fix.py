#!/usr/bin/env python3
"""Tighten the 86 translations that spill onto an extra display line.

Replacements are given positionally against survey/layout_overflow.tsv (produced
by layout_list.py) so the Japanese keys never have to be retyped. Each candidate
is re-simulated through layout_audit.rows before anything is written; if even one
would still overflow, nothing is touched.
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from layout_audit import rows, BASE

NEW = [
    "기본적으로 인간 실격 부류니까。",
    "（・・・나쁜 징조가 아니길。）",
    "그러고 보니、무샤도 애가 있다던데",
    "대단하네、칼로 트럭을 두 쪽이라니。",
    "근육은 실제로 안 쓰니 의미 없지만",
    "（・・・왠지 불길한 예감이 드는데）",
    "그랬더니 이런 게 우수수 나오더라。",
    "역시 풀은 날로 먹으면 안 되겠어。",
    "그럼 늘 그 자리로 갖다 드릴게요。",
    "가방에 들어가는 법은 안 물어봤어。",
    "윗몸일으키기 하게 다리 좀 잡아줘。",
    "그럼 그건 쇼핑이 주목적이었어？",
    "다들 말만 그러고 몸은 안 움직이는",
    "근데 난 네가 온 걸 알고 있었어。",
    "여기서 봉사는 이런 걸 말하니까요。",
    "거기까지 말하면 오히려 질리니까、",
    "소원이 이뤄진 게 아니라 결국 자기",
    "다른 남자 손님한테도 그러고 노는",
    "메이드복인데 왜 운동부 인사야？",
    "어른이 저렇게 힘들게 걷고 있는",
    "부지런한 젊은이는 나라의 보배지。",
    "격려하는 건지 깎아내리는 건지",
    "전엔 이상한 생물이 앉아 있었지。",
    "메이드는 나이를 안 밝혀도 되는 법",
    "메이드에겐 눈물 없이 못 할 사연",
    "그때 조금이나마 전력을 내 컴퓨터에",
    "예를 들면 세계 아이들한테 매일、",
    "자、운동도 했으니 커피라도 마시러",
    "그런 이유로 저는 일하러 갈게요。",
    "그、그럼 이제 이 가게엔 나 혼자선",
    "（꼼꼼한 성격이라 끝장 볼 줄 알았",
    "어느 루트냐는 게 여러 개 있어？",
    "아니、게임 속에서 아무리 사랑해도、",
    "그래서 당분간 나도 여기서 느긋하게",
    "인생 설계도 못 하는 어른은 싫어",
    "그러려면 알바 열심히 해서 돈 모아",
    "무슨 말도 안 되는 소리야。",
    "그러니까 포기할 수밖에 없다잖아。",
    "이 세계에선 네가 연상일지 모르지만",
    "뭐、그 사람이 여기 온 뒤부터니까。",
    "（그 분위기를 완전히 망치는 사람이",
    "네～、잡지 집계로 약 １２만 장、",
    "철물이나 전동공구 수리는 내 전문。",
    "자、이 동네에 무슨 일이 일어날까。",
    "툭하면 폭력에 호소하려 든다니까。",
    "너와 인연이 있는 개인 모양이다。",
    "개한테 원한 살 짓은 없는데・・・",
    "그 애가 여기 온 게 3년 전이니까",
    "파일럿의 개인적인 보물일지도 몰라。",
    "상점가 없애기、이거면 한 방이야。",
    "연상한테 「짱」을 붙여 부르냐？",
    "오늘은 꼭 보물을 손에 넣겠습죠。",
    "상점가가 점점 기고만장해지네요。",
    "그건 상점가 사람들 전부의 합의야？",
    "（・・・이제 와서 아니라곤 못 해。",
    "그러니까、조명 담당한테 부탁해야지。",
    "어쩔 수 없지、나중에 수건이랑 셔츠",
    "그리고 이것저것 챙겨주고・・・",
    "딱히 내 걸로 삼고 싶은 건 아냐。",
    "이제 와서 다른 삶을 살 수 있나。",
    "메이드 경력이 １년이랬잖아？",
    "요즘 안 온다 싶더니 집 나서는 게",
    "그 말 들으면 왠지 애완동물이 된",
    "그래서 가게를 얼마나 더 돌 거야？",
    "그걸 생각해서 행동에 옮길 수 있는",
    "아니、그러니까 이대로 하면 얼굴이。",
    "예를 들면 이동을 편하게 하려 차나",
    "겉모습부터 수상한데 새삼 태도가",
    "뭐、남자라면 한 번은 최강을 노리는",
    "역시 말로 안 전해지는 것도 있다고",
    "역시 자유인한텐 상관없는 날이니까、",
    "메이드에겐 넘치는 지성이 배어나오는",
    "아、그래서 지난번 답례를 하려고。",
    "방금 그건 관객이었으면 박수쳤어。",
    "・・・그 목걸이는 누구도 끊을 수는",
    "아니、그러니까 그 이전의 문제라고。",
    "박사님 말대로 동물 책을 읽었어。",
    "어른이 애한테 녀석 취급인가・・・。",
    "（그러고 보니 전에 이런 일 있었지",
    "먹이라니・・・난 애완동물 취급인가。",
    "아침부터 밤까지 계속 책이라니・・・",
    "그냥 아침에 마시러 오는 것뿐이잖아",
    "그런 이유로 이런 귀여운 메이드한테",
    "둘 다・・・쳐줬으면 하는 곡 있어？",
    "온라인 게임에선 레벨이 최대치라",
    "그것도 있겠지만 아직 지은 지",
]

src = open(f"{BASE}/survey/layout_overflow.tsv", encoding="utf-8").read().splitlines()[1:]
src = [ln for ln in src if ln.strip()]
assert len(src) == len(NEW), f"{len(src)} overflow rows but {len(NEW)} replacements"

# per-batch {jp: (old_ko, new_ko)}
plan, bad = {}, []
for ln, new in zip(src, NEW):
    batch, occ, rj, rk, klen, budget, jp, old = ln.split("\t")
    if rows(new, korean=True) > int(rj):
        bad.append((jp, new, len(new), budget))
    plan.setdefault(batch, {})[jp] = (old, new)

if bad:
    for jp, new, n, budget in bad:
        print(f"STILL OVER ({n} > {budget}): {new}")
    sys.exit(f"\n{len(bad)} replacement(s) still overflow -- nothing written")

touched = 0
for batch, repl in plan.items():
    path = f"{BASE}/translation/{batch}.tsv"
    lines = open(path, encoding="utf-8").read().splitlines()
    hits = 0
    for i, ln in enumerate(lines):
        if "\t" not in ln:
            continue
        parts = ln.split("\t")
        jp = parts[0].strip()
        if jp in repl and parts[1].strip() == repl[jp][0]:
            parts[1] = repl[jp][1]
            lines[i] = "\t".join(parts)
            hits += 1
    assert hits == len(repl), f"{batch}: matched {hits} of {len(repl)}"
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    touched += hits
    print(f"{batch}: {hits} lines tightened")

print(f"\n{touched} lines rewritten")
