from engine import EngineSchematic


def main():
    schema = EngineSchematic("input.txt")

    print(f"Sum of part numbers: {schema.sum_part_numbers()}")
    print(f"Sum of gear ratios: {schema.sum_gear_ratio()}")


if __name__ == "__main__":
    main()
