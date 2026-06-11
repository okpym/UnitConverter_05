"""Unit Converter Test Loop — P0 tests driven by tests/manifest.json."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from UnitConverter import main

pytestmark = pytest.mark.p0

METER_TO_FEET = 3.28084
METER_TO_YARD = 1.09361


def _run_main(monkeypatch, capsys, input_str: str) -> str:
    monkeypatch.setattr("builtins.input", lambda _: input_str)
    main()
    return capsys.readouterr().out


def _conversion_lines(out: str) -> list[str]:
    return [line for line in out.splitlines() if " = " in line]


@pytest.mark.val
def test_VAL_01_negative_input_rejected(monkeypatch, capsys):
    """Given meter:-1 → Then 음수 거부. Mom Test: feet:-3 통과 버그."""
    out = _run_main(monkeypatch, capsys, "meter:-1")

    assert " feet" not in out and " yard" not in out, "음수 입력이 변환 결과로 출력됨"
    assert any(
        hint in out.lower() for hint in ("negative", "invalid", "error", "음수")
    ), "음수 거부 안내 메시지가 없음"


@pytest.mark.val
@pytest.mark.parametrize("invalid_input", ["meter", "abc"])
def test_VAL_02_invalid_format_rejected(monkeypatch, capsys, invalid_input):
    """Given meter (no colon) or abc → Then Invalid format."""
    out = _run_main(monkeypatch, capsys, invalid_input)

    assert "Invalid format" in out, "형식 오류 안내 메시지가 없음"
    assert _conversion_lines(out) == [], "잘못된 형식인데 변환 결과가 출력됨"


@pytest.mark.val
def test_VAL_03_unknown_unit_rejected(monkeypatch, capsys):
    """Given metre:2.5 → Then Unknown unit."""
    out = _run_main(monkeypatch, capsys, "metre:2.5")

    assert "Unknown unit" in out, "미등록 단위 안내 메시지가 없음"
    assert _conversion_lines(out) == [], "미등록 단위인데 변환 결과가 출력됨"


@pytest.mark.conv
def test_CONV_01_meter_input_outputs_all_units(monkeypatch, capsys):
    """Given meter:2.5 → Then meter, feet, yard 세 줄 출력."""
    out = _run_main(monkeypatch, capsys, "meter:2.5")
    lines = _conversion_lines(out)

    assert len(lines) == 3, f"meter/feet/yard 3줄 기대, 실제: {lines!r}"
    assert re.search(r"meter\s*=", lines[0]), lines[0]
    assert re.search(r"feet\s*$", lines[1]), lines[1]
    assert re.search(r"yard\s*$", lines[2]), lines[2]


@pytest.mark.conv
def test_CONV_02_feet_input_converts_via_meter(monkeypatch, capsys):
    """Given feet:10 → Then meter 기준 역변환 후 타 단위 출력."""
    out = _run_main(monkeypatch, capsys, "feet:10")
    lines = _conversion_lines(out)

    assert len(lines) == 3, f"변환 3줄 기대, 실제: {lines!r}"

    meter_match = re.search(r"= ([\d.eE+-]+) meter", lines[0])
    feet_match = re.search(r"= ([\d.eE+-]+) feet", lines[1])
    yard_match = re.search(r"= ([\d.eE+-]+) yard", lines[2])
    assert meter_match and feet_match and yard_match

    meter_val = float(meter_match.group(1))
    feet_val = float(feet_match.group(1))
    yard_val = float(yard_match.group(1))

    expected_meter = 10 / METER_TO_FEET
    assert abs(meter_val - expected_meter) < 0.001
    assert abs(feet_val - 10) < 0.001
    assert abs(yard_val - expected_meter * METER_TO_YARD) < 0.001


@pytest.mark.conv
def test_CONV_03_golden_meter_to_feet_matches_readme(monkeypatch, capsys):
    """Given meter:2.5 → Then feet ≈ 8.2 (README 예시, ±0.1)."""
    out = _run_main(monkeypatch, capsys, "meter:2.5")

    feet_match = re.search(r"= ([\d.eE+-]+) feet", out)
    assert feet_match, f"feet 변환 줄 없음: {out!r}"

    feet_val = float(feet_match.group(1))
    assert abs(feet_val - 8.2) <= 0.1, f"README golden 8.2 ft ±0.1 기대, 실제 {feet_val}"
