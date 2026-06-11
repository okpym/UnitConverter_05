# Step5 ARRR Command · PRD 저장 프롬프트

```
Report 폴더와 Prompt 폴더에 세션 5 ARRR Command 산출물 저장!!!
```

### 저장 대상

| 폴더 | 파일 | 내용 |
|------|------|------|
| `Report/` | `Step5_ARRR_Command_보고서.md` | ARRR 매핑, Command·PRD, refactor-smell 결과, 다음 단계 |
| `Prompt/` | `Step5_ARRR_Command_프롬프트.md` | Command 파이프라인, 절차, P0 표, 요청 예시 |
| `Prompt/` | `Step5_ARRR_Command_저장_프롬프트.md` | 본 저장 지시 |

### 세션 5에서 추가·갱신된 파일 (참고)

| 경로 | 역할 |
|------|------|
| `docs/PRD.md` | FR SSOT · FR-VAL/CONV-* · 추적 매트릭스 |
| `.cursor/commands/red-test-plan.md` | Ask ③ C2C·테스트 플랜 |
| `.cursor/commands/red-skeleton.md` | Ask ④ pytest.fail 스켈레톤 |
| `.cursor/commands/green-minimal.md` | Respond GREEN 최소 구현 |
| `.cursor/commands/golden-master.md` | Approval Test |
| `.cursor/commands/refactor-smell.md` | Refine ⑦ 스멜 탐지 |
| `.cursorrules` | PRD·`/red-test-plan` |
| `README.md` | PRD·Command 부분 갱신 |

### 검증 스냅샷 (저장 시점)

```bash
python -m pytest tests/ -v
# → 9 passed, 0 failed, 0 skipped
```

### 미착수 (다음 세션)

| 항목 | Command |
|------|---------|
| refactor-safe 실행 | `/refactor-safe` (미생성) |
| Golden 구축 | `/golden-master` |
| README 진행 상태 Step4 반영 | 수동 |
