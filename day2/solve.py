# accidental part 1 solution that solves part 2 gg
def get_min_by_color(rounds):
    """Return the minimum number of cubes in order for this round to be possible"""
    mins = {
        "red": 0,
        "green": 0,
        "blue": 0,
    }

    for round_ in rounds:
        for cubes in round_:
            num_cubes, color = cubes.split()

            # we know the input, could be lazy with no verifications here
            # mins[color] = max(mins[color], int(num_cubes))

            if color in mins:
                if int(num_cubes) > mins[color]:
                    mins[color] = int(num_cubes)

    return mins


def main():
    input_file = "input.txt"

    # Load data
    games = []
    with open(input_file, "r", encoding="utf8") as f:
        for line in f:
            game_id, game_info = line.strip().split(":", maxsplit=1)
            game_id = int(game_id[5:])

            game_info = game_info.strip().split(";")
            rounds = [
                [s.strip() for s in round_info.split(",")] for round_info in game_info
            ]

            games.append((game_id, rounds))

    # Verify if each game is possible
    # The game will be possible if the sum of the cubes in a set doesn't exceed a maximum

    sum_possible = 0
    sum_power = 0
    for game in games:
        game_id, rounds = game
        mins = get_min_by_color(rounds)

        # part 1
        if mins["red"] <= 12 and mins["green"] <= 13 and mins["blue"] <= 14:
            sum_possible += game_id

        # part 2
        power = mins["red"] * mins["green"] * mins["blue"]
        sum_power += power

    print(f"Part 1:")
    print(f"The sum of possible games is: {sum_possible}")
    print(f"Part 2:")
    print(f"The sum of the power of the minimum sets of cubes is {sum_power}")


if __name__ == "__main__":
    main()
