"""Unit Converter Test Loop — Session 3.

RED 본문은 /tdd-red 로 Test ID 단위 작성.
"""

import re

import pytest

pytestmark = pytest.mark.p0


@pytest.mark.val
@pytest.mark.parametrize(
    "negative_input",
    [pytest.param("meter:-1", id="VAL-01")],
)
def test_VAL_01_negative_input_rejected(monkeypatch, capsys, negative_input):
    """Given meter:-1 → Then 음수 거부. Mom Test: feet:-3 통과 버그."""
    # Arrange
    monkeypatch.setattr("builtins.input", lambda _: negative_input)

    # Act
    from UnitConverter import main

    main()
    out = capsys.readouterr().out

    # Assert — 음수 입력 거부 (에러 메시지 또는 변환 미출력)
    conversion_lines = [
        line
        for line in out.splitlines()
        if " feet" in line or " yard" in line
    ]
    assert not conversion_lines, (
        f"{negative_input} 은 음수이므로 거부되어야 함 — 변환 결과가 출력되면 안 됨"
    )


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
def test_VAL_02_invalid_format_rejected(monkeypatch, capsys, invalid_input):
    """Given meter/abc (manifest) → Then Invalid format. Mom Test: 입력 형식 검증."""
    # Arrange
    monkeypatch.setattr("builtins.input", lambda _: invalid_input)

    # Act
    from UnitConverter import main

    main()
    out = capsys.readouterr().out

    # Assert — Invalid format 안내, 변환 미출력
    assert "Invalid format" in out, (
        f"{invalid_input!r} 은 형식 오류이므로 Invalid format 안내가 필요함"
    )
    conversion_lines = [
        line
        for line in out.splitlines()
        if " feet" in line or " yard" in line
    ]
    assert not conversion_lines, (
        f"{invalid_input!r} 형식 오류 시 변환 결과가 출력되면 안 됨"
    )


@pytest.mark.val
@pytest.mark.parametrize(
    "unknown_input",
    [pytest.param("metre:2.5", id="VAL-03")],
)
def test_VAL_03_unknown_unit_rejected(monkeypatch, capsys, unknown_input):
    """Given metre:2.5 → Then Unknown unit. Mom Test: 오타 단위 metre 시나리오."""
    # Arrange
    monkeypatch.setattr("builtins.input", lambda _: unknown_input)

    # Act
    from UnitConverter import main

    main()
    out = capsys.readouterr().out

    # Assert — Unknown unit 안내, 변환 미출력
    assert "Unknown unit" in out, (
        f"{unknown_input!r} 은 미등록 단위이므로 Unknown unit 안내가 필요함"
    )
    conversion_lines = [
        line
        for line in out.splitlines()
        if " feet" in line or " yard" in line
    ]
    assert not conversion_lines, (
        f"{unknown_input!r} 미등록 단위 시 변환 결과가 출력되면 안 됨"
    )


@pytest.mark.conv
@pytest.mark.parametrize(
    "valid_input",
    [pytest.param("meter:2.5", id="CONV-01")],
)
def test_CONV_01_meter_input_outputs_all_units(monkeypatch, capsys, valid_input):
    """Given meter:2.5 → Then meter, feet, yard 세 줄. Mom Test: 스타터 실행 확인."""
    # Arrange
    monkeypatch.setattr("builtins.input", lambda _: valid_input)

    # Act
    from UnitConverter import main

    main()
    out = capsys.readouterr().out
    lines = [line for line in out.splitlines() if line.strip()]

    # Assert — meter, feet, yard 각각 한 줄씩 (결과 단위는 줄 끝으로 판별)
    assert len(lines) == 3, f"변환 결과는 3줄이어야 함: {lines!r}"
    assert sum(line.strip().endswith("meter") for line in lines) == 1
    assert sum(line.strip().endswith("feet") for line in lines) == 1
    assert sum(line.strip().endswith("yard") for line in lines) == 1


@pytest.mark.conv
@pytest.mark.parametrize(
    "valid_input",
    [pytest.param("feet:10", id="CONV-02")],
)
def test_CONV_02_feet_input_converts_via_meter(monkeypatch, capsys, valid_input):
    """Given feet:10 → Then meter 기준 역변환 후 타 단위 출력."""
    # Arrange
    monkeypatch.setattr("builtins.input", lambda _: valid_input)
    feet_value = 10.0
    expected_meters = feet_value / 3.28084

    # Act
    from UnitConverter import main

    main()
    out = capsys.readouterr().out
    lines = [line for line in out.splitlines() if line.strip()]

    # Assert — 세 단위 출력 + meter 기준 역변환 값
    assert len(lines) == 3
    assert sum(line.strip().endswith("meter") for line in lines) == 1
    assert sum(line.strip().endswith("feet") for line in lines) == 1
    assert sum(line.strip().endswith("yard") for line in lines) == 1

    meter_line = next(line for line in lines if line.strip().endswith("meter"))
    meter_match = re.search(r"= ([\d.]+) meter", meter_line)
    assert meter_match is not None
    assert abs(float(meter_match.group(1)) - expected_meters) < 0.001


@pytest.mark.conv
@pytest.mark.parametrize(
    "golden_input",
    [pytest.param("meter:2.5", id="CONV-03")],
)
def test_CONV_03_golden_meter_to_feet_matches_readme(monkeypatch, capsys, golden_input):
    """Given meter:2.5 → Then feet ≈ 8.2 (README, ±0.1). Mom Test: 반올림 불안."""
    # Arrange
    monkeypatch.setattr("builtins.input", lambda _: golden_input)

    # Act
    from UnitConverter import main

    main()
    out = capsys.readouterr().out

    # Assert — README Golden: 2.5 m → feet ≈ 8.2
    feet_line = next(line for line in out.splitlines() if " feet" in line)
    feet_match = re.search(r"= ([\d.]+) feet", feet_line)
    assert feet_match is not None
    feet_value = float(feet_match.group(1))
    assert abs(feet_value - 8.2) <= 0.1, (
        f"README 예시: 2.5 meter → feet ≈ 8.2 (±0.1), got {feet_value}"
    )
