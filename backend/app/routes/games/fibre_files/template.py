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
        f"{BASE_URL}/play/fiber_files",
        headers=headers,
        data=json.dumps(payload),
    )
    
    sleep(0.3)

    if response.status_code in [200, 201]:
        return response.json()
    elif response.status_code == 401:
        raise Exception("Unauthorized")
    elif response.status_code == 400:
        raise Exception("Bad Request")
    elif response.status_code == 429:
        raise Exception("Rate Limit Exceeded, No more requests allowed")
    else:
        print("Error code:", response.status_code)
        print("Error message:", response.text)
        raise Exception("Unknown Error")

if __name__ == "__main__":
    print("Playing Fiber Files game...")
    # Example usage
    result = play(3, 50)  # Choosing suspect 3 with 50 points bet
    print(result)
