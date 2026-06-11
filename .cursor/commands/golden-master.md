# Golden Master — Approval Test 구축·검증

**GREEN PASS 직후** 대상 Test ID에 **Golden Master(Approval Test)** 를 구축·검증한다.  
기준 파일과 실제 출력의 **바이트 단위 일치**로 회귀를 잡는다. src 로직 변경은 **본 Command 범위 밖** (이미 GREEN 완료 전제).

| 연결 | 파일 |
|------|------|
| Rule | `.cursorrules` |
| SSOT (FR) | `docs/PRD.md` |
| Test ID | `tests/manifest.json` |
| GREEN (앞단) | `/green-minimal` |
| Skill | `@magic-square-tdd` — **있으면 자동 따름** |
| Skill (본 repo) | `@unit-converter-tdd` — magic-square-tdd 없을 때 |

> **magic-square-tdd Skill이 있으면 자동 따름.** golden 경로·직렬화 포맷은 Skill SSOT.

---

## 동작 조건

- **전제:** 대상 Test ID가 `pytest -k "<Test ID>" -v` → **PASS** (GREEN 완료).
- **1 Golden = Test ID 1개** — `tests/golden/{id}.approved.txt` 1파일.
- 변경 범위: `tests/_approval.py`, `tests/golden/`, 해당 Test ID approval 테스트 (**src/ 수정 금지**).
- `git commit` / `push`: **사용자 명시 요청 시만**.

---

## 필수 선언 (응답 첫 줄)

```
Phase: green | Layer: entity | Track: Logic
```

| 필드 | 값 | 비고 |
|------|-----|------|
| Phase | `green` | Golden은 GREEN 산출물 고정 단계 |
| Layer | `entity` \| `boundary` | boundary는 Layer만 변경 |
| Track | `Logic` \| `UI` | P0 Logic·entity 기본 |

---

## 절차

### 0. GREEN 재확인

```bash
pytest -k "<Test ID>" -v
```

FAIL이면 `/green-minimal` 선행 — Golden 진행 금지.

### 1. `tests/_approval.py` — `assert_matches_golden`

없으면 **생성**. 있으면 재사용.

| 함수 | 역할 |
|------|------|
| `assert_matches_golden(actual: str, golden_id: str)` | `tests/golden/{golden_id}.approved.txt` 와 `actual` 비교 |
| `UPDATE_GOLDEN=1` | env 설정 시 golden **덮어쓰기** 후 pass (기준 생성) |
| env 없음 | 불일치 시 `AssertionError` + **diff 요약** |

```python
# tests/_approval.py (스켈레ton — Skill·repo에 맞게 보완)
import os
from pathlib import Path

GOLDEN_DIR = Path(__file__).parent / "golden"


def assert_matches_golden(actual: str, golden_id: str) -> None:
    """actual vs tests/golden/{golden_id}.approved.txt"""
    path = GOLDEN_DIR / f"{golden_id}.approved.txt"
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

### 2. Golden 파일 연결

| 항목 | 규칙 |
|------|------|
| 경로 | `tests/golden/{Test ID}.approved.txt` |
| Test ID | manifest ID 그대로 (예: `D-LOC-01`, `VAL-01`, `CONV-03`) |
| 테스트 | Given/When Act 후 `actual` 직렬화 → `assert_matches_golden(actual, "<Test ID>")` |

### 3. 기준 파일 생성 — `UPDATE_GOLDEN=1`

**최초 1회** — GREEN PASS 출력을 golden으로 고정:

```bash
# Windows (PowerShell)
$env:UPDATE_GOLDEN=1; pytest -k "<Test ID>" -v

# macOS / Linux / Git Bash
UPDATE_GOLDEN=1 pytest -k "<Test ID>" -v
```

- 생성·갱신 파일: `tests/golden/<Test ID>.approved.txt`
- **src/ 코드는 변경하지 않음** — Act 결과만 기록.

### 4. matched 확인 — `UPDATE_GOLDEN` 없음

```bash
pytest -k "<Test ID>" -v
```

| 결과 | 의미 |
|------|------|
| **PASS** | golden **matched** |
| **FAIL** | mismatch — diff 확인 후 **src 수정**(GREEN) 또는 Act 직렬화 버그 수정 (golden 수동 편집 **금지**) |

---

## 출력 직렬화 규칙 (고정)

Golden 비교 전 `actual` 문자열은 **아래 포맷 SSOT**. 임의 변경 금지.

### Magic Square · entity (기본)

| 타입 | 포맷 |
|------|------|
| **좌표 `int[6]`** | **1-index** — `[r1,c1,r2,c2,r3,c3]` 공백 구분 한 줄 (예: `1 4 2 3 4 1`) |
| **에러 코드** | ECB 문자열 고정 — `Invalid format` / `Unknown unit` 등 (**E001~E005 코드 문자열 사용 금지**) |
| **그리드** | row-major, 셀 공백 구분, 행은 `\n` (Skill SSOT 우선) |

```python
def serialize_coords_1index(coords: list[int]) -> str:
    assert len(coords) == 6
    return " ".join(str(x) for x in coords) + "\n"
```

### UnitConverter (stdout Golden)

| 타입 | 포맷 |
|------|------|
| stdout | `capsys.readouterr().out` 그대로, trailing newline 정규화 (`_approval.py`) |
| 에러 | PRD 키워드 문자열 — `Invalid format`, `Unknown unit`, `Negative value` |

---

## 금지

| 금지 | 이유 |
|------|------|
| **`tests/golden/*.approved.txt` 수동 편집**으로 pytest 통과 | Golden 우회 — Act·src를 고쳐야 함 |
| **UPDATE_GOLDEN**으로 mismatch 은폐 (env 켠 채 matched 검증 생략) | 4단계 필수 |
| **직렬화 포맷 임의 변경** | diff 불가·회귀 무력화 |
| **E001~E005** golden 기준 | P0 ECB 범위 밖 |
| **src/ 수정** (GREEN 이미 PASS 전제) | Golden 단계는 Harness·golden만 |
| **다른 Test ID** golden 동시 갱신 | 1 ID = 1 golden |

---

## 보고 템플릿

```markdown
## Golden Master 보고
- Phase: green | Layer: entity | Track: Logic | Test ID: D-LOC-01
- golden: tests/golden/D-LOC-01.approved.txt
- UPDATE_GOLDEN=1: 기준 생성 완료 (또는 이미 존재 — 생략)
- matched: ✅ PASS (`pytest -k D-LOC-01 -v`, UPDATE_GOLDEN unset)
- diff: (mismatch 시) expected N lines / actual M lines — 첫 차이: «한 줄 요약»
- 변경: tests/_approval.py, tests/golden/D-LOC-01.approved.txt, tests/test_….py
```

| 보고 항목 | 내용 |
|-----------|------|
| **golden 경로** | `tests/golden/{id}.approved.txt` |
| **matched 여부** | PASS → matched / FAIL → mismatch |
| **diff 요약** | mismatch 시 첫 상이 줄·길이 차 (전문은 pytest 출력) |

---

## pytest 명령 요약

```bash
# ① GREEN 확인
pytest -k "<Test ID>" -v

# ② 기준 생성 (최초)
UPDATE_GOLDEN=1 pytest -k "<Test ID>" -v

# ③ matched 검증 (필수)
pytest -k "<Test ID>" -v
```

---

## 완료

`UPDATE_GOLDEN` **없이** PASS = golden **matched** 확인 후:

**다음:** 다음 Test ID GREEN → Golden, 또는 REFACTOR Phase (golden 재검증 필수).
