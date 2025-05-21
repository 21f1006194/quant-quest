# This is the template code for playing the game.
import requests
import json
from time import sleep

BASE_URL = "%%API_BASE_URL%%"
API_TOKEN = "%%API_TOKEN%%"


class GamePlay:
    def __init__(self):
        self.session_id = None
        self.game_data = None
        self.pnl = None
        self.current_balance = None
        self.headers = {
            "X-API-Token": API_TOKEN,
            "Content-Type": "application/json",
        }

    def get_game_data(self):
        response = requests.get(
            f"{BASE_URL}/play/mean_mangos",
            headers=self.headers,
        )
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            raise Exception("Failed to get game data")

    def play(self):
        payload = {}
        response = requests.post(
            f"{BASE_URL}/play/mean_mangos",
            headers=self.headers,
            data=json.dumps(payload),
        )
        sleep(0.2)  # Required to avoid rate limit -- Dont change
        if response.status_code == 200 or response.status_code == 201:
            self.session_id = response.json()["session_id"]
            self.price_data = response.json()["price_data"]
            self.entry_price = response.json()["entry_price"]
            self.price_data = [
                float(price) for price in self.price_data.split(";") if price
            ]
            return self.price_data
        else:
            raise Exception("Failed to start game")

    def buy(self, qty):
        return self.trade(qty, "buy")

    def sell(self, qty):
        return self.trade(qty, "sell")

    def trade(self, qty, choice):

        if len(choice) != 2:
            raise Exception("Choice must be a two character string")
        payload = {
            "session_id": self.session_id,
            "qty": qty,
            "choice": choice,
        }
        response = requests.patch(
            f"{BASE_URL}/play/mean_mangos",
            headers=self.headers,
            data=json.dumps(payload),
        )
        sleep(0.2)  # Required to avoid rate limit -- Dont change
        if response.status_code == 200 or response.status_code == 201:
            self.game_data = response.json()["game_data"]
            self.pnl = response.json()["pnl"]
            self.current_balance = response.json()["current_balance"]
            return response.json()
        else:
            print(response)
            print(response.text)
            raise Exception("Failed to bet")


if __name__ == "__main__":
    game = GamePlay()
    # past_price = game.play()
    # print(price_data)
    # Analyse the past price data and make a decision to buy() or sell()
    # Do proper money management and decide the qty to buy or sell
