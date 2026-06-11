"""Unit Converter — PSC 기반 RED 스켈레톤 (PRD §7.1).

PSC ↔ Test ID:
  PSC-1 → CONV-01  (유효 입력 1회 → meter·feet·yard 동시 출력)
  PSC-2 → VAL-01~03 (잘못된 입력 거부 + 안내 메시지)
  PSC-3 → CONV-03  (README 예시 수치 ±0.1)

RED 본문(assert)은 /tdd-red 로 Test ID 단위 작성.
"""

import pytest

pytestmark = pytest.mark.p0


# =============================================================================
# PRD §7.1 PSC-1 — 유효 입력 1회로 meter·feet·yard 결과를 동시에 확인
# 측정: meter:2.5 실행 → 3줄 출력 (CONV-01)
# Mom Test: 인터뷰 — 단계별 계산·메모 반복 감소
# =============================================================================


@pytest.mark.conv
@pytest.mark.parametrize(
    "valid_input",
    [pytest.param("meter:2.5", id="CONV-01")],
)
def test_PSC_01_single_input_all_units(monkeypatch, capsys, valid_input):
    """PSC-1 | CONV-01 — Given meter:2.5 → Then meter, feet, yard 세 줄."""
    # Given: meter:2.5 (manifest)
    # When: main() 호출
    # Then: meter·feet·yard 동시 출력 (3줄)
    pytest.fail("RED: PSC-1 / CONV-01 — 동시 단위 출력 assert 미작성")


# =============================================================================
# PRD §7.1 PSC-2 — 잘못된 입력 시 변환 미출력 + 안내 메시지
# 측정: VAL-01~03 pytest PASS
# Mom Test: 시뮬 — feet:-3 캡처만 → 실제 거부
# =============================================================================


@pytest.mark.val
@pytest.mark.parametrize(
    "invalid_input",
    [pytest.param("meter:-1", id="VAL-01")],
)
def test_PSC_02_negative_input_rejected(monkeypatch, capsys, invalid_input):
    """PSC-2 | VAL-01 — Given meter:-1 → Then 음수 거부."""
    # Given: meter:-1 (manifest)
    # When: main() 호출
    # Then: 음수 거부 — 변환 결과 미출력
    pytest.fail("RED: PSC-2 / VAL-01 — 음수 입력 거부 assert 미작성")


@pytest.mark.val
@pytest.mark.parametrize(
    "invalid_input",
    [
        pytest.param("meter", id="VAL-02-no-colon"),
        pytest.param("abc", id="VAL-02-garbage"),
        pytest.param("meter:", id="VAL-02-empty-value"),
        pytest.param(":2.5", id="VAL-02-empty-unit"),
    ],
)
def test_PSC_02_invalid_format_rejected(monkeypatch, capsys, invalid_input):
    """PSC-2 | VAL-02 — Given 형식 오류 → Then Invalid format 안내."""
    # Given: meter / abc / meter: / :2.5 (manifest)
    # When: main() 호출
    # Then: Invalid format 안내 — 변환 결과 미출력
    pytest.fail("RED: PSC-2 / VAL-02 — 형식 오류 거부 assert 미작성")


@pytest.mark.val
@pytest.mark.parametrize(
    "unknown_input",
    [pytest.param("metre:2.5", id="VAL-03")],
)
def test_PSC_02_unknown_unit_rejected(monkeypatch, capsys, unknown_input):
    """PSC-2 | VAL-03 — Given metre:2.5 → Then Unknown unit 안내."""
    # Given: metre:2.5 (manifest)
    # When: main() 호출
    # Then: Unknown unit 안내 — 변환 결과 미출력
    pytest.fail("RED: PSC-2 / VAL-03 — 미등록 단위 거부 assert 미작성")


# =============================================================================
# PRD §7.1 PSC-3 — README 예시 수치와 ±0.1 이내 일치
# 측정: CONV-03 pytest PASS (2.5 meter → feet ≈ 8.2)
# Mom Test: 반올림 불안 — 수치 허용 오차로 확신
# =============================================================================


@pytest.mark.conv
@pytest.mark.parametrize(
    "golden_input",
    [pytest.param("meter:2.5", id="CONV-03")],
)
def test_PSC_03_readme_feet_tolerance(monkeypatch, capsys, golden_input):
    """PSC-3 | CONV-03 — Given meter:2.5 → Then feet ≈ 8.2 (±0.1)."""
    # Given: meter:2.5 (manifest)
    # When: main() 호출
    # Then: feet ≈ 8.2 (README 예시, ±0.1)
    pytest.fail("RED: PSC-3 / CONV-03 — README 수치 허용 오차 assert 미작성")


# =============================================================================
# P0 보조 — PSC §7.1 범위 밖이나 manifest P0 (CONV-02)
# =============================================================================


@pytest.mark.conv
@pytest.mark.parametrize(
    "valid_input",
    [pytest.param("feet:10", id="CONV-02")],
)
def test_CONV_02_feet_input_converts_via_meter(monkeypatch, capsys, valid_input):
    """CONV-02 — Given feet:10 → Then meter 기준 역변환 후 타 단위 출력."""
    # Given: feet:10 (manifest)
    # When: main() 호출
    # Then: meter 기준 역변환 후 타 단위 출력
    pytest.fail("RED: CONV-02 — feet 역변환 assert 미작성")
