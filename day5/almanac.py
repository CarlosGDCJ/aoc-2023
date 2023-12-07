import logging

logger = logging.getLogger(__name__)


class Almanac:
    def __init__(self, src_path: str):
        self.src_path = src_path
        self.maps = []

        with open(self.src_path, "r", encoding="utf8") as f:
            seeds_line = f.readline().strip()
            # part 1
            self.seeds1 = self.get_seeds_part1(seeds_line)
            # part 2 | seeds are a list of tuples now
            self.seeds2 = self.get_seeds_part2(seeds_line)

            map_line = False
            for line in f:
                line = line.strip()
                if line.endswith("map:"):
                    # map data starts next
                    map_line = True
                    map_parts = []
                    continue

                elif line == "" and map_line:
                    map_line = False
                    # map data ended, create map
                    self.maps.append(Map(map_parts))
                    continue

                if map_line:
                    dest_start, src_start, size = [int(num) for num in line.split(" ")]
                    map_part = (
                        (src_start, src_start + size),
                        (dest_start, dest_start + size),
                    )

                    map_parts.append(map_part)

            if len(map_parts) > 0:
                self.maps.append(Map(map_parts))

    def get_seeds_part1(self, seeds_line: str) -> list[int]:
        return [
            int(s) for s in seeds_line.split(":", maxsplit=1)[-1].strip().split(" ")
        ]

    def get_seeds_part2(self, seeds_line: str) -> list[int]:
        seeds = []
        raw_nums = self.seeds1

        for i in range(0, len(raw_nums), 2):
            seeds.append((raw_nums[i], raw_nums[i] + raw_nums[i + 1]))

        return seeds

    def get_locations_part1(self) -> list[int]:
        """Walk through the maps and get a location"""
        locations = []
        for seed in self.seeds1:
            value = seed
            for map_ in self.maps:
                if value in map_:
                    value = map_[value]

            locations.append(value)

        return locations

    def get_locations_part2(self) -> set[int]:
        """Range-walk through the maps"""
        in_ranges = [x for x in self.seeds2]
        for map_ in self.maps:
            out_ranges = []
            # as we don't have to trace back to the original seeds, we pass everything through each map before moving on
            for range_ in in_ranges:
                out_ranges.extend(map_[range_])

            in_ranges = out_ranges

        return in_ranges


class Map:
    def __init__(self, map_parts):
        self.map_parts = sorted(map_parts, key=lambda x: x[0])

    def __contains__(self, item):
        for (src_start, src_end), _ in self.map_parts:
            if src_start <= item < src_end:
                return True

        return False

    def __getitem__(self, idx):
        if isinstance(idx, int):
            for (src_start, src_end), (dest_start, dest_end) in self.map_parts:
                if src_start <= idx < src_end:
                    return dest_start + (idx - src_start)

        elif isinstance(idx, tuple):
            out_ranges = []
            ranges_to_process = [idx]
            while len(ranges_to_process) > 0:
                logger.debug(f"ranges to process: {ranges_to_process}")
                start, end = ranges_to_process.pop()
                logger.debug(f"\tprocessing range: ({start}, {end})")
                has_intersection = False
                for (src_start, src_end), (dest_start, dest_end) in self.map_parts:
                    logger.debug(
                        f"\t\tmap part: ({src_start}, {src_end}) : ({dest_start},"
                        f" {dest_end})"
                    )
                    if src_start <= start < src_end:
                        has_intersection = True

                        # whole idx in map_part
                        if end <= src_end:
                            logger.debug("\t\twhole range in map_part")
                            delta_start = start - src_start
                            out_ranges.append(
                                (
                                    dest_start + delta_start,
                                    dest_start + delta_start + end - start,
                                )
                            )

                        # part of idx in map_part
                        # process the part that's in and leave the rest for later
                        else:
                            logger.debug("\t\tpart of range in map_part")
                            delta_start = start - src_start
                            out_ranges.append((dest_start + delta_start, dest_end))
                            ranges_to_process.insert(0, (src_end, end))

                        # there's no overlap between map parts, so if we found the match we can skip to the next
                        break

                    elif start <= src_start < end:
                        has_intersection = True

                        # whole map_part in idx
                        if src_end <= end:
                            logger.debug("\t\twhole map_part in range")
                            out_ranges.append((dest_start, dest_end))
                            ranges_to_process.insert(0, (start, src_start))
                            ranges_to_process.insert(0, (src_end, end))

                        # part of map_part in idx
                        else:
                            logger.debug("\t\tpart of map_part in range")
                            intersection_size = end - src_start
                            out_ranges.append(
                                (dest_start, dest_start + intersection_size)
                            )
                            ranges_to_process.insert(0, (start, src_start))

                        # there's no overlap between map parts, so if we found the match we can skip to the next
                        break

                if not has_intersection:
                    logger.debug("\tno intersection")
                    out_ranges.append((start, end))

                logger.debug(f"\tout_ranges: {out_ranges}")

            return out_ranges

    def __repr__(self):
        strings = [f"({x[0]}, {x[1]}) : ({y[0]}, {y[1]})" for x, y in self.map_parts]
        return "{" + "\n".join(strings) + "}"
