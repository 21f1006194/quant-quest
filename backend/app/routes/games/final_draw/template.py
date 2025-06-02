import requests
import json
from time import sleep

BASE_URL = "%%API_BASE_URL%%"
API_TOKEN = "%%API_TOKEN%%"


class GamePlay:
    def __init__(self):
        self.session_id = None
        self.last_pick = None
        self.headers = {
            "X-API-Token": API_TOKEN,
            "Content-Type": "application/json",
        }

    def get_game_data(self):
        response = requests.get(
            f"{BASE_URL}/play/final_draw",
            headers=self.headers,
        )
        sleep(0.3)  # Required to avoid rate limit -- Don't change
        if response.status_code == 200 or response.status_code == 201:
            self.last_pick = response.json()["last_pick"]
            return response.json()
        else:
            raise Exception("Failed to get game data")

    def start(self):
        payload = {}
        response = requests.post(
            f"{BASE_URL}/play/final_draw",
            headers=self.headers,
            data=json.dumps(payload),
        )
        sleep(0.3)  # Required to avoid rate limit -- Don't change
        if response.status_code == 200 or response.status_code == 201:
            self.session_id = response.json()["session_id"]
            self.last_pick = response.json()["last_pick"]
            return {"message": "Game has been started. Place your bet."}
        else:
            raise Exception("Failed to start game")

    def next(self, choice):
        if choice not in ["select", "skip"]:
            raise Exception("Choice must be 'select' or 'skip'")
        payload = {
            "session_id": self.session_id,
            "choice": choice,
        }
        response = requests.patch(
            f"{BASE_URL}/play/final_draw",
            headers=self.headers,
            data=json.dumps(payload),
        )
        sleep(0.2)  # Required to avoid rate limit -- Don't change
        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            self.last_pick = result["last_pick"]
            return result
        else:
            print(response)
            print(response.text)
            raise Exception("Failed to bet")


if __name__ == "__main__":
    print("Playing the Final Draw game...")
    game = GamePlay()

    # STEP 1: Inspect game setup
    # game_data = game.get_game_data()
    # print("Game Info:", game_data)

    # STEP 2: Start the game (start session)
    # print(game.start())

    # STEP 3: Place your bet (select or skip)
    # choice = "select"
    # result = game.next(choice)
    # print("Game Result:", result)
