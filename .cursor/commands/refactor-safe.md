# Refactor Safe — 스멜 1개 Safe Refactor (Refine)

**ARRR R단계 (Refine = ⑧)** — `/refactor-smell` **표에서 선택한 스멜 1개만** Safe Refactor 실행.  
**동작·관찰 불변** — 구조·이름·SSOT 정리만. 기능 추가·버그 수정은 **별도 GREEN**.

| 연결 | 파일 |
|------|------|
| Rule | `.cursorrules` |
| SSOT (FR) | `docs/PRD.md` |
| 스멜 (앞단) | `/refactor-smell` → `.cursor/commands/refactor-smell.md` |
| Golden | `tests/_approval.py`, `tests/golden/*.approved.txt` |
| Skill | `@magic-square-tdd` — **있으면 자동 따름** |
| Skill (본 repo) | `@unit-converter-tdd` — magic-square-tdd 없을 때 |

> **magic-square-tdd Skill이 있으면 자동 따름.**  
> UnitConverter repo: `UnitConverter.py` = `src/` 동일 취급.

---

## 동작 조건

- **스멜 1개** — 직전 `/refactor-smell` 후보 **#N 1개** 또는 채팅에서 명시한 표 행 1개.
- **Change Budget** 필수 준수 (초과 시 분할·중단).
- **기능 추가·버그 수정 금지** — 새 FR·미통과 테스트 해결은 `/green-minimal`.
- `git commit` / `push`: **사용자 명시 요청 시만**.

---

## 필수 선언 (응답 첫 줄)

```
Phase: refactor | Layer: entity | Track: Logic
```

| 필드 | 값 |
|------|-----|
| Phase | `refactor` |
| Layer | `entity` \| `boundary` |
| Track | `Logic` \| `UI` |

---

## 전제 (게이트)

```bash
python -m pytest tests/ -v
```

| 결과 | 조치 |
|------|------|
| 전부 PASS | Refactor 진행 |
| FAIL | 중단 — GREEN·Golden 선행 |

직전 `/refactor-smell` 후보의 **Budget ✅** 행만 실행. ⚠️ 초과 행은 **거부**.

---

## Change Budget (1회 상한)

| 항목 | 상한 |
|------|------|
| 파일 | **≤ 3** |
| 클래스 | **≤ 1** |
| 메서드 | **≤ 3** |

리팩터 전·후 변경 파일·추출 메서드 수를 보고에 기록.

---

## 절차

1. **대상 스멜 확정** — smell 표 행 1개 (유형·위치·#번호).
2. **Budget 검증** — 파일·클래스·메서드 상한 확인.
3. **Safe Refactor** — 동작 불변 리팩터만 (extract constant · rename · extract method · dedupe).
4. **pytest 전체**
   ```bash
   python -m pytest tests/ -v
   ```
5. **Golden matched** — `UPDATE_GOLDEN` **unset**
   ```bash
   python -m pytest tests/ -k golden -v
   # 또는 tests/test_converter.py::test_VAL_01_golden_stdout_approval 등 대상 golden 테스트
   ```
6. **Golden diff 처리** (아래 §Golden).
7. **Refactor Safe 보고**.

---

## Safe Refactor 허용 · 금지

| 허용 | 금지 |
|------|------|
| Magic Number → `entity/constants.py` import | 새 기능·새 Test ID 동시 해결 |
| `main()` → private helper 1~3개 extract | assert 완화·삭제·skip/xfail |
| 중복 블록 → 함수 추출 (동일 출력) | ECB: entity→boundary/control import |
| 식별자 rename (의미 동일) | E001~E005 emit 추가 |
| 테스트·prod 동일 상수 SSOT | golden 파일 **수동 편집**으로 통과 |

### 예시 (후보 #1 P0 Magic Number)

```python
# entity/constants.py
METER_TO_FEET = 3.28084
METER_TO_YARD = 1.09361

# UnitConverter.py
from entity.constants import METER_TO_FEET, METER_TO_YARD
```

---

## Golden diff 처리

Refactor 후 `@pytest.mark.golden` 또는 `assert_matches_golden` 테스트 실행.

| 상황 | 조치 |
|------|------|
| **matched** (PASS, env 없음) | 완료 |
| **diff · 의도적** (출력 포맷·직렬화 정책 변경이 리팩터 목적) | **ISS 문서화** (`Report/` 또는 PRD 부록 1문단) → `UPDATE_GOLDEN=1` 재생성 → matched 재검증 |
| **diff · 비의도** | **롤백** — 리팩터 변경 되돌림 → pytest PASS 복구 |

```bash
# 의도적 golden 갱신 (ISS 기록 후)
$env:UPDATE_GOLDEN=1; python -m pytest tests/ -k golden -v
Remove-Item Env:UPDATE_GOLDEN -ErrorAction SilentlyContinue
python -m pytest tests/ -k golden -v
```

**금지:** ISS 없이 `UPDATE_GOLDEN=1` · golden 수동 편집.

---

## 보고 템플릿

```markdown
## Refactor Safe 보고
- Phase: refactor | Layer: entity | Track: Logic
- 스멜: #1 P0 Magic Number → constants SSOT
- Budget: 파일 3 · 클래스 0 · 메서드 0 (≤3/≤1/≤3)
- 변경 요약: entity/constants.py METER_* 추가; UnitConverter·test_converter import
- pytest: `python -m pytest tests/ -v` → 8 passed, 0 failed
- golden matched: ✅ (`test_VAL_01_golden_stdout_approval`, UPDATE_GOLDEN unset)
- golden diff: 없음 (또는 의도적 → ISS: Report/… · UPDATE_GOLDEN 후 matched)
- commit: (사용자 요청 시만)
```

| 보고 항목 | 내용 |
|-----------|------|
| 변경 요약 | 스멜 1개에 대한 diff 1~3문장 |
| pytest | `tests/` 전체 passed/failed |
| golden matched | PASS/FAIL · 대상 golden 경로 |

---

## 금지

| 금지 | 이유 |
|------|------|
| 스멜 **2개 이상** 동시 해결 | 1 safe = 1 smell |
| Budget 초과 | refactor-smell 약속 |
| 기능 추가·버그 수정 | GREEN 담당 |
| assert 완화·테스트 삭제 | REFACTOR 우회 |
| 비의도 golden diff 방치 | 롤백 필수 |
| ISS 없는 UPDATE_GOLDEN | Golden 거버넌스 |

---

## 완료

`pytest tests/` **전부 PASS** + golden **matched** 확인 후:

**다음:** `/refactor-smell` 재실행 (남은 스멜) 또는 다음 Test ID TDD 사이클.

**파이프라인:**

```
/refactor-smell (탐지) → /refactor-safe (스멜 1개) → pytest + golden → (반복)
```
