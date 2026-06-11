# Step4 TDD RED 프롬프트

## 역할 설정

```
@c:\DEV\UnitConverter_05\ Step4 TDD RED를 진행할거야.
너는 Unit Converter P0 Test ID에 대해 RED(TDD Phase: red)만 수행한다.
규칙:
1. 한 번에 Test ID 1개만 RED (전체 6건 순차 진행 시에도 ID 단위로 선언·보고).
2. tests/manifest.json의 Given/Then을 따른다.
3. UnitConverter.py 및 루트 프로덕션 코드는 수정하지 않는다.
4. pytest.skip / xfail / assert 완화로 통과 우회 금지.
5. 각 Phase 후 pytest 실행·결과 보고 (passed / failed / skipped).
```

---

## 필수 선언 (응답 첫 줄)

```
TDD Phase: red | Test ID: <VAL-xx|CONV-xx> — RED
```

---

## 사전 확인

1. `README.md` — P0·품질 요구
2. `Report/Step3_워크북.md` — 하지 않을 것 §4
3. `tests/manifest.json` — Given/Then·Mom Test 메모
4. `.cursorrules` — RED 없는 GREEN 금지

---

## P0 Test ID 순서 (manifest)

| 순서 | Test ID | Given | Then |
|------|---------|-------|------|
| 1 | VAL-01 | `meter:-1` | 음수 거부 |
| 2 | VAL-02 | `meter` / `abc` | Invalid format |
| 3 | VAL-03 | `metre:2.5` | Unknown unit |
| 4 | CONV-01 | `meter:2.5` | meter/feet/yard 3줄 |
| 5 | CONV-02 | `feet:10` | meter 기준 역변환 |
| 6 | CONV-03 | `meter:2.5` | feet ≈ 8.2 (±0.1) |

---

## RED 절차 (Test ID 1건)

1. `tests/manifest.json`에서 Given/Then 확인.
2. `tests/test_converter.py` skeleton의 `pytest.skip` 제거 = Given/Then AAA 본문 **동시** 작성.
3. `monkeypatch` + `capsys`로 `main()` 호출 (대화형 `input` 대체).
4. `pytest -k "<TestID_언더스코어>" -v` 실행 → **FAIL** 확인 (이미 PASS면 “스타터 충족”으로 보고).
5. RED 보고 템플릿 작성.
6. **프로덕션 코드 미수정** 유지.

---

## pytest 명령

```bash
# 단일 Test ID (하이픈 대신 언더스코어)
pytest -k VAL_01 -v

# P0 전체
pytest -m p0 -v --maxfail=10
```

---

## RED 보고 템플릿

```markdown
## RED 보고
- TDD Phase: red | Test ID: VAL-01 — RED
- Given / Then: (manifest 인용)
- pytest: `pytest -k VAL_01 -v` → N passed, M failed, K skipped
- FAIL: (실패 assert·출력 스니펫)
- 변경: tests/ 만
- Mom Test 연결: (manifest mom_test 필드)
```

---

## Cursor 연결

| 용도 | 경로 |
|------|------|
| RED만 | Command `/tdd-red` |
| GREEN·REFACTOR | Skill `@unit-converter-tdd` |
| Rule | `.cursorrules` |

---

## 전체 RED 한 번에 요청 (본 세션 완료 예시)

```
P0 Test ID VAL-01부터 CONV-03까지 RED 진행해줘.
- manifest Given/Then 준수
- UnitConverter.py 수정 금지
- 마지막에 pytest -m p0 -v 전체 보고
```

---

## 다음 Phase (RED 완료 후)

```
VAL-01 GREEN 해줘
```

→ `@unit-converter-tdd` Skill, `UnitConverter.py` 최소 수정, `pytest -m p0` 회귀 확인.

---

## 저장

RED 세션 종료 시:

```
Report 폴더와 Prompt 폴더에 Step4 RED 산출물 저장!!!
```

→ `Prompt/Step4_TDD_RED_저장_프롬프트.md` 참고.
