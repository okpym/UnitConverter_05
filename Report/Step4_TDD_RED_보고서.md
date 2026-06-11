# Step4 TDD RED 보고서

- **프로젝트:** Unit Converter (`UnitConverter_05`)
- **일자:** 2026-06-11
- **세션 범위:** P0 Test ID 6건 RED 본문 작성 · pytest FAIL 확인
- **선행 산출:** Step3 워크북 · `tests/manifest.json` · `/tdd-red` · `@unit-converter-tdd`
- **Mom Test 출처:** Step3 가상 시뮬레이션 (학생 페르소나)

---

## 1) 주제 한 문장

> **README P0 요구를 `manifest.json` Test ID 단위로 RED 테스트로 고정하고, pytest FAIL/PASS로 “아직 구현 안 된 것”과 “스타터에 이미 있는 것”을 분리한다.**

---

## 2) R-G-I-O

| 구분 | 정의 | Step4 내용 |
|------|------|------------|
| **R — Reality** | 현재 상태 | Step3까지 skeleton 6건 `skip`. `UnitConverter.py` 37줄 — 형식·미등록 단위는 처리, **음수 미검증** (`meter:-1` 변환 출력). |
| **G — Goal** | 이번 세션 목표 | P0 6 Test ID RED 본문 완료. `pytest -m p0`로 VAL-01 **FAIL**, 나머지 **PASS** 확인. 프로덕션 코드 **미수정**. |
| **I — Input** | 입력·전제 | `tests/manifest.json`, `.cursorrules` TDD 규칙, `tests/test_converter.py`, 스타터 `UnitConverter.py`. |
| **O — Output** | 산출 | RED 테스트 본문(`tests/test_converter.py`), 본 보고서, RED·저장 프롬프트. |

---

## 3) RED 결과 요약

### pytest (세션 종료 시점)

```bash
pytest -m p0 -v --maxfail=10
```

| 결과 | 건수 |
|------|------|
| **passed** | 6 |
| **failed** | 1 |
| **skipped** | 0 |
| **수집** | 7 (VAL-02 파라미터 2케이스) |

### Test ID별 RED 상태

| Test ID | Given | Then (manifest) | pytest | RED 판정 |
|---------|-------|-----------------|--------|----------|
| **VAL-01** | `meter:-1` | 음수 거부 | **FAIL** | 진짜 RED — 구현 필요 |
| **VAL-02** | `meter`, `abc` | Invalid format | PASS (×2) | 테스트 확립, 스타터 충족 |
| **VAL-03** | `metre:2.5` | Unknown unit | PASS | 테스트 확립, 스타터 충족 |
| **CONV-01** | `meter:2.5` | meter/feet/yard 3줄 | PASS | 테스트 확립, 스타터 충족 |
| **CONV-02** | `feet:10` | meter 기준 역변환 | PASS | 테스트 확립, 스타터 충족 |
| **CONV-03** | `meter:2.5` | feet ≈ 8.2 (±0.1) | PASS | Golden Master 수치 검증 통과 |

---

## 4) FAIL 상세 — VAL-01

**Mom Test 연결:** `feet:-3` 캡처만 — 본 코드 미연결 (Step3 증거 2)

**입력:** `meter:-1`

**현재 출력 (버그):**

```
-1.0 meter = -1.0 meter
-1.0 meter = -3.28084 feet
-1.0 meter = -1.09361 yard
```

**테스트 기대:**

1. ` feet` / ` yard` 변환 줄 **없음**
2. `negative` / `invalid` / `error` / `음수` 중 거부 안내 **있음**

**assert 실패:** 음수 입력이 변환 결과로 출력됨.

---

## 5) 테스트 설계 (RED 본문)

| Test ID | 검증 전략 |
|---------|-----------|
| VAL-01 | `monkeypatch`로 `input` 고정 → `main()` → 변환 줄·거부 메시지 |
| VAL-02 | `@pytest.mark.parametrize("meter", "abc")` → `Invalid format` + 변환 줄 0 |
| VAL-03 | `metre:2.5` → `Unknown unit` + 변환 줄 0 |
| CONV-01 | `meter:2.5` → ` = ` 포함 3줄, 각 줄 단위 suffix |
| CONV-02 | `feet:10` → meter/feet/yard 수치, `10/METER_TO_FEET` 역변환 |
| CONV-03 | feet 값 파싱 → `abs(feet - 8.2) <= 0.1` (README Golden) |

**공통 헬퍼:** `_run_main`, `_conversion_lines` (`tests/test_converter.py`)

**프로덕션 import:** `sys.path`에 프로젝트 루트 추가 후 `from UnitConverter import main`

---

## 6) Mom Test 증거 ↔ RED 매핑

| Mom Test 증거 | RED 대응 |
|---------------|----------|
| 4시간 요구 해석 | manifest 6 Test ID → 할 일 목록 확정 |
| `feet:-3` 캡처만 | **VAL-01 FAIL** — 유일 미구현 |
| assert·반올림 원복 불안 | CONV-03 Golden (±0.1) — **이미 PASS** (raw float로도 허용 범위 내) |

---

## 7) 변경 파일

| 경로 | 변경 |
|------|------|
| `tests/test_converter.py` | skeleton `skip` 제거, P0 RED 본문 6 ID + 헬퍼 |
| `UnitConverter.py` | **미변경** (RED 규칙) |

---

## 8) 금지·범위 밖 (Step3 §4 유지)

- cubit 동적 등록, `units.json`, JSON/CSV 출력
- OCP/SRP 대규모 리팩터 (REFACTOR Phase에서 선택)
- Step1 inch↔cm 시나리오 FR 구현

---

## 9) 다음 세션

| 순서 | Phase | Test ID | 작업 |
|------|-------|---------|------|
| 1 | **GREEN** | VAL-01 | `UnitConverter.py` 음수 검증 최소 추가 |
| 2 | **GREEN** | VAL-02~03, CONV-01~03 | 코드 변경 없이 PASS 유지 확인 |
| 3 | **REFACTOR** (선택) | P0 전체 | SRP 파싱/검증/변환 분리, `pytest -m p0` 게이트 |

**권장 명령:** `@unit-converter-tdd` + “VAL-01 GREEN”

---

## 참고

| 문서 | 경로 |
|------|------|
| Step3 워크북 | `Report/Step3_워크북.md` |
| Test ID 출처 | `tests/manifest.json` |
| RED Command | `.cursor/commands/tdd-red.md` |
| TDD Skill | `.cursor/skills/unit-converter-tdd/SKILL.md` |
| RED 실행 프롬프트 | `Prompt/Step4_TDD_RED_프롬프트.md` |
