# Product Requirements Document — Unit Converter

| 항목 | 값 |
|------|-----|
| **프로젝트** | UnitConverter_05 |
| **버전** | 0.1 (P0 초안) |
| **일자** | 2026-06-11 |
| **상태** | P0 TDD 진행 중 |
| **프로덕션** | `UnitConverter.py` |
| **Test ID SSOT** | `tests/manifest.json` |

---

## 1. 목적

사용자가 `단위:값` 형식으로 길이를 입력하면, 등록된 모든 단위로 변환 결과를 출력하는 CLI 프로그램을 제공한다.  
본 PRD는 **기능 요구(FR)** 의 단일 출처(SSOT)이며, `/red-test-plan` C2C Rule1 FR 인용·TDD Test ID 추적의 기준 문서이다.

### 1.1 문제 정의 (Mom Test · Step3)

학습자는 README의 품질·테스트 요구를 한 번에 구현하려다 요구 해석·재확인에 시간을 쓴다. 본 프로젝트는 README P0를 **Test ID 단위**로 쪼개 RED→GREEN마다 pytest로 검증하는 방식을 우선 고정한다.  
(상세: [`Report/Step3_워크북.md`](../Report/Step3_워크북.md))

### 1.2 문서 우선순위

| 충돌 시 | 우선 문서 |
|---------|-----------|
| FR·Acceptance vs TDD Given/Then | **`tests/manifest.json`** (실행 가능한 검증 문장) |
| README vs Step3 워크북 | **Step3 워크북** (`.cursorrules`) |
| FR 원문·범위·우선순위 | **본 PRD** |

---

## 2. 범위

### 2.1 P0 (이번 Phase — 필수)

| 영역 | FR ID | Test ID |
|------|-------|---------|
| 입력 검증 | FR-VAL-01 ~ FR-VAL-03 | VAL-01 ~ VAL-03 |
| 단위 변환 | FR-CONV-01 ~ FR-CONV-03 | CONV-01 ~ CONV-03 |

### 2.2 P1 · 연기 (본 PRD 등재, 구현·TC 별도 Phase)

| 영역 | FR ID | 비고 |
|------|-------|------|
| 설계 품질 | FR-NFR-01 ~ FR-NFR-02 | OCP · SRP — REFACTOR Phase |
| 설정 외부화 | FR-EXT-01 | units.json 등 |
| 동적 단위 등록 | FR-EXT-02 | cubit 예시 |
| 출력 포맷 | FR-EXT-03 | JSON / CSV / 표 |

Step3 워크북 §4 **하지 않을 것**과 동일: cubit·설정 외부화·JSON/CSV는 P0 범위 밖.

---

## 3. 용어 · 입력·출력 규약

### 3.1 입력 형식

- 패턴: `{unit}:{value}`
- 예: `meter:2.5`, `feet:10`
- `unit`: 등록된 단위 식별자 (문자열, P0는 `meter` | `feet` | `yard`)
- `value`: 0 이상의 실수 (음수 불가)

### 3.2 출력 형식 (P0)

입력 `{value} {unit}` 기준, **세 줄** 고정:

```
{value} {unit} = {x} meter
{value} {unit} = {y} feet
{value} {unit} = {z} yard
```

- README 예시 (`meter:2.5`): feet ≈ **8.2**, yard ≈ **2.7** (표시 반올림은 구현 정책 — CONV-03에서 ±0.1 검증)
- P0는 **표 형·JSON·CSV 출력 선택 없음**

### 3.3 변환 상수 (meter 기준)

| 관계 | 값 |
|------|-----|
| 1 meter | 3.28084 feet |
| 1 meter | 1.09361 yard |
| feet ↔ yard | meter 환산 후 상호 변환 |

### 3.4 사용자 메시지 (P0)

| 상황 | stdout 메시지 (키워드) |
|------|------------------------|
| 형식 오류 | `Invalid format` |
| 숫자 파싱 실패 | `Invalid number` |
| 음수 | `Negative value` |
| 미등록 단위 | `Unknown unit` |

> **ECB:** P0 테스트·플랜에서 **E001~E005 에러 코드 emit 금지** (`/red-test-plan` 블록 4). 사용자 메시지는 위 키워드 문자열로 충분하다.

---

## 4. 기능 요구 (FR)

### 4.1 입력 검증

#### FR-VAL-01 — 음수 입력 거부

| 항목 | 내용 |
|------|------|
| **우선순위** | P0 |
| **Test ID** | VAL-01 |
| **요구** | `value`가 0 미만이면 변환을 수행하지 않고 거부한다. |
| **Acceptance** | Given `meter:-1` → Then 변환 결과(feet/yard 줄) **미출력**, 거부 메시지 또는 non-zero exit. |
| **Mom Test** | `feet:-3` 캡처만 — main 미연결 |

#### FR-VAL-02 — 입력 형식 검증

| 항목 | 내용 |
|------|------|
| **우선순위** | P0 |
| **Test ID** | VAL-02 |
| **요구** | `unit:value` 형식이 아니거나 unit/value가 비어 있으면 거부한다. |
| **Acceptance** | Given `meter`, `abc`, `meter:`, `:2.5` → Then stdout에 **`Invalid format`** 포함, 변환 미출력. |
| **Mom Test** | README 입력 형식 검증 |

#### FR-VAL-03 — 미등록 단위 거부

