# Unit Converter — Product Requirements Document (PRD)

- **프로젝트:** Unit Converter (`UnitConverter_05`)
- **버전:** 1.0
- **일자:** 2026-06-11
- **역할:** 기능 요구(FR) SSOT — Test ID·TDD·Refactor Command가 인용하는 원문
- **충돌 우선순위:** Given/Then 세부는 `tests/manifest.json` 우선 · FR 원문 인용은 본 문서

---

## 1. 개요

사용자가 `단위:값` 형식(예: `meter:2.5`)으로 길이를 입력하면, 등록된 모든 단위로 변환한 결과를 한 번에 출력하는 CLI 프로그램이다.

본 PRD는 README 기본·품질·추가 요구와 Mom Test·Step3~6 보고서를 통합한 **기능 요구의 단일 출처(SSOT)** 이다.

---

## 2. 문제 정의

### 2.1 표면 문제 (잘못된 정의)

> meter/feet/yard를 한 번에 변환해 주는 Unit Converter 프로그램을 만든다.

### 2.2 진짜 문제

| 출처 | 한 문장 | 증거 |
|------|---------|------|
| **Step1 인터뷰** (inch↔cm 시나리오) | 한 단위로만 적힌 길이를 내 단위와 비교하려면 계산기·메모·화면을 오가며 **8~10분** 재계산·재검산이 필요하고, 반올림 때문에 판정 확신이 어렵다. | 23.6 inch → 59.944 cm, 저녁 재검산 3분 |
| **Step3 시뮬레이션** (학습자 페르소나) | README의 품질·테스트 요구를 실행 가능한 작업으로 쪼개지 못해 초안·캡처·외부 검색에 **~4시간**을 쓰고, 제출 직전 테스트·출력 포맷 불안으로 확장 요구를 손대지 않는다. | `feet:-3` 캡처만, assert 원복 |

### 2.3 제품 가치 제안

1. **한 번 입력 → 관련 단위 동시 출력** — 단계별 계산기·메모 반복을 줄인다.
2. **검증 가능한 요구 분해** — README 항목을 Test ID 단위로 쪼개 RED→GREEN마다 pytest로 즉시 확인한다.
3. **확장 여지** — 새 단위·설정 외부화·출력 포맷은 OCP를 만족하는 구조로 단계적 추가한다.

---

## 3. 사용자 · 범위

### 3.1 페르소나

| ID | 설명 | 핵심 니즈 |
|----|------|-----------|
| **P-USER** | 일상에서 단위 변환이 필요한 사용자 (해외 쇼핑·가구 배치 등) | 한 입력으로 여러 단위 비교, 반올림 불안 감소 |
| **P-DEV** | Python 입문 과제를 수행하는 학습자 | 요구 해석 비용 감소, 테스트로 회귀 방지 |

### 3.2 이번 릴리스 범위 (P0)

- 입력 형식 `unit:value` 파싱
- meter / feet / yard 상호 변환
- 음수·형식 오류·미등록 단위 검증
- pytest 기반 Test ID(CONV-01~03, VAL-01~03) 전부 통과

### 3.3 범위 밖 (P1 · deferred)

Step3 워크북 §4 · `manifest.json` deferred와 동일:

| 항목 | 사유 |
|------|------|
| cubit 등 동적 단위 등록 | 설계 문맹 구간 — 별도 Phase |
| 설정 외부화 (JSON/YAML) | P0 검증 루프 선행 |
| JSON / CSV / 표 형태 출력 선택 | 반올림·예시 불일치가 우선 — 포맷 확장은 검증 면적만 증가 |
| Step1 inch↔cm 시나리오를 그대로 FR로 구현 | 별개 페르소나 — P0는 README `meter:2.5` 기준 |
| boundary/entity 완전 레이어 분리 | Refactor Budget 초과 — 별도 Phase |

---

## 4. 기능 요구 (FR)

### 4.1 입력 검증 — FR-VAL

| FR ID | 원문 (SHALL) | Test ID | Given (manifest) | Then (manifest) |
|-------|--------------|---------|------------------|-------------------|
| **FR-VAL-01** | value가 0 미만이면 변환을 수행하지 않고 거부한다. | VAL-01 | `meter:-1` | 음수 거부 (에러 메시지 또는 변환 미출력) |
| **FR-VAL-02** | `unit:value` 형식이 아니거나 unit·value가 비어 있으면 Invalid format 안내 후 종료한다. | VAL-02 | `meter`, `abc`, `meter:`, `:2.5` | Invalid format 안내 |
| **FR-VAL-03** | 등록되지 않은 단위면 Unknown unit 안내 후 종료한다. | VAL-03 | `metre:2.5` | Unknown unit 안내 |

### 4.2 단위 변환 — FR-CONV

