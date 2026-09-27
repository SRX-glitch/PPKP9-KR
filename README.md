# PPKP9-KR — 파워프로군 포켓 9 (NDS) 한글패치

パワプロクンポケット9 (Nintendo DS, 일본판)의 비공식 팬 번역 프로젝트.
석세스 모드 「さすらいのナイスガイ」 시나리오 대사를 중심으로 한국어를 입힌다.

**현재 배포판: v0.1** (빌드 `PPKP9_kr_v231_padfix3`, 2026-09-15)
→ [Releases](https://github.com/SRX-glitch/PPKP9-KR/releases) 의 xdelta 패치를 원본 덤프에 적용한다.
아직 손볼 곳이 많은 초기 판이다. 남은 문제는 [KNOWN_ISSUES.md](KNOWN_ISSUES.md) 참조.

## 배포 원칙
- **패치(xdelta)만 배포**한다. ROM·빌드 결과물(`builds/`)은 저장소에 올리지 않는다.
- 적용 대상은 SHA-1 `9d37ea0bbd71bda9db9bd641460061b0ce9e3aeb` 덤프 하나뿐이다.
- 릴리스마다 패치를 원본에 역적용해 빌드와 SHA-1이 같은지 검증한다(`tools/make_release.py`).

## 저장소 구성
| 경로 | 내용 |
|---|---|
| `tools/` | 추출·번역 삽입·폰트 팩·훅·검증 게이트·릴리스 도구 (`build_kr.py`가 진입점) |
| `translation/` | 번역 배치 TSV(`batchNNN.tsv`)와 오버라이드 |
| `survey/common/`, `survey/font/`, `survey/ov28/opcode_lengths.json` | 빌드가 읽는 워크리스트·폰트 배치·오프코드 폭 표 (나머지 `survey/`는 ROM에서 재생성 가능한 대용량 덤프라 미추적) |
| `release/` | 배포판 패치 `PPKP9-KR-0.1/` (폐기된 0.9.x는 `_archive/`) |
| `cheats/` | 에뮬레이터용 Action Replay 치트 (⚠ v213 기준, v0.1과 주소 불일치 — KNOWN_ISSUES D) |
| `handoff/` | 외부 번역 인수인계 패키지(샤드·정책·QA 기록, 2026-07~08) |
| `KNOWN_ISSUES.md` | 미해결 문제 정리 (v0.1 기준) |
| `RESUME.md` | 세션별 작업 일지·다음 세션 인계 (가장 위가 최신) |
| `GAME_REFERENCE.md`, `SURVEY.md`, `RE_PLAN.md` | 게임 구조·조사 기록·역분석 계획 |

## 빌드 (재현)
원본 ROM을 `rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds`에 두고:

```
PYTHONIOENCODING=utf-8 PPKP9_ROMOUT=builds/PPKP9_kr.nds \
PPKP9_CHOICE_REDIRECT=1 PPKP9_MEASURE_HOOK=1 PPKP9_REGION_CAP=0x74000 \
PPKP9_BATCH_SITES=1 PPKP9_BATCH_EXCLUDE=25,30,18,20 \
PPKP9_FILE8=1 PPKP9_FILE8_INPLACE=1 \
PPKP9_EXTRA_LATE=18,20,30 PPKP9_TAIL_REGION=30,20,18,8 python tools/build_kr.py
```
약 3~5분. 게이트(choice·opcode·리전·escape·f8 포인터)가 하나라도 red면 출하하지 않는다.

## 라이선스 / 면책
비영리 팬 번역이며 코나미와 무관하다. 패치에는 원 게임 데이터가 들어 있지 않다.
