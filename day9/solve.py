from oasis_and_sand_instability_sensor import OasisAndSandInstabilitySensor


def main():
    input_path = "simple_input.txt"
    input_path = "input.txt"

    oasis_and_sand_instability_sensor = OasisAndSandInstabilitySensor(input_path)
    print(
        "The sum of extrapolated values is:"
        f" {sum(oasis_and_sand_instability_sensor.extrapolate_backwards())}"
    )


if __name__ == "__main__":
    main()
