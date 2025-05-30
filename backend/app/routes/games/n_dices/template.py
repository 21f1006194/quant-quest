import requests
import json
from time import sleep

BASE_URL = "%%API_BASE_URL%%"
API_TOKEN = "%%API_TOKEN%%"


class GamePlay:
    def __init__(self):
        self.session_id = None
        self.n = None
        self.headers = {
            "X-API-Token": API_TOKEN,
            "Content-Type": "application/json",
        }

    def get_game_data(self):
        response = requests.get(
            f"{BASE_URL}/play/n_dices",
            headers=self.headers,
        )
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            raise Exception("Failed to get game data")

    def play(self):
        payload = {}
        response = requests.post(
            f"{BASE_URL}/play/n_dices",
            headers=self.headers,
            data=json.dumps(payload),
        )
        sleep(0.3)  # Required to avoid rate limit -- Don't change
        if response.status_code == 200 or response.status_code == 201:
            self.session_id = response.json()["session_id"]
            self.n = response.json()["n"]
            return {"message": "Roll completed. Place your bet."}
        else:
            raise Exception("Failed to start game")

    def bet(self, choice, bet_amount):
        payload = {
            "session_id": self.session_id,
            "choice": choice,
            "bet_amount": bet_amount,
        }
        response = requests.patch(
            f"{BASE_URL}/play/n_dices",
            headers=self.headers,
            data=json.dumps(payload),
        )
        sleep(0.3)  # Required to avoid rate limit -- Don't change
        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            self.toss_result = result["result"]
            return result
        else:
            print(response)
            print(response.text)
            raise Exception("Failed to bet")


if __name__ == "__main__":
    print("Playing the N Dices game...")
    # game = GamePlay()

    # STEP 1: Get the number of dice
    # print(game.play())
    # print(game.n)

    # STEP 2: Place your bet with amount
    # choice = "30"
    # bet_amount = 20
    # result = game.bet(choice, bet_amount)
    # print("Game Result:", result)
