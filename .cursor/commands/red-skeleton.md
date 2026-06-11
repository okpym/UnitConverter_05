# RED Skeleton — pytest.fail 스켈레톤 (Ask)

**ARRR A단계 (Ask = RED ④)** 만 수행한다.  
직전 `/red-test-plan` **설계표(블록 2·3)** 기준으로 `tests/`에 **pytest.fail 스켈레톤만** 작성한다.  
실제 assert 본문·GREEN·REFACTOR·프로덕션 수정은 하지 않는다.

| 연결 | 파일 |
|------|------|
| Rule | `.cursorrules` |
| 설계 (앞단) | `/red-test-plan` → `.cursor/commands/red-test-plan.md` |
| SSOT (FR) | `docs/PRD.md` |
| Test ID | `tests/manifest.json` |
| Skill | `@unit-converter-tdd` |
| RED 본문 (다음) | `/tdd-red` — assert 본문·AssertionError FAIL |

> **Track A (boundary):** 선언 `Layer: boundary`만 변경 후 동일 절차. Harness는 stdin/stdout 관찰 위주.

---

## 동작 조건

- **추가 인자 없이** `/red-skeleton` 만으로 동작 (직전 채팅 `/red-test-plan` 4블록·Test ID 사용).
- Test ID·파일·함수명은 **블록 3 테스트 플랜**과 1:1 일치.
- 한 번에 **Test ID 1개**만 (`.cursorrules` TDD 원칙).
- 변경 범위: **`tests/` 만** (필요 시 `tests/conftest.py` 픽스처 추가).

---

## 필수 선언 (응답 첫 줄)

```
Phase: red | Layer: entity | Track: Logic
```

| 필드 | 값 | 비고 |
|------|-----|------|
| Phase | `red` | 고정 |
| Layer | `entity` \| `boundary` | Track A: `Layer: boundary` |
| Track | `Logic` \| `UI` | P0 기본 `Logic` · `entity` |

---

## 절차

1. 채팅 또는 직전 `/red-test-plan` 출력에서 **Test ID·블록 2·3** 확인.
2. `tests/manifest.json` Given/Then과 설계표 정합 확인.
3. **블록 3** 경로·함수명으로 테스트 함수 작성 (아래 스켈레톤 규칙).
4. `pytest -k "<Test ID>" -v` 실행 → **FAIL** (`pytest.fail` — RED 스켈레톤).
5. **RED Skeleton 보고** (아래 템플릿).

---

## 스켈레톤 규칙 (필수)

| 항목 | 규칙 |
|------|------|
| AAA | `# Given:` · `# When:` · `# Then:` 주석 3줄 (manifest G/W/T) |
| Then | **`pytest.fail("RED: {Test ID} — …")` 한 줄만** |
| assert | **본문 금지** — `/tdd-red`에서 작성 |
| skip / xfail | **금지** |
| 통과 더미 | `pass`, `assert True`, 빈 Then **금지** |
| `UnitConverter.py` · `src/` | **수정 금지** |
| Domain Mock | Logic Track — `/red-test-plan` 블록 4와 동일 (Harness `monkeypatch`만) |

---

## 템플릿 (UnitConverter · VAL-01)

```python
import pytest

pytestmark = pytest.mark.p0


@pytest.mark.val
@pytest.mark.parametrize(
    "negative_input",
    [pytest.param("meter:-1", id="VAL-01")],
)
def test_VAL_01_negative_input_rejected(monkeypatch, capsys, negative_input):
    # Given: meter:-1 (manifest)
    # When: main() 호출 (/tdd-red에서 Act 연결)
    # Then: 음수 거부 — 변환 결과 미출력
    pytest.fail("RED: VAL-01 — 음수 입력 거부 assert 미작성")
```

---

## pytest · 보고 (Phase 종료 필수)

```bash
pytest -k "<Test ID>" -v
```

**기대:** 1 failed (`pytest.fail`). PASS면 스켈레톤 아님.

```markdown
## RED Skeleton 보고
- Phase: red | Layer: entity | Track: Logic | Test ID: VAL-01
- pytest: `pytest -k VAL-01 -v` → 0 passed, 1 failed, 0 skipped
- FAIL: test_VAL_01_negative_input_rejected[VAL-01] — RED: VAL-01 — …
- 변경: tests/test_converter.py (tests/ 만)
```

| 보고 항목 | 내용 |
|-----------|------|
| Test ID | manifest ID 1개 |
| FAIL 한 줄 | `test_… — RED: {Test ID} — …` |
| 변경 파일 | `tests/` 경로만 |

---

## 금지

| 금지 | 이유 |
|------|------|
| `UnitConverter.py` · `src/` **수정** | RED ④ — tests 스켈레톤만 |
| assert 본문 | `/tdd-red` 담당 |
| `pytest.skip()` · `xfail` · `pass` · `assert True` | RED 우회 |
| GREEN / REFACTOR | 선행 금지 |
| Domain Mock (Logic) | 블록 4 위반 |
| E001~E005 emit | P0 범위 밖 |

---

## 완료

스켈레톤 작성·pytest FAIL 확인 후:

**다음:** `/tdd-red` — `pytest.fail` 제거, Given/When Act + Then **assert** 본문 → FAIL(AssertionError) 확인.
