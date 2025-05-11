import random
from typing import List
from app.services import GameService

SUITS = ["S", "C", "D", "H"]  # Spades, Clubs, Diamonds, Hearts
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
RANK_VALUES = {r: i for i, r in enumerate(RANKS, start=2)}


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
        return sum(RANK_VALUES[card.rank] for card in hand)

    def result(self, bet_details):
        total_bet = bet_details["base_bet"] + bet_details["raise_bet"]
        if bet_details["player_hand_value"] > bet_details["house_hand_value"]:
            return total_bet * self.payout
        else:
            return 0.0
