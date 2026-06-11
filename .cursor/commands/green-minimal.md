# GREEN Minimal — RED 1묶음 최소 구현 (Respond)

**ARRR R단계 (Respond = GREEN)** 만 수행한다.  
**RED 1묶음(Test ID 1개)** 에 대해 `src/` **최소 구현**으로 해당 테스트를 **PASS**시킨다.  
REFACTOR·다른 Test ID 선행 해결·assert 완화는 하지 않는다.

| 연결 | 파일 |
|------|------|
| Rule | `.cursorrules` |
| SSOT (FR) | `docs/PRD.md` |
| Test ID | `tests/manifest.json` |
| 상수 SSOT | `entity/constants.py` (또는 Skill·repo 정의 경로) |
| RED (앞단) | `/red-test-plan` → `/red-skeleton` → `/tdd-red` |
| Skill | `@magic-square-tdd` — **있으면 자동 따름** |
| Skill (본 repo) | `@unit-converter-tdd` — magic-square-tdd 없을 때 |
| REFACTOR (다음) | 별도 Phase — 본 Command 범위 밖 |

> **magic-square-tdd Skill이 있으면 자동 따름.**  
> UnitConverter repo: 프로덕션은 루트 `UnitConverter.py` (및 이후 분리 모듈) — `src/`와 동일 취급.

---

## 동작 조건

- **RED 1묶음 = Test ID 1개** (parametrize id·마커 묶음 포함).
- **1커밋 = 1 RED 묶음** — `git commit`은 **사용자 명시 요청 시만** (`.cursorrules`).
- 변경: **`src/`(또는 `UnitConverter.py`) + 해당 Test ID 테스트** — 이번 묶음 assert 교체만.

---

## 필수 선언 (응답 첫 줄)

```
Phase: green | Layer: entity | Track: Logic
```

| 필드 | 값 | 비고 |
|------|-----|------|
| Phase | `green` | 고정 |
| Layer | `entity` \| `boundary` | boundary GREEN은 Layer만 변경 |
| Track | `Logic` \| `UI` | P0 Logic·entity 기본 |

---

## 절차

1. **RED 재확인** — 대상 Test ID 테스트가 RED 상태인지 확인 (`pytest.fail` 또는 AssertionError FAIL).
   ```bash
   pytest -k "<Test ID>" -v
   ```
2. **`docs/PRD.md` · manifest** — Given/Then·Invariant 재확인.
3. **`src/` 최소 구현** — 이번 Test ID PASS에 **필요한 코드만** 추가·수정.
4. **테스트 정리** — `pytest.fail` **제거**, Then을 manifest **assert 본문**으로 교체 (완화 금지).
5. **PASS 확인**
   ```bash
   pytest -k "<Test ID>" -v
   pytest tests/test_<module>.py -v
   ```
6. **회귀** — P0 또는 동 파일 내 다른 테스트 FAIL 시 **즉시 수정** (이번 GREEN 범위 내).
   ```bash
   pytest -m p0 -v --maxfail=3
   ```
7. **GREEN Minimal 보고** (아래 템플릿).

---

## 구현 규칙

### 상수 · 하드코딩

| 규칙 | 내용 |
|------|------|
| **매직넘버 금지** | `34`, `16`, `4`, `3.28084` 등 리터럴을 src·테스트에 직접 쓰지 않음 |
| **SSOT** | `entity/constants.py` (또는 repo Skill이 정한 constants 모듈)에서 import |
| **최소 범위** | 이번 Test ID에 필요한 상수·함수만 추가 |

```python
# ✅ entity/constants.py
GRID_SIZE = 4
MAGIC_SUM = 34
BLANK_COUNT = 2

# ✅ entity/… 또는 UnitConverter.py
from entity.constants import GRID_SIZE, MAGIC_SUM
```

### ECB · 레이어

| 규칙 | 내용 |
|------|------|
| **E001~E005** | `raise` · `return` · stdout emit **금지** (P0) |
| **entity 레이어** | `boundary` · `control` **import 금지** — ECB 의존 역전 |
| **허용** | entity 내부 순수 로직, constants import, 테스트 Harness |

```python
# ❌ entity/ 내부
from boundary.cli import ...
from control.main import ...

# ✅ entity/ 내부
from entity.constants import MAGIC_SUM
```

### 테스트 교체 (pytest.fail → assert)

```python
# Before (RED skeleton)
pytest.fail("RED: VAL-01 — 음수 입력 거부 assert 미작성")

# After (GREEN)
from UnitConverter import main
main()
out = capsys.readouterr().out
assert not any(" feet" in line or " yard" in line for line in out.splitlines())
```

---

## pytest 명령 (예시)

**단일 Test ID (GREEN 게이트):**

```bash
pytest -k "VAL-01" -v
```

**파일 전체 (동 파일 회귀):**

```bash
pytest tests/test_converter.py -v
```

UnitConverter P0 회귀:

```bash
pytest -m p0 -v --maxfail=3
```

---

## 보고 템플릿

```markdown
## GREEN Minimal 보고
- Phase: green | Layer: entity | Track: Logic | Test ID: VAL-01
- pytest: `pytest -k VAL-01 -v` → 1 passed, 0 failed, 0 skipped
- PASS: test_VAL_01_negative_input_rejected[VAL-01]
- 변경: UnitConverter.py, tests/test_converter.py
- 회귀: `pytest -m p0 -v` → … (FAIL 있으면 즉시 수정 후 재보고)
- commit: (사용자 요청 시만) «1 RED 묶음 = 1 commit»
```

| 보고 항목 | 내용 |
|-----------|------|
| PASS Test ID | manifest ID 1개 |
| 변경 파일 | `src/`·`UnitConverter.py` + `tests/` 경로 |
| 회귀 | FAIL 시 **즉시 수정** 후 재실행·재보고 |

---

## 금지

| 금지 | 이유 |
|------|------|
| **이번 RED 묶음 외 Test ID** 동시 해결 | 1 GREEN = 1 Test ID |
| **REFACTOR** | 구조 정리·SRP 분리는 별도 Phase |
| **assert 완화·삭제** · skip/xfail | GREEN 우회 |
| **RED 없이** src 수정 | `.cursorrules` |
| **하드코딩·매직넘버** | constants SSOT 위반 |
| **E001~E005** raise/return/emit | P0 ECB 범위 밖 |
| **entity → boundary/control import** | ECB 레이어 규칙 |
| **`git commit` / `push`** | 사용자 명시 요청 시만 |

---

## 완료

대상 Test ID **PASS** + 회귀 **FAIL 0**(P0 또는 동 파일) 확인 후:

**다음:** 다음 Test ID RED → GREEN 반복, 또는 REFACTOR Phase (별도 Command·Skill).

**커밋 (선택):** 사용자가 요청할 때만 — 메시지에 Test ID 포함 (예: `green: VAL-01 — 음수 입력 거부`).
