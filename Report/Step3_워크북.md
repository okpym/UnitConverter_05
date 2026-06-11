# Step3 세션 3 워크북

- **프로젝트:** Unit Converter (`UnitConverter_05`)
- **일자:** 2026-06-11
- **세션 범위:** Mom Test → 주제·R-G-I-O → 8계층 중 **Rule · Command · (Skill) · Test Loop**
- **Mom Test 출처:** [가상 시뮬레이션] 프로그래밍 수업 UnitConverter 과제 페르소나 (실제 사용자 경험 아님)

---

## Mom Test 결과

- **페르소나:** 대학 2학년 Python 입문 수업 학생. 지난주 `README.md` + `UnitConverter.py` 스타터로 UnitConverter 과제 수령, 마감 금요일 23:59.
- **진짜 문제 (한 문장):** README의 품질·테스트 요구를 실행 가능한 작업으로 쪼개지 못해 초안·캡처·외부 검색에 약 4시간을 쓰고, 제출 직전에는 테스트 부족과 출력 포맷 불일치 불안으로 확장 요구(OCP·동적 등록)를 아예 손대지 않았다.
- **Mom Test 증거 3줄:**
  1. **과거·구체:** 화~금 총 **~4시간** — 상당 부분 README·OCP·테스트 요구 **해석**에 소모 (실제 코딩보다 “무엇을 원하는지” 파악).
  2. **실제 행동:** `feet:-3` 확인 후 **`main()` 미연결** — 터미널 캡처·`draft_validator.py` 주석만 남기고 본 코드는 그대로 둠.
  3. **불안·비용:** 제출 직전 **테스트 1개·출력 반올림** 불일치 — `round()` 시도 후 assert 깨져 **원복**, `cubit` 등록·설정 외부화는 **미시도**.

---

## 1) 주제 한 문장 (Mom Test 기반 · 솔루션 최소화)

> **요구(검증·테스트·확장)를 한 번에 구현하려 하지 말고, README 항목을 Test ID 단위로 쪼개 RED→GREEN마다 pytest로 “맞는지”를 즉시 확인할 수 있는 작업 방식을 먼저 고정한다.**

(“단위 변환기 앱을 만든다”가 아니라, 가상 인터뷰에서 드러난 **재확인·초안 정체 비용**을 줄이는 것이 주제.)

---

## 2) R-G-I-O

| 구분 | 정의 | UnitConverter_05 내용 |
|------|------|------------------------|
| **R — Reality (현재)** | 지금 상태 + 진짜 문제 | `UnitConverter.py` 37줄 단일 `main()`, meter/feet/yard 하드코딩, 음수·오타 미검증. Mom Test: 학습자가 요구를 **캡처·초안·ChatGPT·유튜브**로 처리하고 **테스트 1개·포맷 불안**으로 제출. OCP/SRP·동적 등록·JSON/CSV는 **손대지 않음**. |
| **G — Goal (목표)** | 이번 세션 달성 상태 | **구현 전** AI 거버넌스·검증 루프 확립: `.cursorrules`(Rule), `/tdd-red`(Command), `unit-converter-tdd`(Skill), `tests/`+pytest(Test Loop). README P0(변환·입력 검증)를 `tests/manifest.json` Test ID로 분해. |
| **I — Input (입력·전제)** | 재료·경계 | `README.md` 기본·품질 요구, `UnitConverter.py` 스타터, Mom Test 증거 3줄, Activities 6h 로드맵(세션 3 = TC 인프라 선행). **금지:** cubit·설정 외부화·출력 포맷 선택은 이번 세션 범위 밖. |
| **O — Output (산출)** | 완료 시 보이는 것 | (1) `Report/Step3_워크북.md` (본 문서) (2) `.cursorrules` (3) `.cursor/commands/tdd-red.md` (4) `.cursor/skills/unit-converter-tdd/SKILL.md` (5) `tests/manifest.json` + skeleton pytest — `pytest --collect-only`로 Test ID 수집 가능, P0는 skip skeleton. |

---

## 3) 성공 기준 3개 (Mom Test 증거 연결)

