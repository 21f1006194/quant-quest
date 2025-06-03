# This is the template code for playing the game.
import requests
import json
from time import sleep

BASE_URL = "%%API_BASE_URL%%"
API_TOKEN = "%%API_TOKEN%%"


class GamePlay:
    def __init__(self):
        self.session_id = None
        self.assets = None
        self.headers = {
            "X-API-Token": API_TOKEN,
            "Content-Type": "application/json",
        }

    def get_game_data(self):
        response = requests.get(
            f"{BASE_URL}/play/knapsack",
            headers=self.headers,
        )
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            raise Exception("Failed to get game data")

    def play(self):
        payload = {}
        response = requests.post(
            f"{BASE_URL}/play/knapsack",
            headers=self.headers,
            data=json.dumps(payload),
        )
        sleep(0.2)  # Required to avoid rate limit -- Dont change
        if response.status_code == 200 or response.status_code == 201:
            self.session_id = response.json()["session_id"]
            self.assets = response.json()["assets"]
            return self.assets
        else:
            raise Exception("Failed to start game")

    def verify_sack(self, sack):
        # TODO: check all fields
        return True

    def trade(self, sack):
        if not self.verify_sack(sack):
            raise Exception("Wrong format for sack")

        payload = {"session_id": self.session_id, "sack": sack}
        response = requests.patch(
            f"{BASE_URL}/play/knapsack",
            headers=self.headers,
            data=json.dumps(payload),
        )
        sleep(0.2)  # Required to avoid rate limit -- Dont change
        if response.status_code == 200 or response.status_code == 201:
            self.result = response.json()["result"]
            self.current_balance = response.json()["current_balance"]
            return response.json()
        else:
            print(response)
            print(response.text)
            raise Exception("Failed to bet")


if __name__ == "__main__":
    game = GamePlay()
    # TODO: fill
