import random
from typing import List

from app.services import GameService

SUITS = ["S", "C", "D", "H"]  # Spades, Clubs, Diamonds, Hearts
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


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


class GoFish:
    def __init__(self):
        self.game = GameService.get_game_by_name("go_fish")
        self.max_bet_per_session = self.game.max_bets_per_session
        self.config_data = self.game.config_data
        self.min_bet_amount = self.config_data["min_bet_amount"]
        self.half_guess_payout = self.config_data["half_guess_payout"]
        self.full_guess_payout = self.config_data["full_guess_payout"]

    def new_game(self):
        deck = Deck()
        session_data = {}
        initial_cards = deck.draw(7)
        session_data["initial_cards"] = [str(card) for card in initial_cards]
        fish_cards = deck.draw(self.max_bet_per_session)
        session_data["fish_cards"] = [str(card) for card in fish_cards]
        return session_data

    def get_result(
        self, session_data: dict, fishing_attempt: int, guess: str, bet_amount: int
    ):
        """Check if the card is in the fish cards

        Args:
            session_data (dict): The session data
            fishing_attempt (int): Index of the card being attempted to be fished
            guess (str): The guess of the player
            bet_amount (int): The amount of the bet
        """
        if bet_amount < self.min_bet_amount:
            raise ValueError(
                f"Invalid bet amount, minimum bet amount is {self.min_bet_amount}"
            )
        if fishing_attempt < 1 or fishing_attempt > len(session_data["fish_cards"]):
            raise ValueError(
                f"Invalid fishing attempt, only {len(session_data['fish_cards'])} attempts allowed, this is attempt {fishing_attempt}"
            )
        revealing_card = session_data["fish_cards"][fishing_attempt - 1]
        if guess == revealing_card:
            return {
                "result": "Full guess win",
                "payout": bet_amount * self.full_guess_payout,
                "card": revealing_card,
            }
        elif guess[:-1] == revealing_card[:-1] or guess[-1] == revealing_card[-1]:
            return {
                "result": "Half guess win",
                "payout": bet_amount * self.half_guess_payout,
                "card": revealing_card,
            }
        else:
            return {
                "result": "No win",
                "payout": 0,
                "card": revealing_card,
            }