| ID | 기준 | Mom Test 증거 연결 | 검증 방법 |
|----|------|-------------------|-----------|
| **SC-1** | README P0 요구가 **Test ID 1:1**로 `manifest.json`에 등록되어, “OCP가 뭔지 모르겠다”는 막연함 대신 **할 일 목록**이 보인다. | 증거 1: 4시간 중 상당 부분 **요구 해석** → Test ID로 쪼갬 | `tests/manifest.json`에 CONV-01~03, VAL-01~03 존재 |
| **SC-2** | 음수·형식·미등록 단위에 대한 **RED 테스트 골격**이 있고, Rule이 “RED 없이 GREEN 금지”를 명시한다. | 증거 2: `feet:-3` **캡처만** → VAL-01 RED가 실패 상태로 대기 | `pytest -k VAL-01` 수집·skip 또는 FAIL; `.cursorrules` TDD 절 |
| **SC-3** | TDD Phase마다 **pytest 실행·보고**가 Rule·Skill·Command에 정의되어, 제출 직전 “assert 깨질까 봐 원복” 패턴을 **루프로 선행 검증**한다. | 증거 3: 테스트 1개·포맷 불안 **원복** → Test Loop가 변경 전후 게이트 | Skill § Test Loop; Command RED 보고 템플릿 |

---

## 4) 표면 문제 — 이번 프로젝트에서 하지 않을 것

Mom Test·README에서 **과제처럼 보이지만** 진짜 문제(재확인·초안 정체)와 무관하거나 **이번 세션 범위 밖**인 항목:

| 하지 않을 것 | 이유 (Mom Test 연결) |
|-------------|---------------------|
| **“완성된 단위 변환 앱”을 한 번에 구현** | 표면 과제; 학습자는 변환 로직은 계산기로 이미 맞춤 봄 — 병목은 **구조·검증** |
| **OCP 리팩터 + cubit 동적 등록 + 설정 외부화** | 페르소나가 **아예 미시도** — 설계 문맹 구간; Phase 4(추가 요구)로 연기 |
| **JSON / CSV / 표 형태 출력 포맷 선택** | 제출 불안은 **반올림·예시 불일치** — 포맷 기능 추가는 오히려 검증 면적만 확대 |
| **ChatGPT·유튜브 의존 워크플로 고정** | 외부 검색은 증거상 **대체 행동** — 이번 세션은 Rule·Test Loop로 **자기 검증** 습관만 |
| **Step1 인터뷰(가구 inch↔cm)를 그대로 FR로 구현** | 별개 페르소나·시나리오 — 본 프로젝트 P0는 README `meter:2.5` 기준 |

---

## 8계층 — 이번 세션에서 만드는 것

> 전체 8계층: Model · Agent · Harness / **Rule · Skill · Command** / Tool·MCP · **Test/Review Loop** / Hook  
> **이번 세션:** Rule, Command, (Skill), Test Loop 만. Hook·전체 구현·GREEN은 다음 세션.

| 계층 | 산출물 | 역할 (한 줄) | 경로 |
|------|--------|-------------|------|
| **Rule** | Cursor 헌법 | TDD Phase, 파일 배치, RED 없는 GREEN 금지, pytest 게이트 | `.cursorrules` |
| **Command** | RED 단축 버튼 | 실패 테스트만 작성; 프로덕션 수정 금지 | `.cursor/commands/tdd-red.md` |
| **(Skill)** | TDD 매뉴얼 | RED→GREEN→REFACTOR 절차·pytest 보고; Command와 연결 | `.cursor/skills/unit-converter-tdd/SKILL.md` |
| **Test Loop** | pytest Harness | manifest 기반 Test ID, Phase 후 pytest 실행·보고 | `tests/manifest.json`, `tests/conftest.py`, `tests/test_converter.py`, `pyproject.toml` |

### 계층 연결

```
Mom Test 증거 → manifest Test ID (SC-1)
       ↓
Rule (.cursorrules) ← Command (/tdd-red) ← Skill (unit-converter-tdd)
       ↓
Test Loop (pytest) — RED FAIL 확인 → (다음 세션) GREEN
```

### 다음 세션 예고 (본 워크북 범위 밖)

- `/tdd-red VAL-01` — 음수 입력 RED 본문 작성 → FAIL 확인
- GREEN: `UnitConverter.py` 최소 수정 + pytest 통과
- REFACTOR: SRP 클래스 분리 (README 품질 요구)
- Hook (`hooks.json`): 미착수

---

## 참고

| 문서 | 경로 |
|------|------|
| Mom Test 시뮬레이션 (채팅) | 가상 3턴 — 학생 페르소나 |
| Step1 인터뷰 (별도 시나리오) | `Report/Step1_MomTest_인터뷰_보고서.md` |
| 요구사항 | `README.md` |
| 스타터 코드 | `UnitConverter.py` |
