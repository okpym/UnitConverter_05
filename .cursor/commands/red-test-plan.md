# RED Test Plan — C2C 설계표·테스트 플랜 (Ask)

**ARRR A단계 (Ask = RED ③)** 만 수행한다. C2C 설계표와 테스트 플랜 **문서 출력**만 한다.  
테스트 본문 작성·pytest 실행·GREEN/REFACTOR·프로덕션 수정은 하지 않는다.

| 연결 | 파일 |
|------|------|
| Rule | `.cursorrules` |
| SSOT (FR) | `docs/PRD.md` — 없으면 `README.md` 기본·품질 요구 + `Report/Step3_워크북.md` |
| Test ID | `tests/manifest.json` |
| RED 본문 (다음) | `/red-skeleton` |
| RED 실행 (이후) | `/tdd-red` · `@unit-converter-tdd` |

---

## 동작 조건

- **추가 인자 없이** `/red-test-plan` 만으로 동작한다.
- **세션 주제** · **대상 Test ID** 는 현재 채팅 맥락과 PRD FR에서 **자동 추출**한다.
- 한 번에 **Test ID 1개**만 설계한다 (`.cursorrules` TDD 원칙).
- PRD와 manifest가 충돌하면 **manifest Given/Then** 우선, FR 인용은 PRD에서만.

---

## 필수 선언 (응답 첫 줄)

```
Phase: red | Layer: entity | Track: Logic
```

| 필드 | 값 | 비고 |
|------|-----|------|
| Phase | `red` | 고정 |
| Layer | `entity` \| `boundary` | Track A(boundary)는 Layer만 `boundary`로 바꿔 동일 절차 재사용 |
| Track | `Logic` \| `UI` | UnitConverter P0 기본은 `Logic` · `entity` |

> **Track A (boundary):** 본 Command 출력 구조·4블록·금지 사항은 동일하다. 선언의 `Layer: boundary`만 바꾸면 재사용 가능하다 (Track·pytest Harness는 boundary 대상에 맞게 조정).

---

## 절차

1. `docs/PRD.md` — 대상 FR 인용 (없으면 README §기본·품질 요구).
2. `Report/Step3_워크북.md` — P0·하지 않을 것(§4) 확인.
3. `tests/manifest.json` — Test ID Given/Then·mom_test 확인.
4. 채팅·README 세션 주제에서 **현재 Test ID 1개** 확정.
5. 아래 **출력 4블록**을 표 형식으로 작성 (**파일 생성 없음**).
6. 마지막 줄: `/red-skeleton 으로 넘길 준비됐다`

---

## 출력 4블록 (필수 · 표 형식)

### 블록 1 — C2C (Rule1~3)

| Rule | 내용 |
|------|------|
| **Rule1 — FR 인용** | PRD FR ID·원문 인용 (예: `FR-VAL-01` …). PRD 없으면 README 항목 번호·원문 |
| **Rule2 — To-Do 1개** | 이번 RED에서 검증할 **행동 1문장** (구현·코드 작성 아님) |
| **Rule3 — Test ID G/W/T** | Given / When / Then (manifest 정합, When = 호출·입력 트리거) |

```markdown
### 1. C2C (Rule1~3)

| Rule | 내용 |
|------|------|
| Rule1 | FR-… — «PRD 원문» |
| Rule2 | … |
| Rule3 | **VAL-01** — Given: … / When: … / Then: … |
```

---

### 블록 2 — Track B 표 (Logic · entity 기본)

| 열 | 설명 |
|----|------|
| Test ID | manifest ID |
| 대상 함수 | 프로덕션·테스트에서 호출할 함수/진입점 (예: `main`, 추후 `parse_input`) |
| Given→Then | manifest Given에서 Then까지 한 줄 흐름 |
| Invariant | RED 중에도 **변하지 않아야 하는** 관찰 (예: 변환 줄 미출력, 메시지 키워드) |
| Expected RED Failure | pytest FAIL 예상 유형 (AssertionError 메시지·누락 assert 등) |

```markdown
### 2. Track B

| Test ID | 대상 함수 | Given→Then | Invariant | Expected RED Failure |
|---------|-----------|------------|-----------|----------------------|
| VAL-01 | `main()` | meter:-1 → 음수 거부 | feet/yard 변환 줄 0건 | AssertionError: 변환 결과 출력 |
```

---

### 블록 3 — 테스트 플랜

| 항목 | 작성 내용 |
|------|-----------|
| 파일 경로 | `tests/test_converter.py` (또는 분리 파일명 **계획만**) |
| 함수명 | `test_<ID>_…` 네이밍 |
| conftest 픽스처 | `monkeypatch`, `capsys`, `manifest` 등 사용 계획 |
| pytest 명령 | `pytest -k "<Test ID>" -v` |
| RED 묶음 범위 | parametrize id·마커(`@pytest.mark.val` 등) · 이번 ID만 |

```markdown
### 3. 테스트 플랜

| 항목 | 값 |
|------|-----|
| 파일 | `tests/test_converter.py` |
| 함수 | `test_VAL_01_negative_input_rejected` |
| conftest | `monkeypatch`(input), `capsys` |
| pytest | `pytest -k VAL-01 -v` |
| RED 묶음 | `@pytest.mark.val`, parametrize id=`VAL-01`, P0 only |
```

---

### 블록 4 — ECB·Mock 점검

| Track | 점검 |
|-------|------|
| **Logic Track** | **Domain Mock 금지** — 변환 비율·단위 테이블을 Mock으로 대체하지 않음 |
| **공통** | **E001~E005 emit 금지** — 테스트·플랜에 ECB 에러 코드 출력 시나리오 넣지 않음 |
| boundary / UI | stdin·stdout 관찰 위주; 외부 I/O Mock은 Harness(`monkeypatch`)만 |

```markdown
### 4. ECB·Mock 점검

| 항목 | 판정 | 비고 |
|------|------|------|
| Domain Mock | ❌ 금지 | Logic Track — 실제 `main`/도메인 경로 |
| E001~E005 emit | ❌ 금지 | RED 플랜에 포함 안 함 |
| Harness Mock | ✅ 허용 | `builtins.input` monkeypatch 등 |
```

---

## 금지

| 금지 | 이유 |
|------|------|
| `src/` · `UnitConverter.py` · 프로덕션 코드 **수정** | Ask 단계 — 설계만 |
| `tests/` · `src/` **파일 생성·수정** | `/red-skeleton` · `/tdd-red` 담당 |
| GREEN / REFACTOR | RED ③ 설계 전용 |
| `pytest.skip()` · `xfail` · assert 완화 제안 | RED 우회 |
| Domain Mock (Logic Track) | ECB·Track B Invariant 위반 |
| E001~E005 emit 시나리오 | 본 Phase 범위 밖 |

---

## 완료

응답 **마지막 줄** (고정):

```
/red-skeleton 으로 넘길 준비됐다
```

**다음:** `/red-skeleton` — skeleton·AAA 본문 작성 (여전히 GREEN·프로덕션 수정 금지).
