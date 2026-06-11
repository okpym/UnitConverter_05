# Step4 TDD RED·GREEN 프롬프트

## 역할 설정

```
@c:\DEV\UnitConverter_05\ Unit Converter P0 TDD를 진행할거야.
Rule: .cursorrules
Test ID: tests/manifest.json
RED만: /tdd-red
전체 사이클: @unit-converter-tdd
```

---

## RED — 실패 테스트 먼저

### Command

```
/tdd-red VAL-01
/tdd-red VAL-02
/tdd-red ALL
```

### 필수 선언 (응답 첫 줄)

```
TDD Phase: red | Test ID: VAL-01 — RED
```

### 절차

1. `README.md`, `Report/Step3_워크북.md` — P0·하지 않을 것 확인
2. `tests/manifest.json` Given/Then 확인
3. `tests/test_converter.py`에 AAA 실패 테스트 작성
4. skeleton `skip` 제거 = Given/Then과 동시
5. `pytest -k "<Test ID>" -v` → **FAIL** 확인

### 금지

- `UnitConverter.py` 및 프로덕션 코드 수정
- assert 완화, `skip`/`xfail`, GREEN 선행

### RED 보고 템플릿

```markdown
## RED 보고
- TDD Phase: red | Test ID: VAL-01 — RED
- pytest: `pytest -k VAL-01 -v` → N passed, M failed, K skipped
- FAIL: test_… — …
- 변경: tests/ 만
```

---

## GREEN — 최소 구현

### 요청 예시

```
VAL-01 GREEN 해줘
GREEN 해줘
```

### 필수 선언 (응답 첫 줄)

```
TDD Phase: green | Test ID: VAL-01 — GREEN
```

### 절차

1. `UnitConverter.py` **최소** 수정
2. `pytest -k "<Test ID>" -v` → **PASS**
3. `pytest -m p0 -v` 회귀 확인
4. GREEN 보고

### 금지

- RED 없이 프로덕션 수정
- 한 번에 여러 Test ID GREEN (규칙상 Test ID 단위)

---

## P0 Test ID 우선 순서

| 순서 | ID | Given | Then |
|------|-----|-------|------|
| 1 | VAL-01 | `meter:-1` | 음수 거부 |
| 2 | VAL-02 | `meter` / `abc` / `meter:` / `:2.5` | Invalid format |
| 3 | VAL-03 | `metre:2.5` | Unknown unit |
| 4 | CONV-01 | `meter:2.5` | meter/feet/yard 3줄 |
| 5 | CONV-02 | `feet:10` | meter 역변환 |
| 6 | CONV-03 | `meter:2.5` | feet ≈ 8.2 (±0.1) |

---

## Test Loop (Phase 종료 시)

```bash
pytest -m p0 -v --maxfail=3
```

보고: passed / failed / skipped + 변경 파일 목록

---

## REFACTOR (다음 Phase)

```
TDD Phase: refactor | Test ID: … — REFACTOR
```

- SRP/OCP 정리 — 동작 불변
- `pytest -m p0 -v` → 실패 0
