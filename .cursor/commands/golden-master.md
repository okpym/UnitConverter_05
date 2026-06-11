# Golden Master — Approval Test 구축·검증 (Respond)

**GREEN PASS 직후** 대상 Test ID에 **Golden Master(Approval Test)** 를 구축·검증한다.  
stdout·직렬화 결과를 `tests/golden/*.approved.txt`에 고정하고, 이후 Refactor에서 **matched** 게이트로 사용한다.  
`git commit` / `push`는 **사용자 명시 요청 시만**.

| 연결 | 파일 |
|------|------|
| Rule | `.cursorrules` |
| SSOT (FR) | `docs/PRD.md` |
| Test ID | `tests/manifest.json` |
| GREEN (앞단) | `/green-minimal` · `@unit-converter-tdd` |
| Approval 헬퍼 | `tests/_approval.py` |
| Golden 저장소 | `tests/golden/{Test ID}.approved.txt` |
| Refactor 게이트 | `/refactor-safe` |

> **UnitConverter repo:** VAL-* 등 ECB **문자열 stdout** Golden. `CONV-*` 수치 Golden은 별도 assert(허용 오차)와 구분.

---

## 동작 조건

- **추가 인자 없이** `/golden-master` 만으로 동작 (직전 GREEN의 **Test ID 1개** 사용).
- 한 번에 **Test ID 1개**만 — RED 묶음·parametrize id와 1:1.
- **전제:** 대상 Test ID **pytest PASS** (`/green-minimal` 또는 `@unit-converter-tdd` GREEN 완료).
- 변경 범위: **`tests/_approval.py`** (없을 때만 생성) · **`tests/golden/`** · **`tests/test_*.py`** (golden 테스트 함수 추가).

---

## 필수 선언 (응답 첫 줄)

```
Phase: green | Layer: entity | Track: Logic
```

| 필드 | 값 | 비고 |
|------|-----|------|
| Phase | `green` | Golden은 GREEN 직후 구축 |
| Layer | `entity` \| `boundary` | stdout 관찰 기본 `entity` |
| Track | `Logic` \| `UI` | P0 기본 `Logic` |

---

## 절차

1. **GREEN PASS 재확인**
   ```bash
   pytest -k "<Test ID>" -v
   ```
   대상 행위 테스트(예: `test_VAL_01_negative_input_rejected`) **PASS** 필수.

2. **`tests/_approval.py` — `assert_matches_golden`**
   - 없으면 생성. 있으면 **재사용** (수정 최소).
   - `UPDATE_GOLDEN=1` 일 때만 golden 파일 **쓰기**; 그 외 **읽기·비교만**.

3. **Golden 테스트 연결**
   - `tests/test_converter.py` (또는 블록 3 경로)에 `@pytest.mark.golden` 테스트 추가.
   - Given/When은 행위 테스트와 동일 Act → `capsys` stdout 캡처 → `assert_matches_golden(out, "<Test ID>.approved.txt")`.

4. **기준 파일 생성** — `UPDATE_GOLDEN=1`
   ```bash
   # PowerShell
   $env:UPDATE_GOLDEN=1; python -m pytest tests/ -k "<Test ID>" -v
   Remove-Item Env:UPDATE_GOLDEN -ErrorAction SilentlyContinue

   # bash
   UPDATE_GOLDEN=1 pytest -k "<Test ID>" -v
   unset UPDATE_GOLDEN
   ```
   → `tests/golden/<Test ID>.approved.txt` 생성·갱신.

5. **matched 확인** — `UPDATE_GOLDEN` **unset**
   ```bash
   python -m pytest tests/ -k golden -v
   # 또는
   python -m pytest tests/test_converter.py::test_<ID>_golden_stdout_approval -v
   ```
   **기대:** PASS, diff 없음.

6. **Golden Master 보고** (아래 템플릿).

---

## Golden 포맷 SSOT (고정 · 수동 편집 금지)

| 유형 | 규칙 | UnitConverter 예 |
|------|------|------------------|
| **int[6] · 1-index** | 배열 Golden은 **길이 6**, 인덱스 **1~6** (0-based 금지). 한 줄 한 원소 또는 프로젝트 직렬화 규약 준수 | (본 repo P0 미사용 — Magic Square 등 공유 규약) |
| **에러 코드 문자열** | prod `print` 문구와 **바이트 단위 일치** — 공백·콜론·예시 괄호 포함 | `Negative value: -1` |
| **정규화** | `_approval.py`: `actual.rstrip("\n") + "\n"` — trailing newline 1개 | `VAL-01.approved.txt` |
| **E001~E005** | P0 Golden에 ECB 에러 **코드 문자열** (예: `E001`) **포함 금지** — 사람이 읽는 메시지만 | VAL-* stdout 메시지 |