| 항목 | 내용 |
|------|------|
| **우선순위** | P0 |
| **Test ID** | VAL-03 |
| **요구** | P0 등록 단위(`meter`, `feet`, `yard`) 외 입력은 거부한다. |
| **Acceptance** | Given `metre:2.5` → Then stdout에 **`Unknown unit`** 포함, 변환 미출력. |
| **Mom Test** | 오타 단위 metre 시나리오 |

---

### 4.2 단위 변환

#### FR-CONV-01 — meter 입력 시 전 단위 출력

| 항목 | 내용 |
|------|------|
| **우선순위** | P0 |
| **Test ID** | CONV-01 |
| **요구** | 유효한 `meter:{value}` 입력 시 meter·feet·yard 변환 결과를 **각 1줄씩** 출력한다. |
| **Acceptance** | Given `meter:2.5` → Then stdout **3줄**, 각각 `meter` / `feet` / `yard` 단위로 끝남. |
| **Mom Test** | 스타터 실행 확인 |

#### FR-CONV-02 — 비-meter 입력 · meter 기준 역변환

| 항목 | 내용 |
|------|------|
| **우선순위** | P0 |
| **Test ID** | CONV-02 |
| **요구** | `feet` 또는 `yard` 입력 시 meter로 환산한 뒤 세 단위 결과를 출력한다. |
| **Acceptance** | Given `feet:10` → Then 3줄 출력; meter 줄 값은 `10 / 3.28084` 와 ±0.001 이내. |
| **Mom Test** | 계산기 대조 행동 |

#### FR-CONV-03 — Golden 예시 (README)

| 항목 | 내용 |
|------|------|
| **우선순위** | P0 |
| **Test ID** | CONV-03 |
| **요구** | README 예시 `meter:2.5` → feet 표시값이 **8.2에 ±0.1** 이내. |
| **Acceptance** | Given `meter:2.5` → Then feet 줄 파싱값 ∈ [8.1, 8.3]. |
| **Mom Test** | yard:1 vs README 2.7 반올림 불안 |

---

## 5. 비기능 · 확장 요구 (P1+)

### FR-NFR-01 — OCP

새 단위 추가 시 기존 변환·검증 코드 변경을 최소화할 수 있는 확장 지점을 둔다. (REFACTOR Phase)

### FR-NFR-02 — SRP

입력 파싱·검증·변환·출력 책임을 분리한 클래스 구성을 목표로 한다. (REFACTOR Phase)

### FR-EXT-01 — 설정 외부화

변환 비율을 JSON/YAML 등 외부 설정에서 로드한다.

### FR-EXT-02 — 동적 단위 등록

런타임에 `1 cubit = 0.4572 meter` 형태로 단위·비율을 등록·사용한다.

### FR-EXT-03 — 출력 포맷 선택

JSON / CSV / 표 형태 출력을 선택할 수 있다.

---

## 6. 추적 매트릭스 (FR ↔ Test ID)

| FR ID | Test ID | Priority | Given (manifest) | Then (manifest) |
|-------|---------|----------|------------------|-----------------|
| FR-VAL-01 | VAL-01 | P0 | `meter:-1` | 음수 거부 |
| FR-VAL-02 | VAL-02 | P0 | `meter` / `abc` / `meter:` / `:2.5` | Invalid format |
| FR-VAL-03 | VAL-03 | P0 | `metre:2.5` | Unknown unit |
| FR-CONV-01 | CONV-01 | P0 | `meter:2.5` | meter/feet/yard 3줄 |
| FR-CONV-02 | CONV-02 | P0 | `feet:10` | meter 역변환 |
| FR-CONV-03 | CONV-03 | P0 | `meter:2.5` | feet ≈ 8.2 (±0.1) |

---

## 7. TDD · 검증 정책

| 정책 | 내용 |
|------|------|
| Phase | RED → GREEN → REFACTOR, **Test ID 1개씩** |
| RED 게이트 | `pytest -k "<Test ID>" -v` → FAIL |
| P0 회귀 | `pytest -m p0 -v` |
| Logic Track | Domain Mock 금지 — 실제 `main()` 경로 관찰 |
| Harness | `monkeypatch`(`builtins.input`), `capsys` 허용 |

Rule: [`.cursorrules`](../.cursorrules) · Command: `/tdd-red`, `/red-test-plan` · Skill: `@unit-converter-tdd`

---

## 8. 참고 문서

| 문서 | 경로 | 역할 |
|------|------|------|
| README | [`README.md`](../README.md) | 과제 개요·실행 방법 |
| Step3 워크북 | [`Report/Step3_워크북.md`](../Report/Step3_워크북.md) | R-G-I-O · 범위 · 성공 기준 |
| Test manifest | [`tests/manifest.json`](../tests/manifest.json) | Given/Then · Mom Test |
| 스타터 | [`UnitConverter.py`](../UnitConverter.py) | 현재 구현 기준선 |
| Mom Test 인터뷰 | [`Report/Step1_MomTest_인터뷰_보고서.md`](../Report/Step1_MomTest_인터뷰_보고서.md) | 별도 페르소나 (P0 FR 아님) |

---

## 9. 변경 이력

| 버전 | 일자 | 변경 |
|------|------|------|
| 0.1 | 2026-06-11 | 초안 — README P0 · manifest 6건 FR 정식화 |
