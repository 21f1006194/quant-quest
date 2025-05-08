# This is the template code for playing the ten dice game.
import requests
import json
from time import sleep

BASE_URL = "%%API_BASE_URL%%"
API_TOKEN = "%%API_TOKEN%%"


def play(choice: int, bet_amount: int):
    headers = {
        "X-API-Token": API_TOKEN,
        "Content-Type": "application/json",
    }
    payload = {"choice": choice, "bet_amount": bet_amount}
    response = requests.post(
        f"{BASE_URL}/play/sniper_shot",
        headers=headers,
        data=json.dumps(payload),
    )
    sleep(0.3)
    if response.status_code == 200 or response.status_code == 201:
        return response.json()
    elif response.status_code == 401:
        raise Exception("Unauthorized")
    elif response.status_code == 400:
        raise Exception("Bad Request")
    elif response.status_code == 429:
        raise Exception("Rate Limit Exceeded, No more requests allowed")
    else:
        print("Error code: ", response.status_code)
        print("Error message: ", response.text)
        raise Exception("Error")


if __name__ == "__main__":
    print("Playing the sniper shot game...")
    # Write a script to play the game

    # for i in range(100):
    #     play(i, 10)
