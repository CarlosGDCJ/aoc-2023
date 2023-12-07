from almanac import Almanac
import logging


def main():
    logging.basicConfig(level=logging.DEBUG)
    input_file = "input.txt"
    # input_file = "simple_input.txt"
    almanac = Almanac(input_file)
    # locs = almanac.get_locations_part1()
    # print(f"Locations: {locs}")
    # print(f"\tmin location: {min(locs)}")

    locs2 = almanac.get_locations_part2()
    logging.info(f"Locations: {locs2}")
    logging.info(f"\tmin location: {min(locs2, key=lambda x: x[0])}")


if __name__ == "__main__":
    main()
