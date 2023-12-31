from enum import Enum


class TileType(Enum):
    HOODWINK = "S"
    PIPE_VERTICAL = "|"
    PIPE_HORZONTAL = "-"
    PIPE_NE = "L"
    PIPE_NW = "J"
    PIPE_SE = "F"
    PIPE_SW = "7"
    GROUND = "."
    VISITED = "^"


class MapTile:
    neighbors_increments = {
        TileType.HOODWINK: [(1, 0), (0, 1), (-1, 0), (0, -1)],
        TileType.PIPE_VERTICAL: [(1, 0), (-1, 0)],  # |
        TileType.PIPE_HORZONTAL: [(0, 1), (0, -1)],  # -
        TileType.PIPE_NE: [(-1, 0), (0, 1)],  # L
        TileType.PIPE_NW: [(-1, 0), (0, -1)],  # J
        TileType.PIPE_SE: [(1, 0), (0, 1)],  # F
        TileType.PIPE_SW: [(1, 0), (0, -1)],  # 7
        TileType.GROUND: [],
    }

    def __init__(self, symbol: str, position: tuple[int, int]):
        self.symbol = TileType(symbol)
        self.row, self.col = position

        self.neighbors_increments = MapTile.neighbors_increments[self.symbol]

    def __repr__(self) -> str:
        if isinstance(self.symbol, TileType):
            return self.symbol.value
        return self.symbol

    def get_neighbors_increments(self) -> list[tuple[int, int]]:
        return self.neighbors_increments

    def __hash__(self) -> int:
        return hash((self.row, self.col))


class PipesMap:
    def __init__(self, map_path: str):
        self.map_path = map_path
        self.map = []

        count = 0
        with open(self.map_path, "r", encoding="utf8") as f:
            for row_idx, line in enumerate(f):
                line = line.strip()
                row = [MapTile(c, (row_idx, col_idx)) for col_idx, c in enumerate(line)]
                self.map.append(row)
                count += 1

        self.num_rows = count
        self.num_cols = len(self.map[0])

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.map[row][col].symbol == TileType.HOODWINK:
                    self.start = self.map[row][col]
                    break

    def __repr__(self) -> str:
        return "\n".join(["".join([str(r) for r in row]) for row in self.map])

    def get_valid_neighbors(self, tile: MapTile) -> list[MapTile]:
        neighbors = []
        for x, y in tile.get_neighbors_increments():
            if 0 <= tile.row + x < self.num_rows and 0 <= tile.col + y < self.num_cols:
                if tile == self.start:
                    # this may be the worst way to do this btw
                    if self.start in self.get_valid_neighbors(
                        self.map[tile.row + x][tile.col + y]
                    ):
                        neighbors.append(self.map[tile.row + x][tile.col + y])
                elif self.map[tile.row + x][tile.col + y].symbol != TileType.GROUND:
                    neighbors.append(self.map[tile.row + x][tile.col + y])

        return neighbors

    def run_dfs(self, start: MapTile):
        """Find the big loop"""
        # can we do this without the stack AND the map giving parent info?
        stack = [(start, None)]
        visited = set()
        #              node : parent)
        visited_map = {start: None}
        start_found = False

        # stop when we find start again
        while not start_found:
            curr, parent = stack.pop()

            # explore curr
            visited.add(curr)
            visited_map[curr] = parent

            for n in self.get_valid_neighbors(curr):
                if n not in visited:
                    stack.append((n, curr))
                elif n == start and visited_map[curr] != start:
                    start_found = True
                    break

        # get the loop (path from start back start)
        path = [start]
        parent = curr

        while parent is not None:
            path.append(parent)
            parent = visited_map[parent]

        return path

    # imagine doing bfs

    # def run_bfs(self, start: MapTile) -> list[MapTile, int]:
    #     #    (node, steps_from_start)
    #     q = [(start, 0)]
    #     distances = []
    #     visited = set()

    #     while len(q) > 0:
    #         # print(f"Visited: {visited}")
    #         # print(f"Queue: {q}")
    #         next_, steps_from_start = q.pop(0)
    #         distances.append((next_, steps_from_start))

    #         # explore next_
    #         visited.add(next_)
    #         next_.symbol = str(steps_from_start)
    #         for n in self.get_valid_neighbors(next_):
    #             if n not in visited:
    #                 q.append((n, steps_from_start + 1))

    #     return sorted(distances, key=lambda x: x[1], reverse=True)

    def is_inside(self, tile: MapTile, pipe_loop: list[MapTile]) -> bool:
        # Ray casting
        # https://gist.github.com/inside-code-yt/7064d1d1553a2ee117e60217cfd1d099
        intersec_points = 0
        xp, yp = tile.row, tile.col

        for i in range(len(pipe_loop) - 1):
            x1, y1 = pipe_loop[i].row, pipe_loop[i].col
            x2, y2 = pipe_loop[i + 1].row, pipe_loop[i + 1].col

            if (yp < y1) != (yp < y2) and xp < x1 + ((yp - y1) / (y2 - y1)) * (x2 - x1):
                intersec_points += 1

        return intersec_points % 2 != 0

    def count_tiles_inside(self, pipe_loop: list[MapTile]) -> int:
        count = 0
        for row in self.map:
            for tile in row:
                if tile not in pipe_loop:
                    if self.is_inside(tile, pipe_loop):
                        tile.symbol = "I"
                        count += 1
                    else:
                        tile.symbol = "O"

        return count
