import requests
import json
from time import sleep

BASE_URL = "%%API_BASE_URL%%"
API_TOKEN = "%%API_TOKEN%%"

class GamePlay:
    def __init__(self):
        self.session_id = None
        self.game_data = None
        self.headers = {
            "X-API-Token": API_TOKEN,
            "Content-Type": "application/json",
        }

    def get_metadata(self):
        response = requests.get(
            f"{BASE_URL}/play/three_doors_maze",
            headers=self.headers,
        )
        if response.status_code == 200:
            return response.json()
        raise Exception("Failed to get game metadata")

    def start_game(self):
        response = requests.post(
            f"{BASE_URL}/play/three_doors_maze",
            headers=self.headers,
            data=json.dumps({}),
        )
        sleep(0.2)
        if response.status_code in (200, 201):
            data = response.json()
            self.session_id = data["session_id"]
            self.game_data = data["game_data"]
            return data
        raise Exception(f"Failed to start game: {response.text}")

    def make_choice(self, door: str, bet_amount: float):
        if not self.session_id:
            raise Exception("No active session")
        payload = {
            "session_id": self.session_id,
            "choice": door,
            "bet_amount": bet_amount,
        }
        response = requests.patch(
            f"{BASE_URL}/play/three_doors_maze",
            headers=self.headers,
            data=json.dumps(payload),
        )
        sleep(0.2)
        if response.status_code in (200, 201):
            data = response.json()
            self.game_data = data["game_data"]
            return data
        raise Exception(f"Failed to make choice: {response.text}")

    def play_until_win(self, bet_amount=10):
        print("Starting new game...")
        self.start_game()
        while self.game_data and self.game_data["current_room"] != -1:
            print(f"\nRoom: {self.game_data['current_room']}")
            print(f"Hint: {self.game_data['hint']}")
            print(f"Bayesian Probabilities: {self.game_data['bayesian_probs']}")
            door = max(self.game_data["bayesian_probs"], key=self.game_data["bayesian_probs"].get)
            print(f"Choosing door: {door}")
            result = self.make_choice(door, bet_amount)
            reward = result["reward"]
            print(f"Reward: {reward}")
            if reward > 0:
                print("🎉 Reached the final room and won!")
                break
        print("Game session complete.")

if __name__ == "__main__":
    print("Playing three doors maze game...")
    # game = GamePlay()
    # game.play_until_win(bet_amount=10)
