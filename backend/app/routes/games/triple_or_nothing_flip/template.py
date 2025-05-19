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
        response = requests.get(
            f"{BASE_URL}/play/triple_or_nothing",
            headers=self.headers,
        )
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception("Failed to get game data")

    def play(self):
        response = requests.post(
            f"{BASE_URL}/play/triple_or_nothing",
            headers=self.headers,
            data=json.dumps({}),
        )
        sleep(0.2)
        if response.status_code in [200, 201]:
            self.session_id = response.json()["session_id"]
            return response.json()
        else:
            raise Exception("Failed to start game")

    def bet(self, choice, step, bet_amount):
        payload = {
            "session_id": self.session_id,
            "choice": choice,
            "bet_amount": bet_amount,
            "step": step,
        }
        response = requests.patch(
            f"{BASE_URL}/play/triple_or_nothing",
            headers=self.headers,
            data=json.dumps(payload),
        )
        sleep(0.2)
        if response.status_code in [200, 201]:
            result = response.json()
            self.toss_result = result["toss_result"]
            return result
        else:
            raise Exception("Failed to bet")


if __name__ == "__main__":
    print("Playing the triple or nothing flip game...")
    #game = GamePlay()
    #print(game.get_game_data())
    #print(game.play())
    # Example:
    # print(game.bet("H", 1, 10))  # First Flip
    # print(game.bet("H", 2, 10))  # Optional Second Flip
