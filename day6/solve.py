from race import Race


def read_input(input_path: str) -> dict[str, list[int]]:
    data = {}
    with open(input_path, "r", encoding="utf8") as f:
        for line in f:
            key, raw_values = line.split(":", maxsplit=1)
            key = key.lower()

            values = [int(x) for x in raw_values.strip().split()]
            data[key] = values

    return data


def main():
    input_path = "input.txt"  # part 1
    # input_path = "input2.txt" # part 2
    # input_path = "simple_input.txt"
    data = read_input(input_path)
    times = data["time"]
    records = data["distance"]

    prod = 1
    for time, record in zip(times, records):
        race = Race(time, record)
        button_times = race.button_times_to_beat_record()
        # print(f"Winning button times: {button_times}")
        print(f"Number of ways to beat: {len(button_times)}")
        prod *= len(button_times)

    print(f"Multiplying number of ways to beat we have: {prod}")


if __name__ == "__main__":
    main()
