# Step4 TDD RED 저장 프롬프트

```
Report 폴더와 Prompt 폴더에 Step4 RED 산출물 저장!!!
```

### 저장 대상

| 폴더 | 파일 | 내용 |
|------|------|------|
| `Report/` | `Step4_TDD_RED_보고서.md` | P0 RED 결과, pytest 요약, VAL-01 FAIL 상세, Mom Test 매핑, 다음 GREEN |
| `Prompt/` | `Step4_TDD_RED_프롬프트.md` | RED 역할·절차·Test ID 순서·보고 템플릿 |
| `Prompt/` | `Step4_TDD_RED_저장_프롬프트.md` | 본 저장 지시 |
| `tests/` | `test_converter.py` | P0 RED 본문 (skip 제거, AAA) |

### RED 세션 핵심 수치 (2026-06-11)

```bash
pytest -m p0 -v --maxfail=10
# → 6 passed, 1 failed, 0 skipped
# FAIL: VAL-01 (음수 미검증)
```

### 다음 세션 산출 (미작성 · GREEN 시)

| 폴더 | 파일 (예정) | 내용 |
|------|-------------|------|
| `Report/` | `Step4_TDD_GREEN_보고서.md` | VAL-01 GREEN 및 P0 전체 PASS |
| `Prompt/` | `Step4_TDD_GREEN_프롬프트.md` | GREEN 절차·최소 구현 규칙 |
