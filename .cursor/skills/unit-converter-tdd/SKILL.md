---
name: unit-converter-tdd
description: >-
  Runs TDD for Unit Converter (UnitConverter_05). Use for RED, GREEN, REFACTOR,
  CONV-*, VAL-*, tests/manifest.json, or pytest under tests/. For RED-only use
  Command /tdd-red; this skill covers the full cycle and Test Loop reporting.
---

# Unit Converter TDD

| 연결 | 파일 |
|------|------|
| Rule | `.cursorrules` |
| Command (RED만) | `/tdd-red` |
| Test ID | `tests/manifest.json` |
| Mom Test 근거 | `Report/Step3_워크북.md` |

> **RED만:** `/tdd-red`. **GREEN·REFACTOR·전체 사이클:** 이 Skill.

---

## Mom Test → TDD 매핑

| 증거 | TDD 대응 |
|------|----------|
| 요구 해석 4시간 | manifest Test ID로 작업 분해 |
| `feet:-3` 캡처만 | VAL-01 RED → GREEN |
| 테스트·포맷 불안 원복 | Phase마다 pytest 게이트 |

---

## RED (6단계)

1. 선언: `TDD Phase: red | Test ID: … — RED`
2. manifest Given/Then 확인.
3. `tests/`에 실패 테스트 (AAA).
4. `pytest -k "<id>" -v` → **FAIL**.
5. RED 보고 (Command 템플릿).
6. 프로덕션 코드 **미수정**.

## GREEN (5단계)

1. 선언: `TDD Phase: green | Test ID: … — GREEN`
2. `UnitConverter.py` **최소** 수정.
3. `pytest -k "<id>" -v` → **PASS**.
4. 다른 P0 테스트 회귀 확인.
5. GREEN 보고.

## REFACTOR (4단계)

1. 선언: `TDD Phase: refactor | Test ID: … — REFACTOR`
2. SRP/OCP 정리 (README 품질 요구) — 동작 불변.
3. `pytest -m p0 -v` → 실패 0.
4. REFACTOR 보고.

---

## Test Loop (필수)

매 Phase 종료 시:

```bash
pytest -m p0 -v --maxfail=3
```

보고: passed / failed / skipped + 변경 파일 목록.

---

## P0 Test ID (우선 순서)

1. `VAL-01` — 음수 거부 (`meter:-1`)
2. `VAL-02` — 형식 오류 (`meter` / `abc`)
3. `VAL-03` — 미등록 단위 (`metre:2.5`)
4. `CONV-01` — `meter:2.5` 기본 변환
5. `CONV-02` — `feet:10` 역변환
6. `CONV-03` — Golden `2.5 m → 8.2 ft` (README 예시, 허용 오차)

---

## 금지 (Step3 워크북 §4)

- cubit 동적 등록, units.json, JSON/CSV 포맷 — 별도 Phase
- 한 번에 여러 Test ID GREEN
- RED 없는 프로덕션 수정
