import requests
import json
from time import sleep

BASE_URL = "%%API_BASE_URL%%"
API_TOKEN = "%%API_TOKEN%%"

class FibreFilesGame:
    def __init__(self):
        self.session_id = None
        self.headers = {
            "X-API-Token": API_TOKEN,
            "Content-Type": "application/json",
        }

    def start_game(self):
        response = requests.post(
            f"{BASE_URL}/play/fibre_files", headers=self.headers
        )
        sleep(0.2)
        data = response.json()
        self.session_id = data["session_id"]
        return data

    def bet(self, choice, bet_amount):
        payload = {
            "session_id": self.session_id,
            "choice": choice,
            "bet_amount": bet_amount
        }
        response = requests.patch(
            f"{BASE_URL}/play/fibre_files", headers=self.headers, data=json.dumps(payload)
        )
        sleep(0.2)
        return response.json()


if __name__ == "__main__":
    game = FibreFilesGame()
    print(game.start_game())
    # Choice = suspect index (0–9)
    print(game.bet(3, 100))
