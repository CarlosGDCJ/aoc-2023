class Pile:
    def __init__(self, path: str):
        self.input_path = path
        self.cards = []

        with open(self.input_path, "r") as f:
            for line in f:
                card = ScratchCard(line.strip())
                self.cards.append(card)

    def __getitem__(self, idx):
        if isinstance(idx, int):
            return self.cards[idx]
        elif isinstance(idx, slice):
            return self.cards[idx]

    def get_points(self):
        sum_ = 0
        for card in self.cards:
            sum_ += card.get_points()

        return sum_

    def evaluate_scratchcards(self):
        for idx, card in enumerate(self.cards):
            hits = card.get_hits()

            for i in range(1, hits + 1):
                if idx + i < len(self.cards):
                    self.cards[idx + i].num_copies += card.num_copies

        return sum((card.num_copies for card in self.cards))


class ScratchCard:
    def __init__(self, line: str, card_split: str = ":", numbers_split: str = "|"):
        self.numbers_split = numbers_split
        _, numbers = line.split(card_split, maxsplit=1)
        winning, drawn = numbers.split(self.numbers_split, maxsplit=1)
        self.winning, self.drawn = winning.strip().split(), drawn.strip().split()

        self.num_copies = 1

    def __repr__(self):
        return f"{' '.join(self.winning)} {self.numbers_split} {' '.join(self.drawn)}"

    def get_hits(self) -> int:
        return len(set(self.winning).intersection(set(self.drawn)))

    def get_points(self) -> int:
        hits = self.get_hits()

        if hits == 0:
            return 0

        return 2 ** (hits - 1)
