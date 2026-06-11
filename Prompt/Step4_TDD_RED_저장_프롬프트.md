# Step4 TDD RED→GREEN 저장 프롬프트

```
Report 폴더와 Prompt 폴더에 세션 4 TDD 산출물 저장!!!
```

### 저장 대상

| 폴더 | 파일 | 내용 |
|------|------|------|
| `Report/` | `Step4_TDD_RED_보고서.md` | P0 RED→GREEN 요약, pytest 결과, 프로덕션·테스트 변경, 다음 단계 |
| `Prompt/` | `Step4_TDD_RED_프롬프트.md` | RED/GREEN 절차, Command·Skill 연결, P0 Test ID 표 |
| `Prompt/` | `Step4_TDD_RED_저장_프롬프트.md` | 본 저장 지시 |

### 세션 4에서 수정·완성된 코드 (참고)

| 경로 | 역할 |
|------|------|
| `UnitConverter.py` | VAL-01 음수, VAL-02 빈 unit/value 검증 |
| `tests/test_converter.py` | P0 AAA 테스트 본문 (skip 제거) |
| `tests/conftest.py` | import path |
| `.cursorrules` | TDD Rule (변경 없음) |
| `.cursor/commands/tdd-red.md` | RED Command |
| `.cursor/skills/unit-converter-tdd/SKILL.md` | TDD Skill |

### 검증 스냅샷 (저장 시점)

```bash
pytest -m p0 -v
# → 9 passed, 0 failed, 0 skipped
```
