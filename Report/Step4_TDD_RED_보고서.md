# Step4 TDD RED→GREEN 보고서

- **프로젝트:** Unit Converter (`UnitConverter_05`)
- **일자:** 2026-06-11
- **세션 범위:** P0 Test ID — RED 본문 작성 → GREEN 최소 구현 (REFACTOR 미착수)
- **전제:** Step3 워크북 — Rule · Command · Skill · Test Loop skeleton

---

## 1) 세션 목표

Step3에서 만든 `tests/manifest.json`·pytest Harness 위에 **실패 테스트(RED) → 최소 구현(GREEN)** 루프를 실제로 돌려 README P0(VAL-01~03, CONV-01~03)를 검증 가능한 상태로 만든다.

---

## 2) Mom Test 연결

| 증거 (Step3) | 이번 세션 대응 |
|-------------|----------------|
| `feet:-3` 캡처만 — main 미연결 | **VAL-01** RED → GREEN: 음수 거부 구현 |
| 요구 해석 4시간 — Test ID 분해 | **ALL RED**: skeleton `skip` 제거, P0 전체 AAA 테스트 |
| 테스트·포맷 불안 원복 | Phase마다 `pytest -m p0 -v` 게이트 — 최종 **9 passed** |

---

## 3) TDD Phase 요약

| Test ID | RED | GREEN | 최종 |
|---------|-----|-------|------|
| **VAL-01** | `meter:-1` 음수 시 변환 미출력 assert → FAIL | `value < 0` 검증 추가 | PASS |
| **VAL-02** | `meter`/`abc` PASS, `meter:`/`:2.5` FAIL | 빈 unit·value → Invalid format | PASS (4 cases) |
| **VAL-03** | `metre:2.5` → Unknown unit | 스타터에 이미 구현 — 변경 없음 | PASS |
| **CONV-01** | `meter:2.5` 3줄 출력 | 스타터에 이미 구현 — 변경 없음 | PASS |
| **CONV-02** | `feet:10` meter 역변환 | 스타터에 이미 구현 — 변경 없음 | PASS |
| **CONV-03** | `meter:2.5` feet ≈ 8.2 (±0.1) | 스타터에 이미 구현 — 변경 없음 | PASS |

---

## 4) pytest 최종 결과

```bash
pytest -m p0 -v
```

| 결과 | 수 |
|------|-----|
| passed | 9 |
| failed | 0 |
| skipped | 0 |

### Test ID별 수집

| 노드 | 상태 |
|------|------|
| `test_VAL_01_negative_input_rejected[VAL-01]` | PASS |
| `test_VAL_02_invalid_format_rejected[VAL-02-no-colon]` | PASS |
| `test_VAL_02_invalid_format_rejected[VAL-02-garbage]` | PASS |
| `test_VAL_02_invalid_format_rejected[VAL-02-empty-value]` | PASS |
| `test_VAL_02_invalid_format_rejected[VAL-02-empty-unit]` | PASS |
| `test_VAL_03_unknown_unit_rejected[VAL-03]` | PASS |
| `test_CONV_01_meter_input_outputs_all_units[CONV-01]` | PASS |
| `test_CONV_02_feet_input_converts_via_meter[CONV-02]` | PASS |
| `test_CONV_03_golden_meter_to_feet_matches_readme[CONV-03]` | PASS |

---

## 5) 프로덕션 변경 (`UnitConverter.py`)

GREEN에서 추가된 검증만 (최소 diff):

```python
# VAL-01
if value < 0:
    print(f"Negative value: {value_str}")
    return

# VAL-02 (빈 단위·빈 값)
if not unit or not value_str:
    print("Invalid format. Use unit:value (ex: meter:2.5)")
    return
```

스타터에 있던 항목(콜론 없음, Unknown unit, 변환 로직)은 테스트로 회귀 고정만 수행.

---

## 6) 테스트 변경 (`tests/`)

| 파일 | 내용 |
|------|------|
| `test_converter.py` | VAL-01~03, CONV-01~03 AAA 본문; skeleton `skip` 전부 제거 |
| `conftest.py` | 루트 `UnitConverter` import용 `sys.path` |

### 테스트 패턴

- `monkeypatch` + `capsys`로 `main()` 입출력 검증
- `@pytest.mark.parametrize(..., id="VAL-xx")` — `pytest -k VAL-01` 필터
- 변환 여부: `feet`/`yard` 줄 존재 여부 또는 줄 끝 단위(`endswith`)

---

## 7) 성공 기준 달성 (Step3 SC 대비)

| ID | 기준 | 달성 |
|----|------|------|
| **SC-1** | manifest Test ID 1:1 | 유지 — 6 ID 테스트 본문 완료 |
| **SC-2** | RED 테스트 + Rule | VAL-01·02 RED FAIL 확인 후 GREEN |
| **SC-3** | Phase마다 pytest 보고 | RED/GREEN 각 Phase 후 pytest 실행·기록 |

---

## 8) 이번 세션에서 하지 않은 것 (Step3 §4)

| 항목 | 사유 |
|------|------|
| REFACTOR (SRP/OCP 클래스 분리) | P0 GREEN 완료 후 별도 Phase |
| cubit 동적 등록 · units.json | deferred |
| JSON/CSV 출력 포맷 | deferred |
| 출력 반올림 포맷 (`8.2` 문자열) | CONV-03은 수치 ±0.1만 검증 |

---

## 9) 다음 권장

1. **REFACTOR** — `UnitConverter.py` SRP 분리 (입력 파싱 · 검증 · 변환 · 출력)
2. **P1 / deferred** — OCP 단위 등록, 설정 외부화 (별도 Test ID·Phase)
3. README § Cursor AI — `다음 권장: /tdd-red VAL-01` 문구를 P0 완료 상태로 갱신

---

## 참고

| 문서 | 경로 |
|------|------|
| Step3 워크북 | `Report/Step3_워크북.md` |
| Test manifest | `tests/manifest.json` |
| TDD Skill | `.cursor/skills/unit-converter-tdd/SKILL.md` |
| RED Command | `.cursor/commands/tdd-red.md` |