| FR ID | 원문 (SHALL) | Test ID | Given | Then |
|-------|--------------|---------|-------|------|
| **FR-CONV-01** | 유효한 meter 입력 시 meter·feet·yard 세 줄을 출력한다. | CONV-01 | `meter:2.5` | meter, feet, yard 세 줄 출력 |
| **FR-CONV-02** | feet 입력 시 meter 기준으로 역변환한 뒤 타 단위를 출력한다. | CONV-02 | `feet:10` | meter 기준 역변환 후 타 단위 출력 |
| **FR-CONV-03** | meter→feet 변환 결과가 README 예시(2.5 meter → feet ≈ 8.2)와 ±0.1 이내로 일치한다. | CONV-03 | `meter:2.5` | feet ≈ 8.2 (±0.1) |

### 4.3 입출력 형식 — FR-IO

| FR ID | 원문 |
|-------|------|
| **FR-IO-01** | 입력 프롬프트: `Insert value for converting (ex: meter:2.5): ` |
| **FR-IO-02** | 출력 형식: `{value} {unit} = {converted} {target_unit}` (줄 단위, 소수 표현은 float 기본) |
| **FR-IO-03** | 예시 — 입력 `meter:2.5` 시 최소 다음과 동등한 정보를 출력한다: `2.5 meter = 8.2 feet`, `2.5 meter = 2.7 yard` (CONV-03은 수치 허용 오차로 검증) |

### 4.4 지원 단위 (P0)

| 단위 | 비고 |
|------|------|
| meter | 기준 단위 |
| feet | |
| yard | |

### 4.5 추가 요구 (P1 · deferred) — FR-EXT

| FR ID | 원문 (SHALL) | 비고 |
|-------|--------------|------|
| **FR-EXT-01** | 변환 비율을 외부 설정 파일(JSON/YAML)에서 로드한다. | README 추가 요구 |
| **FR-EXT-02** | 런타임에 `1 cubit = 0.4572 meter`처럼 단위와 비율을 등록할 수 있다. | OCP — 기존 코드 최소 변경 |
| **FR-EXT-03** | 출력을 JSON / CSV / 표 형태 중 선택할 수 있다. | README 추가 요구 |

---

## 5. 비기능 요구 (NFR)

| NFR ID | 원문 | 검증 |
|--------|------|------|
| **NFR-OCP** | 새 단위 추가 시 기존 변환·검증 로직의 수정을 최소화한다 (Open-Closed). | P1 FR-EXT-02 · 코드 리뷰 |
| **NFR-SRP** | 입력 파싱·검증·변환·출력 책임을 분리한다 (Single Responsibility). | Step6 helper 추출 · 추가 Refactor |
| **NFR-CONSTANTS** | 변환 상수는 단일 SSOT(`entity/constants.py`)에서 관리한다. | Step6 #1 완료 |
| **NFR-TEST** | 각 FR은 Test ID와 1:1 추적 가능하며, P0는 `pytest -m p0`로 회귀 검증한다. | manifest · test_converter.py |
| **NFR-TDD** | RED → GREEN → REFACTOR 순서를 지키며, RED 없이 GREEN 구현을 금지한다. | `.cursorrules` |
| **NFR-GOLDEN** | 승인된 stdout 스냅샷(golden) 변경 시 의도적 변경만 허용한다. | `tests/golden/`, `_approval.py` |

---

## 6. 비즈니스 규칙 · 도메인 상수

### 6.1 변환 비율 (meter 기준)

| 상수 | 값 | 출처 |
|------|-----|------|
| `METER_TO_FEET` | 3.28084 | README · `entity/constants.py` |
| `METER_TO_YARD` | 1.09361 | README · `entity/constants.py` |

### 6.2 계산 규칙

- feet·yard 간 비율은 **meter를 중간 기준**으로 계산한다.
- 입력 단위가 feet/yard이면 `meter_value = input / METER_TO_*` 로 역산 후 타 단위로 변환한다.

---

## 7. 성공 기준

### 7.1 제품 성공 (Mom Test · 사용자 가치)

| ID | 기준 | 측정 방법 | Mom Test 연결 |
|----|------|-----------|---------------|
| **PSC-1** | 유효 입력 1회로 meter·feet·yard 결과를 **동시에** 확인할 수 있다. | `meter:2.5` 실행 → 3줄 출력 (CONV-01) | 인터뷰: 단계별 계산·메모 반복 감소 |
| **PSC-2** | 잘못된 입력(음수·형식·미등록 단위) 시 변환 결과가 출력되지 않고 안내 메시지가 나온다. | VAL-01~03 pytest PASS | 시뮬: `feet:-3` 캡처만 → 실제 거부 |
| **PSC-3** | README 예시 수치(2.5 m → feet ≈ 8.2)와 ±0.1 이내로 일치한다. | CONV-03 pytest PASS | 반올림 불안 — 수치 허용 오차로 확신 |

### 7.2 P0 납품 성공 (기능 · 테스트)

| ID | 기준 | 검증 방법 | 상태 |
|----|------|-----------|------|
| **DSC-1** | P0 Test ID 6개(CONV-01~03, VAL-01~03)가 manifest에 등록되어 있다. | `tests/manifest.json` | ✅ |
| **DSC-2** | `pytest -m p0 -v` — failed 0, skipped 0 | Step4 보고: 9 passed | ✅ |
| **DSC-3** | Golden Master(VAL-01 stdout) 승인 스냅샷과 일치한다. | `pytest -k golden` | ✅ |
| **DSC-4** | 변환 상수가 prod/test 이중 정의 없이 `entity/constants.py` SSOT를 사용한다. | Step6 #1 | ✅ |

