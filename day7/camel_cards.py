class Game:
    def __init__(self, hands_path: str, joker_card: str):
        self.hands_path = hands_path
        self.hands = []

        with open(self.hands_path, "r", encoding="utf8") as f:
            for line in f:
                line = line.strip()
                cards, bid = line.split(" ")

                self.hands.append(Hand(list(cards), int(bid), joker_card))

    def get_hands(self):
        return self.hands

    def get_winnings(self, show_hands: bool = False):
        winnings = 0
        sorted_hands = sorted(self.hands)
        for rank, hand in enumerate(sorted_hands, start=1):
            if show_hands:
                print(rank, hand, hand.type)
            winnings += hand.bid * rank
        return winnings


class Hand:
    # card_types = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    # part 2
    card_types = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
    types = [
        "Five of a kind",
        "Four of a kind",
        "Full house",
        "Three of a kind",
        "Two pair",
        "One pair",
        "High card",
    ]

    def __init__(self, cards: list[str], bid: int, joker_card: str):
        self.cards = cards
        self.bid = bid

        # count cards
        self.freqs = {}
        for card in self.cards:
            if card not in self.freqs:
                self.freqs[card] = 1
            else:
                self.freqs[card] += 1

        self.type = self._get_type_info(joker_card)

        self.card_values = dict(
            zip(Hand.card_types, reversed(range(len(Hand.card_types))))
        )

        self.type_values = dict(zip(Hand.types, reversed(range(len(Hand.types)))))

    def __repr__(self):
        return f"{''.join(self.cards)} {self.bid}"

    def _get_type_info(self, joker_card: str = "") -> str:
        sorted_freqs = sorted(self.freqs.items(), key=lambda x: x[1])
        most_common = sorted_freqs[-1]
        second_most = sorted_freqs[-2] if len(sorted_freqs) > 1 else None

        margin = 0

        if len(sorted_freqs) > 1 and joker_card in self.freqs:
            margin = self.freqs[joker_card]

            if most_common[0] == joker_card:
                most_common = sorted_freqs[-2] if len(sorted_freqs) > 1 else most_common
                second_most = sorted_freqs[-3] if len(sorted_freqs) > 2 else most_common

            elif second_most is not None and second_most[0] == joker_card:
                second_most = sorted_freqs[-3] if len(sorted_freqs) > 2 else most_common
                # deal with joker as most common

        # assert len(sorted_freqs) == 1 or most_common[1] >= second_most[1], "Oh oh"

        if most_common[1] + margin == 5:
            type_ = "Five of a kind"
        elif most_common[1] + margin == 4:
            type_ = "Four of a kind"
        elif (
            most_common[1] + margin == 3
            and second_most is not None
            and second_most[1] == 2
        ) or (
            most_common[1] == 3
            and second_most is not None
            and second_most[1] + margin == 2
        ):
            type_ = "Full house"
        elif most_common[1] + margin == 3:
            type_ = "Three of a kind"
        elif (
            most_common[1] + margin == 2
            and second_most is not None
            and second_most[1] == 2
        ) or (
            most_common[1] == 2
            and second_most is not None
            and second_most[1] + margin == 2
        ):
            type_ = "Two pair"
        elif most_common[1] + margin == 2:
            type_ = "One pair"
        else:
            type_ = "High card"

        return type_

    def _ordering_rule(self, other_cards: list[str]) -> int:
        for i in range(5):
            if self.cards[i] == other_cards[i]:
                continue
            elif self.card_values[self.cards[i]] > self.card_values[other_cards[i]]:
                # self is bigger
                return 1
            else:
                return -1

        return 0

    # need __lt__ to sort objects
    def __lt__(self, other):
        if self.type_values[self.type] < self.type_values[other.type]:
            return True
        elif self.type_values[self.type] > self.type_values[other.type]:
            return False
        else:
            return self._ordering_rule(other.cards) < 0
