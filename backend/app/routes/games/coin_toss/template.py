import requests
import json
from time import sleep

BASE_URL = "%%API_BASE_URL%%"
API_TOKEN = "%%API_TOKEN%%"


class GamePlay:
    def __init__(self):
        self.session_id = None
        self.toss_result = None
        self.headers = {
            "X-API-Token": API_TOKEN,
            "Content-Type": "application/json",
        }

    def get_game_data(self):
        """Get initial game data and configuration"""
        response = requests.get(
            f"{BASE_URL}/play/coin_toss",
            headers=self.headers,
        )
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            raise Exception("Failed to get game data")

    def play(self):
        """Toss the coin and start a new session"""
        payload = {}
        response = requests.post(
            f"{BASE_URL}/play/coin_toss",
            headers=self.headers,
            data=json.dumps(payload),
        )
        sleep(0.2)  # Required to avoid rate limit -- Don't change
        if response.status_code == 200 or response.status_code == 201:
            self.session_id = response.json()["session_id"]
            return {"message": "Coin has been tossed. Place your bet."}
        else:
            raise Exception("Failed to start game")

    def bet(self, choice, bet_amount):
        """Place your bet (H for Heads, T for Tails)"""
        if choice not in ["H", "T"]:
            raise Exception("Choice must be 'H' or 'T'")
        payload = {
            "session_id": self.session_id,
            "choice": choice,
            "bet_amount": bet_amount,
        }
        response = requests.patch(
            f"{BASE_URL}/play/coin_toss",
            headers=self.headers,
            data=json.dumps(payload),
        )
        sleep(0.2)  # Required to avoid rate limit -- Don't change
        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            self.toss_result = result["toss_result"]
            return result
        else:
            print(response)
            print(response.text)
            raise Exception("Failed to bet")


if __name__ == "__main__":
    print("Playing the Coin Toss game...")
    # game = GamePlay()

    # STEP 1: Inspect game setup
    # game_data = game.get_game_data()
    # print("Game Info:", game_data)

    # STEP 2: Toss the coin (start session)
    # print(game.play())

    # STEP 3: Place your bet (H or T) with amount
    # choice = "H"
    # bet_amount = 20
    # result = game.bet(choice, bet_amount)
    # print("Game Result:", result)
