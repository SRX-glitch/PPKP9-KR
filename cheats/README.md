# 에뮬레이터 치트 (Action Replay) — ⚠ v213 빌드 기준

> 이 문서는 세션44(v213 외부 테스트용)에 쓴 것이다. 패치 배포는 이제 GitHub Releases `v0.1`
> (`release/PPKP9-KR-0.1/`)로 하며, 아래 v213 xdelta 절차는 **더 이상 유효하지 않다**.
> 치트 파일도 v213의 힙 델타(+0x72000) 기준이라 **v0.1(grow 0x75000)에서는 주소가 어긋난다**
> — 재생성 전까지 참고용으로만 둔다(KNOWN_ISSUES.md D 항목).

## 준비물

- 원본 롬: `Power Pro Kun Pocket 9 (Japan).nds` — SHA1 `9d37ea0b…`
- 패치: `PPKP9_kr_v213_ops.xdelta` (이 폴더)
- xdelta3: Windows는 https://github.com/jmacd/xdelta/releases 또는
  `winget install xdelta3` / Linux·WSL은 `apt install xdelta3`

## 적용

```bash
xdelta3 -d -s "Power Pro Kun Pocket 9 (Japan).nds" PPKP9_kr_v213_ops.xdelta PPKP9_kr_v213_ops.nds
```

결과 SHA1이 `cd567f73095957fc4185e2e2fe5b05757a78457b` 이면 성공.

## 치트 (DeSmuME)

`PPKP9_KR_cheats_v213.txt` 를 연다 →
DeSmuME 메뉴 **Emulation → Cheats → List → Add → Action Replay 탭**에
원하는 코드 블록을 통째로 붙여넣고 이름을 달아 저장한다.

- 이 치트는 **v211~v213 빌드 전용**이다(힙이 +0x72000 밀린 것을 반영).
  원본 롬이나 다른 빌드에는 쓰지 말 것.
- `[검증]` 표시는 실기 메모리에서 값까지 확인한 코드, `[추정]` 은 델타만 적용한 코드.
- さすらい 계열 코드가 안 먹으면 맨 앞 가드 줄(`5233CB60 0233E440`)과 맨 뒤
  `D0000000 00000000` 을 지우고, 그 모드 안에서만 치트를 켜라.

## 테스트 중점 (세션44 → 45 인계)

1. **만세(バンザイ) 실행** — 치트로 게이지 MAX 후 실행. 애니메이션 없이 멈추면
   그 직전 세이브(.dsv)를 보존해 줄 것 (⛔ 미해결 결함)
2. **게임오버 화면** — 대사창이 비고 멈추는지 (⛔ 미해결 결함)
3. 훈련·배회 커맨드가 한국어인지 (「연습」 확인됨, 나머지 커맨드 제보 환영)
4. 아이템 입수/소모 메시지 — 아직 일본어가 정상(파일8 리전 부재, 다음 세션 과제)
