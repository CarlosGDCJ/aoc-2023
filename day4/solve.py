from scratchcards import Pile


def main():
    input_path = "input.txt"
    # input_path = "simple_input.txt"
    # Part 1
    pile = Pile(input_path)
    print(f"Number of points in pile: {pile.get_points()}")

    # Part 2
    print(f"Total scratchcards after evaluation: {pile.evaluate_scratchcards()}")


if __name__ == "__main__":
    main()