### 7.3 프로세스 성공 (Step3 워크북 SC)

| ID | 기준 | Mom Test 증거 연결 | 검증 방법 | 상태 |
|----|------|-------------------|-----------|------|
| **SC-1** | README P0가 Test ID 1:1로 manifest에 등록되어 할 일 목록이 보인다. | 4시간 요구 해석 → Test ID 분해 | manifest 6 ID | ✅ |
| **SC-2** | 음수·형식·미등록 단위 RED 골격 + Rule "RED 없이 GREEN 금지" | `feet:-3` 캡처만 → VAL RED | `.cursorrules` · VAL 테스트 | ✅ |
| **SC-3** | TDD Phase마다 pytest 실행·보고가 정의되어 assert 원복 패턴을 선행 검증한다. | 테스트 1개·포맷 불안 원복 | Skill Test Loop · Step4 기록 | ✅ |

### 7.4 품질 · Refactor 성공 (Step6)

| ID | 기준 | 검증 방법 | 상태 |
|----|------|-----------|------|
| **QSC-1** | Magic Number 스멜 해소 — 상수 SSOT | `entity/constants.py` | ✅ |
| **QSC-2** | `main()` Long Method 완화 — 파싱·변환·출력 helper 추출 | `_parse_unit_value`, `_to_meter_value`, `_print_conversions` | ✅ |
| **QSC-3** | Refactor 후 전체 pytest + golden matched | Step6: 10 passed | ✅ |
| **QSC-4** | 남은 P1 스멜(테스트 Act 중복 등)은 다음 `/refactor-safe`에서 처리 | Step6 §6 | ⬜ |

### 7.5 P1 완료 시 성공 기준 (미착수 · 목표)

| ID | 기준 | FR |
|----|------|-----|
| **P1SC-1** | `units.json`(또는 동등 설정)만 수정해 비율 변경 가능, 코드 재컴파일 없음 | FR-EXT-01 |
| **P1SC-2** | `cubit:1` 등록 후 즉시 변환 가능, 기존 단위 테스트 회귀 0 | FR-EXT-02 |
| **P1SC-3** | JSON/CSV/표 출력 선택 시 P0 golden·수치 검증 유지 | FR-EXT-03 |
| **P1SC-4** | boundary/entity 레이어 분리 후 Feature Envy 스멜 해소 | NFR-SRP 확장 |

---

## 8. 추적 매트릭스

| FR ID | Test ID | 우선순위 | 구현 상태 | pytest | 비고 |
|-------|---------|----------|-----------|--------|------|
| FR-VAL-01 | VAL-01 | P0 | ✅ | PASS | golden VAL-01 |
| FR-VAL-02 | VAL-02 | P0 | ✅ | PASS (4 cases) | |
| FR-VAL-03 | VAL-03 | P0 | ✅ | PASS | |
| FR-CONV-01 | CONV-01 | P0 | ✅ | PASS | |
| FR-CONV-02 | CONV-02 | P0 | ✅ | PASS | |
| FR-CONV-03 | CONV-03 | P0 | ✅ | PASS | golden CONV-03 |
| FR-EXT-01 | — | P1 | ⬜ | — | deferred |
| FR-EXT-02 | — | P1 | ⬜ | — | deferred |
| FR-EXT-03 | — | P1 | ⬜ | — | deferred |

**NFR 추적**

| NFR ID | 근거 산출물 | 상태 |
|--------|-------------|------|
| NFR-CONSTANTS | `entity/constants.py` | ✅ |
| NFR-SRP (부분) | `UnitConverter.py` helper 3개 | ✅ |
| NFR-TDD | `.cursorrules`, Skill, Step4 | ✅ |
| NFR-OCP | FR-EXT-02 미구현 | ⬜ |

---

## 9. 참고 문서

| 문서 | 경로 | 용도 |
|------|------|------|
| README | `README.md` | 실행·구조·Activities |
| Mom Test 인터뷰 | `Report/Step1_MomTest_인터뷰_보고서.md` | 사용자 문제·증거 |
| Mom Test 평가 | `Report/Step1_MomTest_평가_보고서.md` | 인터뷰 품질 |
| Step3 워크북 | `Report/Step3_워크북.md` | R-G-I-O · SC-1~3 · 범위 밖 |
| Step4 TDD | `Report/Step4_TDD_RED_보고서.md` | P0 RED→GREEN |
| Step6 Refactor | `Report/Step6_Refactor_보고서.md` | 스멜 · safe 이력 |
| Test manifest | `tests/manifest.json` | Given/Then SSOT (세부) |

---

## 변경 이력

| 버전 | 일자 | 변경 |
|------|------|------|
| 1.0 | 2026-06-11 | 초안 — Report 통합, FR/NFR·성공기준·추적 매트릭스 |
