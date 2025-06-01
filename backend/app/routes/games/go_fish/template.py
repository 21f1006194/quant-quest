# This is the template code for playing the game.
import requests
import json
from time import sleep

BASE_URL = "%%API_BASE_URL%%"
API_TOKEN = "%%API_TOKEN%%"


class GamePlay:
    def __init__(self):
        self.session_id = None
        self.initial_cards = None
        self.revealed_cards = []
        self.headers = {
            "X-API-Token": API_TOKEN,
            "Content-Type": "application/json",
        }

    def start_game(self):
        """Start a new game session"""
        payload = {}
        response = requests.post(
            f"{BASE_URL}/play/go_fish",
            headers=self.headers,
            data=json.dumps(payload),
        )
        sleep(0.3)  # Required to avoid rate limit -- Don't change
        if response.status_code == 200 or response.status_code == 201:
            self.session_id = response.json()["session_id"]
            self.initial_cards = response.json()["initial_cards"]
            return self.session_id
        else:
            raise Exception("Failed to start game")

    def fish(self, bet_amount, choice):
        """Place the initial base bet"""
        payload = {
            "session_id": self.session_id,
            "bet_amount": bet_amount,
            "choice": choice,
        }
        response = requests.patch(
            f"{BASE_URL}/play/go_fish",
            headers=self.headers,
            data=json.dumps(payload),
        )
        sleep(0.3)  # Required to avoid rate limit -- Don't change
        if response.status_code == 200 or response.status_code == 201:
            data = response.json()
            self.fishing_count = data["fishing_count"]
            self.result = data["result"]
            self.current_balance = data["current_balance"]
            self.revealed_cards.append(data["result"]["card"])
            return data
        else:
            raise Exception("Failed to place base bet")


if __name__ == "__main__":
    game = GamePlay()
    # # 1. Start a new game
    # game.start_game()
    # print(game.initial_cards)
    # # # 2. Place the bet
    # choice = "QH"
    # bet_amount = 50
    # game.fish(bet_amount, choice)
    # print(game.revealed_cards)
