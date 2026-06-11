"""Unit Converter Test Loop skeleton — Session 3.

RED 본문은 /tdd-red 로 Test ID 단위 작성. 현재는 collect-only·skip skeleton.
"""

import pytest

pytestmark = pytest.mark.p0


@pytest.mark.val
def test_VAL_01_negative_input_rejected():
    """Given meter:-1 → Then 음수 거부. Mom Test: feet:-3 통과 버그."""
    pytest.skip("RED skeleton — /tdd-red VAL-01")


@pytest.mark.val
def test_VAL_02_invalid_format_rejected():
    """Given meter (no colon) → Then Invalid format."""
    pytest.skip("RED skeleton — /tdd-red VAL-02")


@pytest.mark.val
def test_VAL_03_unknown_unit_rejected():
    """Given metre:2.5 → Then Unknown unit."""
    pytest.skip("RED skeleton — /tdd-red VAL-03")


@pytest.mark.conv
def test_CONV_01_meter_input_outputs_all_units():
    """Given meter:2.5 → Then meter, feet, yard lines."""
    pytest.skip("RED skeleton — /tdd-red CONV-01")


@pytest.mark.conv
def test_CONV_02_feet_input_converts_via_meter():
    """Given feet:10 → Then consistent conversion."""
    pytest.skip("RED skeleton — /tdd-red CONV-02")


@pytest.mark.conv
def test_CONV_03_golden_meter_to_feet_matches_readme():
    """Given meter:2.5 → Then feet ≈ 8.2 per README."""
    pytest.skip("RED skeleton — /tdd-red CONV-03")
