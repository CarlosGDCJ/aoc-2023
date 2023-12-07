#!/bin/env python3


def part1(raw_calibration):
    start = 0
    end = len(raw_calibration) - 1

    cal_value1 = None
    cal_value2 = None

    while (cal_value1 is None or cal_value2 is None) and start <= end:
        if raw_calibration[start].isdigit():
            cal_value1 = int(raw_calibration[start])

        if raw_calibration[end].isdigit():
            cal_value2 = int(raw_calibration[end])

        if cal_value1 is None:
            start += 1
        if cal_value2 is None:
            end -= 1

    if cal_value1 is None or cal_value2 is None:
        raise ValueError(f"Invalid input: {raw_calibration}")

    return cal_value1, cal_value2


def get_calibration_values(raw_calibration):
    start = 0
    end = len(raw_calibration) - 1

    digit1_idx = None
    digit2_idx = None

    # check for numeric digits
    while (digit1_idx is None or digit2_idx is None) and start <= end:
        if raw_calibration[start].isdigit():
            digit1_idx = start

        if raw_calibration[end].isdigit():
            digit2_idx = end

        if digit1_idx is None:
            start += 1
        if digit2_idx is None:
            end -= 1

    digit1 = int(raw_calibration[digit1_idx]) if digit1_idx is not None else -1
    digit2 = int(raw_calibration[digit2_idx]) if digit2_idx is not None else -1

    # check for spelled out digits
    spelled_digits = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }
    for digit_name, digit_value in spelled_digits.items():
        first_idx = raw_calibration.find(digit_name)
        last_idx = raw_calibration.rfind(digit_name)

        if first_idx == -1:
            continue

        if digit1_idx is None or first_idx < digit1_idx:
            digit1 = digit_value
            digit1_idx = first_idx

        if digit2_idx is None or last_idx > digit2_idx:
            digit2 = digit_value
            digit2_idx = last_idx

    return digit1, digit2


def main():
    calibration_sum = 0
    with open("input.txt", "r", encoding="utf8") as f:
        for line in f:
            raw_calibration = line.strip()
            # part 1
            # digit1, digit2 = part1(raw_calibration)
            # calibration_sum += digit1 * 10 + digit2
            digit1, digit2 = get_calibration_values(raw_calibration)
            calibration_sum += digit1 * 10 + digit2

    print(f"The sum of all calibrations is: {calibration_sum}")


if __name__ == "__main__":
    main()
