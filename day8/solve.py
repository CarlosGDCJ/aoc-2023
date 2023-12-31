from network import NetworkMap
import math


def main():
    input_path = "simple_input.txt"
    input_path = "input2.txt"
    input_path = "simple_input2.txt"
    input_path = "input.txt"

    map_ = NetworkMap(input_path)

    print(
        f"Number of steps to get to {map_.end}: {math.lcm(*map_.follow_instructions())}"
    )


if __name__ == "__main__":
    main()
