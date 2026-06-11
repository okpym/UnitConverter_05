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
| Skill | `@magic-square-tdd` — **있으면 자동 따름** (`.cursor/skills/magic-square-tdd/SKILL.md`) |
| Skill (본 repo) | `@unit-converter-tdd` — magic-square-tdd 없을 때 |
| RED 본문 (다음) | `/tdd-red` — assert 본문·실패 검증 |

> **magic-square-tdd Skill이 있으면 자동 따름.** 경로·픽스처·상수·마커는 Skill SSOT. 없으면 본 Command + `@unit-converter-tdd` + `tests/manifest.json`.

---

## 동작 조건

- **추가 인자 없이** `/red-skeleton` 만으로 동작한다 (직전 채팅의 `/red-test-plan` 4블록·Test ID 사용).
- Test ID·파일·함수명은 **블록 3 테스트 플랜**과 1:1 일치.
- 한 번에 **Test ID 1개**만 (` .cursorrules` TDD 원칙).
- 변경 범위: **`tests/` 만** (필요 시 `tests/conftest.py` 픽스처 추가 — 본 Command 명시분만).

---

## 필수 선언 (응답 첫 줄)

```
Phase: red | Layer: entity | Track: Logic
```

| 필드 | 값 | 비고 |
|------|-----|------|
| Phase | `red` | 고정 |
| Layer | `entity` \| `boundary` | Track A: `Layer: boundary`만 변경 후 동일 절차 |
| Track | `Logic` \| `UI` | P0 Logic·entity 기본 |

---

## 절차

1. 채팅 또는 직전 `/red-test-plan` 출력에서 **Test ID·블록 2·3** 확인.
2. `tests/manifest.json` Given/Then과 설계표 정합 확인.
3. **블록 3** 경로·함수명으로 테스트 함수 작성 (아래 스켈레톤 규칙).
4. Arrange에 필요한 **픽스처 데이터만** 상수 import (`entity/constants.py` — 아래 §상수).
5. `pytest -k "<Test ID>" -v` 실행 → **FAIL** (`pytest.fail` — RED 스켈레톤).
6. **RED Skeleton 보고** (아래 템플릿).

---

## 스켈레톤 규칙 (필수)

| 항목 | 규칙 |
|------|------|
| AAA | `# Given:` · `# When:` · `# Then:` 주석 3줄 (manifest G/W/T 반영) |
| Then | **`pytest.fail("RED: {Test ID} — …")` 한 줄만** — Then 설명은 fail 메시지에 포함 |
| assert | **본문 금지** — `/tdd-red`에서 Given/Then assert 작성 |
| skip / xfail | **금지** |
| 통과 더미 | `pass`, `assert True`, 빈 Then **금지** |
| src/ · `UnitConverter.py` | **수정 금지** |
| Domain Mock | Logic Track — `/red-test-plan` 블록 4와 동일 |

### 상수 (픽스처 데이터만)

- **`entity/constants.py`** 에서 `34`, `16`, `4` import — **테스트 Arrange·픽스처 데이터 참조만**.
- 프로덕션·src 구현 추가 금지 (import만 허용).

```python
from entity.constants import GRID_SIZE, BLANK_COUNT, MAGIC_SUM  # 4, 2→0개, 34 등 프로젝트 정의명
```

> UnitConverter repo: 상수 모듈 없으면 manifest Given 리터럴·`monkeypatch`/`capsys`만 사용 (Skill 우선).

### conftest (Magic Square 기본)

| 픽스처 | 정의 |
|--------|------|
| `grid_g1` | `tests/conftest.py` — **0이 두 칸**, **row-major** 1차원 또는 2차원 그리드 |

```python
@pytest.fixture
def grid_g1():
    """Given grid: 0 두 개, row-major (Magic Square G1)."""
    return [
        16, 3, 2, 13,
        5, 10, 11, 8,
        9, 6, 7, 12,
        4, 15, 14, 0,  # 예: row-major; 0 위치는 Test ID Given에 맞게 조정
    ]
```

> 이미 존재하면 설계표 Given에 맞게 **값만** 조정. UnitConverter: `monkeypatch`, `capsys`, `manifest` (기존 `tests/conftest.py`).

---

## 템플릿 예시 (Magic Square · entity · Logic)

```python
import pytest

from entity.constants import GRID_SIZE, MAGIC_SUM  # 4, 34 — 픽스처 데이터 참조만


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given: grid_g1 — 0 두 개, row-major
    # When: blank 좌표를 row-major 인덱스로 조회 (호출은 /tdd-red에서 연결)
    # Then: 두 blank 좌표가 manifest Then과 일치
    pytest.fail("RED: D-LOC-01 — blank 좌표 row-major 미구현")
```

### UnitConverter 대응 예 (VAL-01)

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

**기대:** 1 failed (`pytest.fail` — RED 스켈레톤). PASS면 스켈레톤 아님.

```markdown
## RED Skeleton 보고
- Phase: red | Layer: entity | Track: Logic | Test ID: D-LOC-01
- pytest: `pytest -k D-LOC-01 -v` → 0 passed, 1 failed, 0 skipped
- FAIL: test_d_loc_01_blank_coords_row_major — RED: D-LOC-01 — …
- 변경: tests/test_….py (tests/ 만)
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
| `src/` · `UnitConverter.py` · `entity/` **구현** 수정 | RED ④ — tests 스켈레톤만 |
| assert 본문 | `/tdd-red` 담당 |
| `pytest.skip()` · `xfail` · `pass` · `assert True` | RED 우회 |
| GREEN / REFACTOR | 선행 금지 |
| Domain Mock (Logic) | `/red-test-plan` 블록 4 |
| E001~E005 emit | P0 범위 밖 |

---

## 완료

스켈레톤 작성·pytest FAIL 확인 후:

**다음:** `/tdd-red` — `pytest.fail` 제거, Given/When Act + Then **assert** 본문 작성 → FAIL(AssertionError) 확인.
