import random
from typing import List

from app.services import GameService

SUITS = ["S", "C", "D", "H"]  # Spades, Clubs, Diamonds, Hearts
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
RANK_VALUES = {r: i for i, r in enumerate(RANKS, start=2)}
HAND_RANKS = {
    "straight_flush": 1,
    "three_of_a_kind": 2,
    "straight": 3,
    "flush": 4,
    "pair": 5,
    "high_card": 6,
}
HAND_TYPES = [
    "Invalid",
    "Straight Flush",
    "Three of a Kind",
    "Straight",
    "Flush",
    "Pair",
    "High Card",
]


class Card:
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank}{self.suit}"

    @classmethod
    def from_str(cls, card_str: str):
        rank = card_str[:-1]
        suit = card_str[-1]
        return cls(rank, suit)


class Deck:
    def __init__(self, remove_cards: List[str] = []):
        self.cards = [Card(rank, suit) for suit in SUITS for rank in RANKS]
        self.cards = [card for card in self.cards if str(card) not in remove_cards]
        random.shuffle(self.cards)

    def draw(self, n: int) -> List[Card]:
        return [self.cards.pop() for _ in range(n)]

    def remaining(self):
        return len(self.cards)


class ThreeCardPoker:
    def __init__(self):
        self.game = GameService.get_game_by_name("three_card_poker")
        self.max_bet_per_session = self.game.max_bets_per_session
        self.config_data = self.game.config_data
        self.payout = self.config_data["payout"]

    def new_game(self):
        deck = Deck()
        session_data = {}
        for i in range(self.max_bet_per_session):
            player_hand = deck.draw(3)
            house_hand = deck.draw(3)
            session_data[i] = {
                "player_hand": [str(card) for card in player_hand],
                "house_hand": [str(card) for card in house_hand],
                "player_hand_value": self.hand_value(player_hand),
                "house_hand_value": self.hand_value(house_hand),
            }
        return session_data

    def hand_value(self, hand: List[Card]):
        values = sorted([RANK_VALUES[card.rank] for card in hand], reverse=True)
        suits = [card.suit for card in hand]
        unique_values = set(values)
        is_flush = len(set(suits)) == 1
        is_straight = len(unique_values) == 3 and max(values) - min(values) == 2

        # Handle special low-Ace straight (A, 2, 3)
        if set(values) == {14, 2, 3}:
            is_straight = True
            values = [3, 2, 1]  # Treat Ace as 1 in this case

        if is_straight and is_flush:
            return (HAND_RANKS["straight_flush"], values)
        elif len(unique_values) == 1:
            return (HAND_RANKS["three_of_a_kind"], values)
        elif is_straight:
            return (HAND_RANKS["straight"], values)
        elif is_flush:
            return (HAND_RANKS["flush"], values)
        elif len(unique_values) == 2:
            # It's a pair + 1 kicker
            pair_value = max(set(values), key=values.count)
            kicker = min(set(values), key=values.count)
            return (HAND_RANKS["pair"], [pair_value, kicker])
        else:
            return (HAND_RANKS["high_card"], values)

    def result(self, bet_details):
        total_bet = bet_details["base_bet"] + bet_details["raise_bet"]
        player_hand_value = tuple(bet_details["player_hand_value"])
        house_hand_value = tuple(bet_details["house_hand_value"])

        if player_hand_value < house_hand_value:
            return total_bet * self.payout
        else:
            return 0.0
