# This is the template code for playing the game.
import requests
import json
from time import sleep

BASE_URL = "%%API_BASE_URL%%"
API_TOKEN = "%%API_TOKEN%%"


class GamePlay:
    def __init__(self):
        self.session_id = None
        self.bet_id = None
        self.hand = None
        self.house_hand = None
        self.current_balance = None
        self.headers = {
            "X-API-Token": API_TOKEN,
            "Content-Type": "application/json",
        }

    def start_game(self):
        """Start a new game session"""
        payload = {}
        response = requests.post(
            f"{BASE_URL}/play/three_card_poker",
            headers=self.headers,
            data=json.dumps(payload),
        )
        sleep(0.2)  # Required to avoid rate limit -- Don't change
        if response.status_code == 200 or response.status_code == 201:
            self.session_id = response.json()["session_id"]
            return self.session_id
        else:
            raise Exception("Failed to start game")

    def place_base_bet(self, base_bet):
        """Place the initial base bet"""
        payload = {"session_id": self.session_id, "base_bet": base_bet}
        response = requests.patch(
            f"{BASE_URL}/play/three_card_poker",
            headers=self.headers,
            data=json.dumps(payload),
        )
        sleep(0.3)  # Required to avoid rate limit -- Don't change
        if response.status_code == 200 or response.status_code == 201:
            data = response.json()
            self.bet_id = data["bet_id"]
            self.hand = data["hand"]
            return data
        else:
            raise Exception("Failed to place base bet")

    def raise_or_fold(self, raise_bet=0):
        """Make a decision to raise or fold"""
        payload = {
            "session_id": self.session_id,
            "bet_id": self.bet_id,
            "raise_bet": raise_bet,
        }
        response = requests.patch(
            f"{BASE_URL}/play/three_card_poker",
            headers=self.headers,
            data=json.dumps(payload),
        )
        sleep(0.3)  # Required to avoid rate limit -- Don't change
        if response.status_code == 200 or response.status_code == 201:
            data = response.json()
            self.house_hand = data.get("house_hand")
            self.current_balance = data.get("current_balance")
            return data
        else:
            raise Exception("Failed to raise or fold")


if __name__ == "__main__":
    game = GamePlay()
    # # 1. Start a new game
    # game.start_game()
    # loop through 5 rounds
    # # 2. Place base bet
    # game.place_base_bet(<base_bet>)
    # # 3. Make a decision to raise or fold
    # game.raise_or_fold(raise_bet=<raise_bet>)
