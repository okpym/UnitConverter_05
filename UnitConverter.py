from entity.constants import METER_TO_FEET, METER_TO_YARD

_INVALID_FORMAT_MSG = "Invalid format. Use unit:value (ex: meter:2.5)"


def _parse_unit_value(input_str: str) -> tuple[str, float] | None:
    if ":" not in input_str:
        print(_INVALID_FORMAT_MSG)
        return None

    unit, value_str = input_str.split(":", 1)
    if not unit or not value_str:
        print(_INVALID_FORMAT_MSG)
        return None

    try:
        value = float(value_str)
    except ValueError:
        print(f"Invalid number: {value_str}")
        return None

    if value < 0:
        print(f"Negative value: {value_str}")
        return None

    return unit, value


def _to_meter_value(unit: str, value: float) -> float | None:
    if unit == "meter":
        return value
    if unit == "feet":
        return value / METER_TO_FEET
    if unit == "yard":
        return value / METER_TO_YARD

    print(f"Unknown unit: {unit}")
    return None


def _print_conversions(value: float, unit: str, meter_value: float) -> None:
    in_feet = meter_value * METER_TO_FEET
    in_yards = meter_value * METER_TO_YARD

    print(f"{value} {unit} = {meter_value} meter")
    print(f"{value} {unit} = {in_feet} feet")
    print(f"{value} {unit} = {in_yards} yard")


def main():
    input_str = input("Insert value for converting (ex: meter:2.5): ")

    parsed = _parse_unit_value(input_str)
    if parsed is None:
        return

    unit, value = parsed
    meter_value = _to_meter_value(unit, value)
    if meter_value is None:
        return

    _print_conversions(value, unit, meter_value)


if __name__ == "__main__":
    main()
