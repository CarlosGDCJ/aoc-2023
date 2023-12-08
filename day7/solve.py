from camel_cards import Game


def main():
    input_path = "input.txt"

    game = Game(input_path, "J")

    print(f"Total winnings: {game.get_winnings(show_hands=True)}")


if __name__ == "__main__":
    main()
