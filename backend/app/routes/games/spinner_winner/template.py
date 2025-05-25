# This is the template code for playing the game.
import requests
import json
from time import sleep

BASE_URL = "%%API_BASE_URL%%"
API_TOKEN = "%%API_TOKEN%%"


class GamePlay:
    def __init__(self):
        self.session_id = None
        self.wheel = None
        self.headers = {
            "X-API-Token": API_TOKEN,
            "Content-Type": "application/json",
        }

    def get_game_data(self):
        response = requests.get(
            f"{BASE_URL}/play/spinner_winner",
            headers=self.headers,
        )
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            raise Exception("Failed to get game data")

    def play(self):
        payload = {}
        response = requests.post(
            f"{BASE_URL}/play/spinner_winner",
            headers=self.headers,
            data=json.dumps(payload),
        )
        sleep(0.2)  # Required to avoid rate limit -- Dont change
        if response.status_code == 200 or response.status_code == 201:
            self.session_id = response.json()["session_id"]
            self.wheel = response.json()["wheel"]
            return self.wheel
        else:
            raise Exception("Failed to start game")

    def bet(self, color, bet_amount):
        payload = {
            "session_id": self.session_id,
            "choice": color,
            "bet_amount": bet_amount,
        }
        response = requests.patch(
            f"{BASE_URL}/play/spinner_winner",
            headers=self.headers,
            data=json.dumps(payload),
        )
        sleep(0.2)  # Required to avoid rate limit -- Dont change
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            print(response)
            print(response.text)
            raise Exception("Failed to bet")


if __name__ == "__main__":
    game = GamePlay()
    # game.play()
    # print(game.wheel)
    # game.bet("Red", 30)
    # print(game.wheel)
