# Step5 ARRR Command · PRD · Refactor Smell 보고서

- **프로젝트:** Unit Converter (`UnitConverter_05`)
- **일자:** 2026-06-11
- **세션 범위:** ARRR A/R 파이프라인 Command · FR SSOT(`docs/PRD.md`) · Refactor Smell 탐지
- **전제:** Step4 P0 RED→GREEN 완료 (`pytest -m p0` 9 passed)

---

## 1) 세션 목표

Step4에서 P0 테스트·GREEN이 고정된 뒤, **AI 거버넌스를 ARRR 단계별 Command로 확장**한다.

| 목표 | 산출 |
|------|------|
| FR 단일 출처 | `docs/PRD.md` (FR-VAL/CONV-* ↔ Test ID) |
| Ask (RED ③④) | `/red-test-plan`, `/red-skeleton` |
| Respond (GREEN) | `/green-minimal`, `/golden-master` |
| Refine (⑦) | `/refactor-smell` (탐지만) |
| Rule·README 연동 | `.cursorrules`, README Command·문서 목록 |

---

## 2) Mom Test 연결

| 증거 (Step3) | Step5 대응 |
|-------------|------------|
| 요구 해석 4시간 — Test ID 분해 | **PRD** FR-VAL/CONV-* + manifest 추적 매트릭스 |
| `feet:-3` 캡처만 | `/red-test-plan` C2C Rule1 FR 인용 → `/red-skeleton` → `/tdd-red` 파이프라인 |
| 테스트·포맷 불안 원복 | `/refactor-smell` 전제: **전체 pytest PASS** 게이트 |
| OCP/SRP 미시도 | `/refactor-smell` P0 후보: Magic Number → constants SSOT |

---

## 3) ARRR ↔ Command 매핑

| ARRR | Phase | Command | 역할 |
|------|-------|---------|------|
| **A — Ask** | RED ③ | `/red-test-plan` | C2C 설계표·테스트 플랜 (파일 생성 없음) |
| **A — Ask** | RED ④ | `/red-skeleton` | `pytest.fail` 스켈레톤만 (`tests/`) |
| **A — Ask** | RED 본문 | `/tdd-red` | AAA assert FAIL (Step4·Skill) |
| **R — Respond** | GREEN | `/green-minimal` | RED 1묶음 최소 구현 · 1커밋=1묶음 |
| **R — Respond** | Golden | `/golden-master` | Approval Test · `UPDATE_GOLDEN` |
| **R — Refine** | ⑦ | `/refactor-smell` | 스멜 탐지만 · 수정·commit 금지 |
| **R — Refine** | (다음) | `/refactor-safe` | P0 1개·Change Budget 내 실행 (미생성) |

```
/red-test-plan → /red-skeleton → /tdd-red → /green-minimal → /golden-master
                                                      ↓
                                            /refactor-smell → /refactor-safe
```

---

## 4) 신규·갱신 산출물

### 4.1 Command (`.cursor/commands/`)

| 파일 | Phase | 한 줄 역할 |
|------|-------|-----------|
| `red-test-plan.md` | red · Ask ③ | C2C 4블록 · ECB·Mock 점검 |
| `red-skeleton.md` | red · Ask ④ | `pytest.fail` AAA 스켈레톤 |
| `green-minimal.md` | green · Respond | src 최소 구현 · constants SSOT |
| `golden-master.md` | green · Golden | `_approval.py` · `golden/*.approved.txt` |
| `refactor-smell.md` | refactor · Refine ⑦ | 스멜 표 · refactor-safe 후보 |
| `tdd-red.md` | red | (Step3) assert FAIL 본문 |

### 4.2 FR SSOT

| 파일 | 내용 |
|------|------|
| `docs/PRD.md` | P0 FR-VAL-01~03, FR-CONV-01~03, 추적 매트릭스, ECB·TDD 정책 |
| `.cursorrules` | `docs/PRD.md` 작업 전 읽기, `/red-test-plan` 명시 |

### 4.3 README (부분 갱신)

- PRD 행·문서 목록·Command 표 (`/red-test-plan`, SSOT)
- **미갱신:** 진행 상태(Step4 P0 완료), `/red-skeleton` 등 신규 Command — Step6 또는 수동 갱신 권장

---

## 5) `/refactor-smell` 실행 결과 (본 세션)

**게이트:** `python -m pytest tests/ -v` → **9 passed, 0 failed**

| P | 건수 | 대표 스멜 |
|---|------|-----------|
| P0 | 2 | Magic Number — `UnitConverter.py` L27,35-36 · `test_converter.py` L139 |
| P1 | 4 | Long Method `main()` · Duplicated `Invalid format` · `conversion_lines` · Act 보일러플레이트 |
| P2 | 2 | Mysterious Name · Feature Envy (I/O+로직 혼재) |

### refactor-safe 후보 (Change Budget: 파일≤3 · 클래스≤1 · 메서드≤3)

| # | P | 대상 | Budget |
|---|-----|------|--------|
| **1** | **P0** | Magic Number → `constants.py` SSOT | ✅ 파일2 |
| 2 | P1 | `main()` → `parse_input` + `to_meter` + 출력 | ✅ 파일1·메서드3 |
| 3 | P1 | `Invalid format` 중복 제거 | ✅ 파일1·메서드1 |

**권장 다음:** P0 후보 #1 → `/refactor-safe` (Command 미생성 시 Skill·수동 REFACTOR)

---

## 6) pytest 스냅샷 (저장 시점)

```bash
python -m pytest tests/ -v
# → 9 passed, 0 failed, 0 skipped
```

코드 변경 없음 — Step5는 **Command·PRD·문서** 중심; 프로덕션·테스트 본문은 Step4 상태 유지.

---

## 7) 성공 기준 (Step5 자체)

| ID | 기준 | 달성 |
|----|------|------|
| **SC5-1** | FR SSOT `docs/PRD.md` + manifest 추적 | ✅ |
| **SC5-2** | ARRR Ask/Respond/Refine Command 5종 + tdd-red | ✅ |
| **SC5-3** | `/refactor-smell` 게이트 PASS 후 스멜 표·후보 출력 | ✅ |
| **SC5-4** | Golden·refactor-safe **실행** | ⬜ Command만, 미실행 |

---

## 8) 이번 세션에서 하지 않은 것

| 항목 | 사유 |
|------|------|
| `/refactor-safe` Command·실행 | P0 Magic Number 리팩터 — 다음 세션 |
| `/golden-master` 실행 | `_approval.py`·golden 파일 미구축 |
| README 진행 상태 Step4 반영 | 문서 부분 갱신만 |
| cubit · units.json · JSON/CSV | Step3 §4 deferred |
| `git commit` | 사용자 요청 시만 (`.cursorrules`) |

---

## 9) 다음 권장

1. **`/refactor-safe`** Command 생성 → P0 #1 Magic Number → `constants.py`
2. **`/golden-master`** — CONV-03 또는 stdout Approval Test
3. **README** — P0 완료·Command 전체 표·다음 권장 문구 갱신
4. **REFACTOR** — `main()` SRP 분리 (후보 #2, Budget 준수)

---

## 참고

| 문서 | 경로 |
|------|------|
| Step3 워크북 | `Report/Step3_워크북.md` |
| Step4 RED→GREEN | `Report/Step4_TDD_RED_보고서.md` |
| PRD | `docs/PRD.md` |
| Prompt (재현) | `Prompt/Step5_ARRR_Command_프롬프트.md` |
| TDD Skill | `.cursor/skills/unit-converter-tdd/SKILL.md` |
