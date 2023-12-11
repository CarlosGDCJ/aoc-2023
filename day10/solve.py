from pipes import PipesMap


def main():
    input_path = "simple_input.txt"
    input_path = "simple_input2.txt"
    input_path = "input.txt"
    pipes_map = PipesMap(input_path)
    res = pipes_map.run_dfs(start=pipes_map.start)
    # print(pipes_map)
    print(f"Loop length: {len(res)}")
    print(f"Half of loop length: {len(res) // 2}")


if __name__ == "__main__":
    main()