### VAL-01 에러 문자열 (고정)

```
Negative value: -1
```

- `-1`은 입력 value_str 그대로 (manifest `meter:-1`).
- golden 파일을 손으로 맞춰 통과시키는 행위 **금지** — 반드시 `UPDATE_GOLDEN=1`로 prod 출력에서 재생성.

---

## `_approval.py` 템플릿 (없을 때만 생성)

```python
"""Golden Master approval helpers."""

import os
from pathlib import Path

GOLDEN_DIR = Path(__file__).parent / "golden"


def assert_matches_golden(actual: str, relative: str) -> None:
    """Compare actual vs tests/golden/{relative} (e.g. VAL-01.approved.txt)."""
    path = GOLDEN_DIR / relative
    normalized = actual.rstrip("\n") + "\n"

    if os.environ.get("UPDATE_GOLDEN") == "1":
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(normalized, encoding="utf-8")
        return

    if not path.is_file():
        raise AssertionError(f"Golden missing: {path} — run UPDATE_GOLDEN=1 pytest …")

    expected = path.read_text(encoding="utf-8")
    if normalized != expected:
        raise AssertionError(
            f"Golden mismatch: {path}\n--- expected\n{expected}--- actual\n{normalized}"
        )
```

---

## Golden 테스트 템플릿 (VAL-01)

```python
@pytest.mark.val
@pytest.mark.golden
@pytest.mark.parametrize(
    "negative_input",
    [pytest.param("meter:-1", id="VAL-01")],
)
def test_VAL_01_golden_stdout_approval(monkeypatch, capsys, negative_input):
    """Given meter:-1 → Golden: stdout ECB 문자열 (Negative value)."""
    monkeypatch.setattr("builtins.input", lambda _: negative_input)

    from UnitConverter import main

    main()
    out = capsys.readouterr().out
    assert_matches_golden(out, "VAL-01.approved.txt")
```

`tests/conftest.py`에 `@pytest.mark.golden` 마커 등록 권장.

---

## pytest 명령 예시

**단일 Test ID (행위 + golden):**

```bash
pytest -k "VAL-01" -v
```

**golden 마커만:**

```bash
pytest -k golden -v
```

---

## 보고 템플릿

```markdown
## Golden Master 보고
- Phase: green | Layer: entity | Track: Logic | Test ID: VAL-01
- 전제: `pytest -k VAL-01` 행위 테스트 PASS ✅
- golden 경로: `tests/golden/VAL-01.approved.txt`
- matched: ✅ (`UPDATE_GOLDEN` unset, `pytest -k golden -v` → 1 passed)
- diff 요약: 없음 (또는 최초 생성 — UPDATE_GOLDEN=1 후 1줄 `Negative value: -1`)
- 변경: tests/_approval.py (유지), tests/test_converter.py (golden 테스트), tests/golden/VAL-01.approved.txt
```

| 보고 항목 | 내용 |
|-----------|------|
| golden 경로 | `tests/golden/{Test ID}.approved.txt` |
| matched | ✅ / ❌ · `UPDATE_GOLDEN` unset 여부 |
| diff 요약 | mismatch 시 expected vs actual **한 줄 요약**; 없으면 `없음` |

---

## 금지

| 금지 | 이유 |
|------|------|
| **golden 파일 수동 편집**으로 통과 | Approval 우회 — `UPDATE_GOLDEN=1`만 허용 |
| **ISS 없이** golden 재생성 | 의도적 변경은 `Report/` ISS 1문단 후에만 (`/refactor-safe` §Golden) |
| GREEN 미완료 Test ID Golden | 행위 테스트 FAIL 상태에서 baseline 생성 금지 |
| **assert 완화** · golden 테스트 삭제 | 거버넌스 붕괴 |
| **E001~E005** 코드 문자열을 golden에 넣기 | P0 ECB 범위 밖 |
| **int[6] 0-index** 직렬화 | 1-index SSOT 위반 |
| 프로덕션 수정 (golden 맞추기) | 동작 변경은 GREEN·별도 FR — golden은 관찰만 |

---

## 완료

golden **matched** 확인 후:

**다음:** `/refactor-smell` (선택) → `/refactor-safe` — Refactor마다 `pytest -k golden` **matched** 게이트.

**ARRR 파이프라인:** `/red-test-plan` → `/red-skeleton` → `/tdd-red` → `/green-minimal` → **`/golden-master`** → `/refactor-smell` → `/refactor-safe`
