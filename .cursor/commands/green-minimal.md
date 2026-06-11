# GREEN Minimal — 최소 구현 (Respond)

**ARRR R단계 (Respond = GREEN ⑤)** 만 수행한다.  
직전 RED 묶음 **1개**에 대해 `src/` **최소 구현**으로 테스트를 **PASS**시킨다.  
**1커밋 = 1 RED 묶음** 원칙 — `git commit` / `push`는 **사용자 명시 요청 시만**.

| 연결 | 파일 |
|------|------|
| Rule | `.cursorrules` |
| SSOT (FR) | `docs/PRD.md` |
| Test ID | `tests/manifest.json` |
| RED (앞단) | `/red-test-plan` → `/red-skeleton` → `/tdd-red` |
| Skill | `@unit-converter-tdd` |
| 상수 SSOT | `entity/constants.py` |
| Refactor (다음) | `/refactor-smell` · `/refactor-safe` |

> **UnitConverter repo:** `UnitConverter.py` · `entity/` = `src/` 동일 취급.

---

## 동작 조건

- **추가 인자 없이** `/green-minimal` 만으로 동작 (직전 채팅·RED 묶음의 **Test ID 1개** 사용).
- 한 번에 **RED 묶음 1개**만 — parametrize id·마커 범위와 1:1 (`.cursorrules` TDD 원칙).
- **전제:** 해당 Test ID가 RED 상태 — `pytest.fail` 스켈레톤 또는 AssertionError **FAIL**.
- 변경 범위: **`UnitConverter.py` · `entity/`** (최소) + **`tests/`** (`pytest.fail` → assert 교체가 남아 있을 때만).

---

## 필수 선언 (응답 첫 줄)

```
Phase: green | Layer: entity | Track: Logic
```

| 필드 | 값 | 비고 |
|------|-----|------|
| Phase | `green` | 고정 |
| Layer | `entity` \| `boundary` | Track A: `Layer: boundary` |
| Track | `Logic` \| `UI` | P0 기본 `Logic` · `entity` |

---

## 절차

1. **RED 재확인** — `tests/manifest.json` Given/Then·직전 `/red-test-plan` 블록 2·3과 정합. `pytest -k "<Test ID>" -v` → **FAIL** (이미 PASS면 구현 존재 — 변경 최소화·보고만).
2. **`src/` 최소 구현** — 이번 Test ID의 Then만 만족하는 **가장 작은** 프로덕션 변경 (`UnitConverter.py` · `entity/`).
3. **테스트 완성** — `pytest.fail`이 남아 있으면 제거하고 Given/When Act + Then **assert** 본문으로 교체 (`/tdd-red` 미실행 시 여기서 수행).
4. **PASS 확인** — 아래 pytest 명령으로 대상 Test ID **PASS**.
5. **회귀 게이트** — P0 전체 실행; **실패 시 즉시 수정** 후 재실행.
6. **GREEN 보고** (아래 템플릿).

---

## 구현 규칙 (필수)

| 항목 | 규칙 |
|------|------|
| **최소 구현** | Then 1개 충족에 필요한 분기·함수만 추가·수정 |
| **매직넘버·하드코딩** | **금지** — 변환 비율·임계값은 `entity/constants.py` **SSOT** |
| **E001~E005** | `raise` · `return` · stdout emit **금지** (P0 범위 밖) |
| **ECB — entity** | `boundary` · `control` 레이어 **import 금지** |
| **에러 표현** | 기존 패턴 유지 — `print` + `return None` 등 manifest·README 관찰 가능 형태 |
| **Domain Mock** | Logic Track — 변환 비율·단위 테이블 Mock **금지** |
| **Harness** | `monkeypatch` · `capsys` 등 테스트 측만 허용 |

### VAL-01 예시 (최소 구현 방향)

```python
# entity/constants.py — 비율은 여기만 (이미 있으면 재사용)
# METER_TO_FEET, METER_TO_YARD ...

# UnitConverter.py — _parse_unit_value() 내
if value < 0:
    print(f"Negative value: {value_str}")
    return None
```

---

## pytest · 보고 (Phase 종료 필수)

**단일 Test ID (대상 RED 묶음):**

```bash
pytest -k "<Test ID>" -v
```

**파일 전체 (회귀·동일 파일 내 다른 ID):**

```bash
pytest tests/test_converter.py -v
```

**P0 회귀 (권장 · Skill Test Loop):**

```bash
pytest -m p0 -v --maxfail=3
```

**기대:** 대상 Test ID **PASS**. 회귀 **failed 0**.

```markdown
## GREEN 보고
- Phase: green | Layer: entity | Track: Logic | Test ID: VAL-01
- pytest: `pytest -k VAL-01 -v` → N passed, 0 failed, 0 skipped
- PASS: test_VAL_01_negative_input_rejected[VAL-01]
- 변경: UnitConverter.py (_parse_unit_value 음수 검증)
- 회귀: `pytest -m p0 -v --maxfail=3` → 10 passed, 0 failed, 0 skipped
```

| 보고 항목 | 내용 |
|-----------|------|
| PASS Test ID | manifest ID 1개 (parametrize id 포함) |
| 변경 파일 | `UnitConverter.py` · `entity/` · `tests/` 경로 |
| 회귀 | passed / failed / skipped — **failed > 0 이면 즉시 수정** |

---

## 금지

| 금지 | 이유 |
|------|------|
| **이번 RED 묶음 외 Test ID** 동시 해결 | 1커밋 = 1 RED 묶음 |
| **REFACTOR** (SRP 분리·rename·구조 정리) | `/refactor-safe` 담당 — GREEN은 동작만 |
| **assert 완화** · 삭제 · `skip` · `xfail` | RED 우회 |
| **E001~E005** `raise` / `return` / emit | P0·ECB 범위 밖 |
| **entity → boundary/control import** | ECB 위반 |
| **매직넘버** 인라인 (3.28084 등) | `entity/constants.py` SSOT 위반 |
| **Domain Mock** (Logic Track) | `/red-test-plan` 블록 4 |
| **`git commit` / `push`** (묵시) | 사용자 명시 요청 시만 |

---

## 커밋 가이드 (사용자 요청 시)

- 메시지: **한국어**, Test ID·FR 한 줄 요약.
- 범위: 이번 RED 묶음 관련 `tests/` + `src/` 변경만 스테이징.
- 예: `GREEN VAL-01: 음수 입력 거부 최소 구현`

---

## 완료

대상 Test ID PASS·P0 회귀 확인 후:

**다음:** 동일 Test ID Golden이 있으면 Golden 승인 테스트 확인 → `/refactor-smell` (선택) · 다음 Test ID RED.

**ARRR 파이프라인:** `/red-test-plan` → `/red-skeleton` → `/tdd-red` → **`/green-minimal`** → `/refactor-smell` → `/refactor-safe`
