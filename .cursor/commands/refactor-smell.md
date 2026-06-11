# Refactor Smell — 코드 스멜 탐지 (Refine)

**ARRR R단계 (Refine = ⑦)** 만 수행한다.  
`src/` · `tests/` 코드에서 **스멜을 탐지·분류**한다. **수정·commit 금지.**

| 연결 | 파일 |
|------|------|
| Rule | `.cursorrules` |
| SSOT (FR) | `docs/PRD.md` |
| Test Loop | `tests/manifest.json`, `pytest` |
| Skill | `@magic-square-tdd` — **있으면 자동 따름** |
| Skill (본 repo) | `@unit-converter-tdd` — magic-square-tdd 없을 때 |
| REFACTOR 실행 (다음) | `/refactor-safe` |

> **magic-square-tdd Skill이 있으면 자동 따름.**  
> UnitConverter repo: 프로덕션 `UnitConverter.py` (및 분리 모듈) = `src/` 동일 취급.

---

## 동작 조건

- **추가 인자 없이** `/refactor-smell` 만으로 동작.
- **코드 수정·commit·push 금지** — 분석·표 출력만.
- 스멜 후보는 **Change Budget** 이내로 `/refactor-safe`에 넘길 **1~3개**만 선정.

---

## 필수 선언 (응답 첫 줄)

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI
```

| 필드 | 값 |
|------|-----|
| Phase | `refactor` |
| Scope | `src/` · `tests/` (탐지 범위) |
| Track | `Logic+UI` |

---

## 전제 (게이트)

**전체 테스트 PASS 필수.** FAIL이면 **즉시 중단** — 스멜 분석하지 않음.

```bash
python -m pytest tests/ -v
```

| 결과 | 조치 |
|------|------|
| 전부 PASS | 스멜 탐지 진행 |
| 1건 이상 FAIL | 중단 — GREEN·Golden 선행, 스멜 표 출력 금지 |

---

## 절차

1. `python -m pytest tests/ -v` 실행 → **전부 PASS** 확인 (아니면 중단 보고).
2. `src/` · `tests/` (및 `UnitConverter.py`) 정적 읽기 — **수정 없음**.
3. 스멜 유형별 탐지 (아래 §스멜 유형).
4. **Change Budget** 초과 리팩터는 후보에서 제외·P2로 강등.
5. **스멜 표** + **`/refactor-safe` 후보 1~3개** 출력.
6. 다음 안내: **P0 1개만** 골라 `/refactor-safe` 실행.

---

## 스멜 유형 (탐지 기준)

| 유형 | 탐지 힌트 |
|------|-----------|
| **Long Method** | 한 함수·메서드 40줄↑ 또는 책임 2개↑ (`main()` 등) |
| **Duplicated Code** | 동일·유사 블록 2회↑ (검증·변환·출력) |
| **Mysterious Name** | `x`, `v`, `tmp`, 도메인 비매칭 식별자 |
| **Magic Number** | `3.28084`, `1.09361`, `34`, `16` 등 constants SSOT 미사용 |
| **ECB 위반** | entity → boundary/control import; E001~E005 emit |
| **Feature Envy** | 한 클래스가 타 객체 데이터만 조작 (출력·파싱 혼재) |

### 우선순위

| 등급 | 기준 |
|------|------|
| **P0** | 테스트·FR 위험, ECB 위반, Magic Number SSOT |
| **P1** | Duplicated Code, Long Method (Budget 내) |
| **P2** | Mysterious Name, Feature Envy (동작 불변·선택) |

---

## Change Budget (`/refactor-safe` 1회 상한)

| 항목 | 상한 |
|------|------|
| 파일 | **≤ 3** |
| 클래스 | **≤ 1** |
| 메서드 | **≤ 3** |

Budget 초과 스멜 → 표에는 기록하되 **후보 제외** 또는 분할 제안(P2).

---

## 출력 (필수)

### 1. 스멜 표

```markdown
### 스멜 표

| P | 유형 | 위치 | 요약 | Budget |
|---|------|------|------|--------|
| P0 | Magic Number | UnitConverter.py L35-36 | 3.28084 리터럴 | ✅ 파일1·메서드1 |
| P1 | Long Method | UnitConverter.py main | 파싱+변환+출력 | ✅ 파일1·메서드1 |
| P2 | Mysterious Name | … | … | ⚠️ 후보 외 |
```

| 열 | 설명 |
|----|------|
| P | P0 / P1 / P2 |
| 유형 | Long Method · Duplicated Code · Mysterious Name · Magic Number · ECB 위반 · Feature Envy |
| 위치 | `파일:줄` 또는 `클래스.메서드` |
| 요약 | 1문장 |
| Budget | ✅ `/refactor-safe` 1회 이내 / ⚠️ 초과 |

### 2. `/refactor-safe` 후보 (1~3개)

```markdown
### refactor-safe 후보

| # | P | 대상 | 기대 효과 | Budget |
|---|-----|------|-----------|--------|
| 1 | P0 | Magic Number → constants | SSOT·FR-NFR | 파일1 |
| 2 | P1 | main 분리 (parse) | SRP | 파일2·메서드2 |
```

---

## 금지

| 금지 | 이유 |
|------|------|
| **코드 수정** (src/ · tests/) | Refine ⑦ — 탐지만 |
| **`git commit` / `push`** | 사용자 요청·`/refactor-safe` 담당 |
| pytest FAIL 상태에서 스멜 표 | 전제 위반 |
| Budget 초과를 P0 후보로 제시 | `/refactor-safe` 실패 유발 |
| assert 완화·테스트 삭제 제안 | REFACTOR 우회 |

---

## 보고 · 다음 단계

```markdown
## Refactor Smell 보고
- Phase: refactor | Scope: src/ tests/ | Track: Logic+UI
- pytest: `python -m pytest tests/ -v` → N passed, 0 failed
- 스멜: P0 …건 · P1 …건 · P2 …건
- refactor-safe 후보: #1 …, #2 …
- 변경: 없음 (탐지만)
```

**다음 (고정 안내):**

> **P0 후보 1개만** 골라 `/refactor-safe` 실행.  
> (예: 후보 #1 Magic Number → constants SSOT)

---

## 완료

스멜 표 + 후보 1~3개 출력 후 **코드·commit 변경 없이** 종료.

**다음:** `/refactor-safe` — P0 1개·Change Budget 준수·pytest PASS 유지.
