# Step6 Refactor Smell · Safe Refactor 보고서

- **프로젝트:** Unit Converter (`UnitConverter_05`)
- **일자:** 2026-06-11
- **세션 범위:** `/refactor-smell` 탐지 → `/refactor-safe` 스멜 1개씩 실행
- **브랜치:** `refactoring`
- **전제:** P0 GREEN 완료 · Golden VAL-01 · `pytest` 전부 PASS

---

## 1) 파이프라인

```
/refactor-smell (⑦ 탐지, 수정 금지)
    → /refactor-safe (⑧ 스멜 1개, Budget 준수)
    → pytest tests/ -v + golden matched
    → (반복)
```

| Command | 파일 | 역할 |
|---------|------|------|
| `/refactor-smell` | `.cursor/commands/refactor-smell.md` | 스멜 표 · safe 후보 1~3개 |
| `/refactor-safe` | `.cursor/commands/refactor-safe.md` | 스멜 1개 Safe Refactor |

---

## 2) 스멜 유형 SSOT (요약)

| 유형 | P0/P1/P2 | 탐지 힌트 |
|------|----------|-----------|
| Magic Number | P0 | 변환 상수 리터럴 · prod/test 이중 정의 |
| ECB 위반 | P0 | entity→boundary import · E001~E005 |
| Long Method | P1 | `main()` 다책임 |
| Duplicated Code | P1 | Invalid format·Act·conversion_lines 중복 |
| Mysterious Name | P2 | `in_meters` 등 의미 모호 |
| Feature Envy | P2 | I/O+로직 혼재 (레이어 미분리) |

**Change Budget (1회):** 파일≤3 · 클래스≤1 · 메서드≤3

---

## 3) 초기 스멜 표 (refactoring 브랜치 · 1차 `/refactor-smell`)

**게이트:** `python -m pytest tests/ -v` → 10 passed (VAL-01 golden 포함)

| P | 유형 | 위치 | 요약 | Budget |
|---|------|------|------|--------|
| P0 | Magic Number | `UnitConverter.py` L23-32 | `3.28084`/`1.09361` 리터럴 | ✅ 파일3 |
| P0 | Magic Number | `tests/test_converter.py` L17-18 | prod와 상수 이중 정의 | ✅ (#1과 동시) |
| P1 | Long Method | `UnitConverter.py` `main()` | 파싱·검증·변환·출력 4책임 | ✅ 파일1·메서드3 |
| P1 | Duplicated Code | `UnitConverter.py` L4-6·L10-12 | `Invalid format` 2회 | ✅ (#2와 동시) |
| P1 | Duplicated Code | `tests/test_converter.py` VAL-01 | `_run_main` Act 2회 | ✅ 파일1 |
| P2 | Feature Envy | `UnitConverter.py` | CLI+도메인 혼재 | ⚠️ Budget 초과 |

### refactor-safe 후보 (1차)

| # | P | 대상 | 상태 |
|---|-----|------|------|
| **1** | P0 | Magic Number → `entity/constants.py` | ✅ **완료** |
| **2** | P1 | `main()` → helper 3개 extract | ✅ **완료** |
| 3 | P1 | VAL-01 Act 중복 → fixture | ⬜ 미착수 |

---

## 4) Safe Refactor 실행 이력

### #1 P0 — Magic Number → constants SSOT

| 항목 | 내용 |
|------|------|
| **커밋** | `fde7464` (refactoring 브랜치) |
| **변경** | `entity/constants.py` — `METER_TO_FEET`, `METER_TO_YARD` |
| | `UnitConverter.py`, `tests/test_converter.py` — import |
| **pytest** | 10 passed |
| **golden** | `tests/golden/VAL-01.approved.txt` matched ✅ |

### #2 P1 — Long Method · Invalid format 중복

| 항목 | 내용 |
|------|------|
| **변경** | `UnitConverter.py` only |
| **추출** | `_parse_unit_value()`, `_to_meter_value()`, `_print_conversions()` |
| | `_INVALID_FORMAT_MSG` — Duplicated Code 해소 |
| **Budget** | 파일1 · 메서드3 |
| **pytest** | 10 passed |
| **golden** | matched ✅ (diff 없음) |

---

## 5) pytest 스냅샷 (저장 시점)

```bash
python -m pytest tests/ -v
# → 10 passed, 0 failed, 0 skipped

python -m pytest tests/ -k golden -v
# → 2 passed (VAL-01 approval, CONV-03 readme golden)
```

---

## 6) 남은 스멜 (다음 `/refactor-smell`)

| P | 유형 | 위치 | 권장 |
|---|------|------|------|
| P1 | Duplicated Code | `tests/test_converter.py` | VAL-01 Act fixture 또는 `_run_main` 공통화 |
| P2 | Feature Envy | `UnitConverter.py` | boundary/entity 분리 — 별도 Phase·Budget 분할 |
| P2 | Mysterious Name | `_print_conversions` 인자 | 선택적 rename |

---

## 7) 다음 권장

1. `/refactor-smell` 재실행 — 후보 #3 또는 남은 P1 확인
2. `/refactor-safe` — VAL-01 Act 중복 (Budget: 파일1)
3. README·Rule에 Refactor Command 반영 ✅ (Step6 문서화)

---

## 참고

| 문서 | 경로 |
|------|------|
| Step4 RED→GREEN | `Report/Step4_TDD_RED_보고서.md` |
| refactor-smell Command | `.cursor/commands/refactor-smell.md` |
| refactor-safe Command | `.cursor/commands/refactor-safe.md` |
| TDD Skill | `.cursor/skills/unit-converter-tdd/SKILL.md` |
