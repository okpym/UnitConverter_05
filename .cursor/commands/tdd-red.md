# TDD RED — 실패 테스트 먼저

**RED(TDD Phase: red)** 만 수행한다. GREEN·REFACTOR·`UnitConverter.py` 수정은 하지 않는다.

| 연결 | 파일 |
|------|------|
| Rule | `.cursorrules` |
| Skill | `@unit-converter-tdd` → `.cursor/skills/unit-converter-tdd/SKILL.md` |
| Test ID | `tests/manifest.json` |

---

## 필수 선언 (응답 첫 줄)

```
TDD Phase: red | Test ID: <CONV-xx|VAL-xx> — RED
```

---

## 절차

1. `README.md`, `Report/Step3_워크북.md` — P0·하지 않을 것 확인.
2. `tests/manifest.json`에서 Test ID의 Given/Then 확인.
3. `tests/test_converter.py` (또는 분리 파일)에 **AAA** 실패 테스트 작성.
4. skeleton `skip` 제거 = Given/Then 구현과 동시.
5. `pytest -k "<Test ID>" -v` → **FAIL** 확인 (PASS면 RED 아님).

---

## 보고 템플릿

```markdown
## RED 보고
- TDD Phase: red | Test ID: VAL-01 — RED
- pytest: `pytest -k VAL-01 -v` → N passed, M failed, K skipped
- FAIL: test_… — …
- 변경: tests/ 만
```

---

## 금지

- `UnitConverter.py` 및 루트 프로덕션 코드 **수정 금지**
- assert 완화, skip/xfail, GREEN 선행

**다음:** GREEN → `@unit-converter-tdd` Skill 또는 사용자 요청.
