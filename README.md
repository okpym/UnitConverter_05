
## Unit Converter (Python)
![unit-converter](./unit-converter.jpg)

### Overview
- 사용자가 입력한 길이(`단위:값`)를 기반으로, 해당 값을 다른 모든 단위로 변환해 출력하는 프로그램.
- 새로운 단위를 추가할 때 기존 코드의 변경이 최소화되도록 설계한다.
- 각 단위 변환 로직은 테스트 코드로 검증한다.

### 현재 진행 상태

| 단계 | 상태 | 산출물 |
|------|------|--------|
| Step1 Mom Test | ✅ | `Report/Step1_MomTest_*.md` |
| Step3 워크북 · TDD 인프라 | ✅ | `Report/Step3_워크북.md`, `tests/`, `.cursorrules` |
| 기본·품질 요구 구현 | ⬜ | `UnitConverter.py` 프로토타입 (37줄) |
| TC 본문 (RED/GREEN) | ⬜ | skeleton 6건 skip |
| 추가 요구사항 | ⬜ | 설정 외부화 · 동적 등록 · 출력 포맷 |

### Mom Test 요약

**표면 문제:** meter/feet/yard를 한 번에 변환해 주는 Unit Converter 프로그램을 만든다.

**진짜 문제 (Step3 · 가상 시뮬레이션):** README의 품질·테스트 요구를 실행 가능한 작업으로 쪼개지 못해 초안·캡처·외부 검색에 시간을 쓰고, 제출 직전 테스트·출력 포맷 불안으로 확장 요구를 손대지 않는다.

**Step1 인터뷰 (별도 시나리오):** 해외 쇼핑 inch↔cm 비교 시 계산기·메모를 오가며 8~10분 재검산 — 상세는 [`Report/Step1_MomTest_인터뷰_보고서.md`](./Report/Step1_MomTest_인터뷰_보고서.md).

**이번 세션 주제:** 요구를 Test ID 단위로 쪼개 RED→GREEN마다 pytest로 즉시 확인하는 작업 방식을 먼저 고정한다. ([`Report/Step3_워크북.md`](./Report/Step3_워크북.md))

---

### 가상환경 설정 및 실행

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 의존성 (테스트)
pip install pytest

# 실행
python UnitConverter.py

# 테스트 (Session 3 — skeleton, 현재 6 skipped)
pytest

# P0만
pytest -m p0 -v

# 가상환경 비활성화
deactivate
```

### 프로젝트 구조

```
UnitConverter_05/
├── UnitConverter.py          # 프로토타입 (프로덕션)
├── tests/
│   ├── manifest.json         # Test ID (CONV-*, VAL-*)
│   ├── conftest.py
│   └── test_converter.py     # RED skeleton
├── Report/                   # Mom Test · Step3 워크북
├── Prompt/                   # 인터뷰·평가 프롬프트
├── .cursorrules              # Rule (TDD · pytest 게이트)
└── .cursor/
    ├── commands/tdd-red.md   # RED Command
    └── skills/unit-converter-tdd/SKILL.md
```

### Test ID (P0)

| ID | Given | Then |
|----|-------|------|
| VAL-01 | `meter:-1` | 음수 거부 |
| VAL-02 | `meter` / `abc` | 형식 오류 |
| VAL-03 | `metre:2.5` | 미등록 단위 |
| CONV-01 | `meter:2.5` | meter/feet/yard 출력 |
| CONV-02 | `feet:10` | meter 기준 역변환 |
| CONV-03 | `meter:2.5` | feet ≈ 8.2 (README 예시) |

출처: [`tests/manifest.json`](./tests/manifest.json)

### 기본 요구사항
1. 사용자 입력 예시:
   ```
   meter:2.5
   ```
   → 출력:
   ```
   2.5 meter = 8.2 feet
   2.5 meter = 2.7 yard
   ...
   ```

2. 현재 지원 단위:
   - meter
   - feet
   - yard

3. 새로운 단위가 추가될 때도 기존 코드의 변경이 최소화되도록 할 것.

4. 각 단위 간 변환이 정확히 계산되도록 테스트 코드를 작성할 것.

### 비즈니스 로직
- `1 meter = 3.28084 feet`
- `1 meter = 1.09361 yard`
- feet/yard 간의 비율은 meter 기반으로 계산.

### 품질 요구사항
- OCP를 만족하는 설계
- SRP를 만족하는 클래스 구성
- 입력 값 검증 (음수, 잘못된 형식, 없는 단위)

### 추가 요구사항
- **설정 외부화**
   - 변환 비율을 외부 설정 파일(JSON/YAML)에서 로드
- **동적으로 단위와 비율을 등록할 수 있도록 한다**
   - 사용자 입력으로 `1 cubit = 0.4572 meter`를 등록하고 사용 가능
- **출력 포맷 선택 기능**
   - JSON / CSV / 표 형태 출력

### Cursor AI (Session 3)

| 계층 | 경로 | 용도 |
|------|------|------|
| Rule | `.cursorrules` | TDD Phase, RED 없는 GREEN 금지 |
| Command | `/tdd-red` | 실패 테스트만 작성 |
| Skill | `@unit-converter-tdd` | RED → GREEN → REFACTOR 절차 |
| Test Loop | `pytest` | Phase마다 실행·보고 |

다음 권장: `/tdd-red VAL-01` — 음수 입력 RED 본문 작성.

---

## 생성형AI를 활용한 Activities (6 시간)

1. 문제 코드 및 기본 요구사항 분석 (0.5시간)
   - 기본 코드구조, 로직 이해
   - Mom Test 인터뷰 · 문제 재정의
2. 기본 요구사항 및 품질 요구사항 구현 (2시간)
   - OCP를 만족하는 인터페이스 구현
   - SRP를 만족하도록 클래스 구현
   - 입력값 검증을 위한 구현
3. TC 구현 (0.5시간)
   - 단위변환 기능 검증 및 입력 값 검증 TC 작성
   - Session 3: manifest · pytest Harness · Rule/Command/Skill
4. 추가 요구사항 구현 (2시간)
   - 3개 요구사항 구현 및 TC 작성
5. 회고 및 발표 (1시간)
   - 실습 목표와 달성도
   - AI를 어떻게 활용했나? 도움이 된 순간과 한계는?
   - TC를 추가보면서 개선에 미친 영향, TC 작성 팁
   - 클린코드와 리팩토링에서 느낀 장점과 어려운점

### 문서 목록

| 문서 | 설명 |
|------|------|
| [`Report/Step1_MomTest_인터뷰_보고서.md`](./Report/Step1_MomTest_인터뷰_보고서.md) | Mom Test Q&A · inch↔cm 시나리오 |
| [`Report/Step1_MomTest_평가_보고서.md`](./Report/Step1_MomTest_평가_보고서.md) | Mom Test 중간 평가 |
| [`Report/Step3_워크북.md`](./Report/Step3_워크북.md) | R-G-I-O · 성공 기준 · 8계층 |
