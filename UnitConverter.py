from entity.constants import METER_TO_FEET, METER_TO_YARD


def main():
    input_str = input("Insert value for converting (ex: meter:2.5): ")

    if ':' not in input_str:
        print("Invalid format. Use unit:value (ex: meter:2.5)")
        return

    unit, value_str = input_str.split(':', 1)

    if not unit or not value_str:
        print("Invalid format. Use unit:value (ex: meter:2.5)")
        return

    try:
        value = float(value_str)
    except ValueError:
        print(f"Invalid number: {value_str}")
        return

    if value < 0:
        print(f"Negative value: {value_str}")
        return

    if unit == "meter":
        meter_value = value
    elif unit == "feet":
        meter_value = value / METER_TO_FEET
    elif unit == "yard":
        meter_value = value / METER_TO_YARD
    else:
        print(f"Unknown unit: {unit}")
        return

    in_meters = meter_value
    in_feet = meter_value * METER_TO_FEET
    in_yards = meter_value * METER_TO_YARD

    print(f"{value} {unit} = {in_meters} meter")
    print(f"{value} {unit} = {in_feet} feet")
    print(f"{value} {unit} = {in_yards} yard")


if __name__ == "__main__":
    main()
