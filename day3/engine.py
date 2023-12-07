from dataclasses import dataclass
import math


@dataclass
class EngineNumber:
    """A number in the engine schematic. start_idx inclusive, end_idx exclusive."""

    value: int
    row: int
    start_idx: int
    end_idx: int

    def __hash__(self):
        return hash((self.value, self.row, self.start_idx, self.end_idx))

    def get_neighbors_coords(
        self, max_rows: int, max_cols: int
    ) -> set[tuple[int, int]]:
        neighbors = set()

        increments = [
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1),
        ]
        points = [
            (x, y)
            for x, y in zip(
                [self.row] * (int(math.log10(self.value)) + 1),
                range(self.start_idx, self.end_idx),
            )
            if 0 <= x < max_rows and 0 <= y < max_cols
        ]

        for row, col in points:
            for row_add, col_add in increments:
                if (
                    0 <= row + row_add < max_rows
                    and 0 <= col + col_add < max_cols
                    and (row + row_add, col + col_add) not in neighbors
                ):
                    neighbors.add((row + row_add, col + col_add))

        # print(points)
        return neighbors

    def is_part_number(self, grid: list[list[str]], symbols: set[str]) -> bool:
        neighbors_coords = self.get_neighbors_coords(
            max_rows=len(grid), max_cols=len(grid[0])
        )
        neighbors = [grid[r][c] for r, c in neighbors_coords]

        for neighbor in neighbors:
            if (isinstance(neighbor, str) and neighbor in symbols) or (
                isinstance(neighbor, EngineAsterisk)
            ):
                return True

        return False


@dataclass
class EngineAsterisk:
    """An asterisk symbol in the engine schematic. start_idx inclusive, end_idx exclusive."""

    row: int
    col: int

    def __hash__(self):
        return hash((self.row, self.col))

    def get_neighbors_coords(
        self, max_rows: int, max_cols: int
    ) -> set[tuple[int, int]]:
        neighbors = set()

        increments = [
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1),
        ]

        for row_add, col_add in increments:
            if (
                0 <= self.row + row_add < max_rows
                and 0 <= self.col + col_add < max_cols
                and (self.row + row_add, self.col + col_add) not in neighbors
            ):
                neighbors.add((self.row + row_add, self.col + col_add))

        # print(points)
        return neighbors

    def is_gear(
        self, grid: list[list[str]], symbols: set[str]
    ) -> tuple[bool, list[EngineNumber]]:
        neighbors_coords = self.get_neighbors_coords(
            max_rows=len(grid), max_cols=len(grid[0])
        )
        neighbors = set(grid[r][c] for r, c in neighbors_coords)

        adjacent_part_numbers = []
        for neighbor in neighbors:
            if isinstance(neighbor, EngineNumber) and neighbor.is_part_number(
                grid, symbols
            ):
                adjacent_part_numbers.append(neighbor)

        return (len(adjacent_part_numbers) == 2, adjacent_part_numbers)


class EngineSchematic:
    def __init__(self, path):
        self.src_path = path
        self.grid = []
        self.symbols = set()

        number_start = None
        number_end = None
        with open(self.src_path, "r", encoding="utf8") as f:
            for row_idx, line in enumerate(f):
                line = line.strip()
                self.grid.append(list(line))
                for col_idx, char in enumerate(line):
                    if char.isdigit():
                        if number_start is None:
                            number_start = col_idx
                    else:
                        if char == "*":
                            self.grid[row_idx][col_idx] = EngineAsterisk(
                                row_idx, col_idx
                            )

                        if char != "." and char not in self.symbols:
                            # symbol
                            self.symbols.add(char)

                        if number_start is not None:
                            number_end = col_idx
                            # create number
                            num_val = int(line[number_start:number_end])
                            number = EngineNumber(
                                num_val, row_idx, number_start, number_end
                            )

                            for col_idx in range(number_start, number_end):
                                self.grid[row_idx][col_idx] = number

                            number_start = None
                            number_end = None

                if number_start is not None:
                    # last digit of line is a number
                    number_end = len(line)
                    num_val = int(line[number_start:number_end])
                    number = EngineNumber(num_val, row_idx, number_start, number_end)

                    for col_idx in range(number_start, number_end):
                        self.grid[row_idx][col_idx] = number

                    number_start = None
                    number_end = None

    def sum_part_numbers(self) -> int:
        sum_ = 0
        for row in range(len(self.grid)):
            col = 0
            while col < len(self.grid[0]):
                grid_point = self.grid[row][col]
                if isinstance(grid_point, EngineNumber):
                    if grid_point.is_part_number(self.grid, self.symbols):
                        # print(f"Found engine number: {grid_point.value}")
                        # print(f"\trow: {row}, col: {col}")
                        # print(
                        #     f"\tstart_idx: {grid_point.start_idx}, end_idx:"
                        #     f" {grid_point.end_idx}"
                        # )
                        # print(f"\tskipping: {int(math.log10(grid_point.value)) + 1}")
                        sum_ += grid_point.value
                        col += int(math.log10(grid_point.value)) + 1
                        continue
                col += 1

        return sum_

    def sum_gear_ratio(self) -> int:
        sum_ = 0
        for row in range(len(self.grid)):
            for col in range(len(self.grid)):
                grid_point = self.grid[row][col]
                if isinstance(grid_point, EngineAsterisk):
                    is_gear_, adj_parts = grid_point.is_gear(self.grid, self.symbols)

                    if is_gear_:
                        # print("Found gear")
                        # print(f"\trow: {row}, col: {col}")
                        # print(f"\tEngine number 1: {adj_parts[0].value}")
                        # print(f"\tEngine number 2: {adj_parts[1].value}")
                        # print(
                        #     f"\tGear ratio: {adj_parts[0].value * adj_parts[1].value}"
                        # )
                        sum_ += adj_parts[0].value * adj_parts[1].value

        return sum_
