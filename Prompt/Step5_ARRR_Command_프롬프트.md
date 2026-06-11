# Step5 ARRR Command · PRD · Refactor Smell 프롬프트

## 역할 설정

```
@c:\DEV\UnitConverter_05\ Unit Converter ARRR Command 체계를 사용할거야.
Rule: .cursorrules
FR SSOT: docs/PRD.md
Test ID: tests/manifest.json
전체 TDD: @unit-converter-tdd
```

---

## ARRR 파이프라인 (요약)

| 단계 | Command | 선언 예 |
|------|---------|---------|
| Ask ③ | `/red-test-plan` | `Phase: red \| Layer: entity \| Track: Logic` |
| Ask ④ | `/red-skeleton` | 동일 |
| RED 본문 | `/tdd-red` | `TDD Phase: red \| Test ID: VAL-01 — RED` |
| Respond GREEN | `/green-minimal` | `Phase: green \| Layer: entity \| Track: Logic` |
| Golden | `/golden-master` | `Phase: green \| Layer: entity \| Track: Logic` |
| Refine ⑦ | `/refactor-smell` | `Phase: refactor \| Scope: src/ tests/ \| Track: Logic+UI` |
| Refine 실행 | `/refactor-safe` | (미생성 — P0 1개·Budget 준수) |

---

## Ask — RED 설계·스켈레톤

### `/red-test-plan`

- **출력만** — C2C 4블록, tests/src 파일 생성 금지
- FR 인용: `docs/PRD.md` (예: `FR-VAL-01`)
- 완료: `/red-skeleton 으로 넘길 준비됐다`

### `/red-skeleton`

- `tests/`에 **pytest.fail** AAA만
- Then: `pytest.fail("RED: {Test ID} — …")` 한 줄
- assert·skip·xfail·src 수정 금지

### `/tdd-red`

- assert 본문 → **FAIL**(AssertionError)
- `UnitConverter.py` 수정 금지

---

## Respond — GREEN · Golden

### `/green-minimal`

1. RED 재확인 → src/`UnitConverter.py` 최소 구현
2. `pytest.fail` 제거 → assert 교체
3. `pytest -k "<Test ID>" -v` → PASS
4. 매직넘버 → `constants.py` SSOT · ECB: entity→boundary import 금지

```bash
pytest -k "VAL-01" -v
pytest tests/test_converter.py -v
pytest -m p0 -v --maxfail=3
```

### `/golden-master`

**전제:** 대상 Test ID PASS

```bash
UPDATE_GOLDEN=1 pytest -k "<Test ID>" -v   # 기준 생성
pytest -k "<Test ID>" -v                   # matched
```

- `tests/_approval.py` · `tests/golden/{id}.approved.txt`
- golden 수동 편집 우회 금지

---

## Refine — 스멜 탐지

### `/refactor-smell`

**게이트 (FAIL 시 중단):**

```bash
python -m pytest tests/ -v
```

**스멜 유형:** Long Method · Duplicated Code · Mysterious Name · Magic Number · ECB 위반 · Feature Envy

**Change Budget:** 파일≤3 · 클래스≤1 · 메서드≤3

**출력:** 스멜 표(P0/P1/P2) + `/refactor-safe` 후보 1~3개

**다음:** P0 **1개만** 골라 `/refactor-safe`

### Step5 탐지 결과 (스냅샷)

| # | P | 후보 |
|---|-----|------|
| 1 | P0 | Magic Number → `constants.py` |
| 2 | P1 | `main()` 메서드 분리 |
| 3 | P1 | `Invalid format` 중복 제거 |

---

## P0 Test ID (manifest)

| ID | Given | Then |
|----|-------|------|
| VAL-01 | `meter:-1` | 음수 거부 |
| VAL-02 | `meter` / `abc` / `meter:` / `:2.5` | Invalid format |
| VAL-03 | `metre:2.5` | Unknown unit |
| CONV-01 | `meter:2.5` | 3줄 출력 |
| CONV-02 | `feet:10` | meter 역변환 |
| CONV-03 | `meter:2.5` | feet ≈ 8.2 (±0.1) |

---

## 금지 (공통)

- RED 없이 GREEN · assert 완화 · skip/xfail
- `/refactor-smell`에서 코드·commit 수정
- E001~E005 emit (P0)
- `git commit` / `push` — 사용자 명시 요청 시만

---

## 요청 예시

```
/red-test-plan
/red-skeleton
/tdd-red VAL-01
/green-minimal VAL-01
/golden-master CONV-03
/refactor-smell
/refactor-safe 후보 #1 Magic Number
```

---

## Test Loop

```bash
pytest -m p0 -v --maxfail=3
python -m pytest tests/ -v
```

보고: passed / failed / skipped + 변경 파일 목록
