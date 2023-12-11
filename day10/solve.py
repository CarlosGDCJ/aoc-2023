from pipes import PipesMap


def main():
    input_path = "simple_input.txt"
    input_path = "simple_input2.txt"
    input_path = "simple_input3.txt"
    input_path = "simple_input4.txt"
    input_path = "simple_input5.txt"
    input_path = "input.txt"
    pipes_map = PipesMap(input_path)
    loop = pipes_map.run_dfs(start=pipes_map.start)
    print(f"Loop length: {len(loop)}")
    print(f"Half of loop length: {len(loop) // 2}")

    num_tiles_inside = pipes_map.count_tiles_inside(loop)
    print(f"Number of tiles inside: {num_tiles_inside}")
    # print(pipes_map)


if __name__ == "__main__":
    main()
