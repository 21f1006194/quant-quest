# This is the template code for playing the game.
import requests
import json

BASE_URL = "%%API_BASE_URL%%"
API_TOKEN = "%%API_TOKEN%%"

def play():
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    choice = input("Choose a color (Red, Blue, Green, Yellow, Purple): ")

    payload = {"choice": choice}
    response = requests.post(f"{BASE_URL}/api/lucky_probability_spin/play", headers=headers, data=json.dumps(payload))
    data = response.json()
    
    if "error" in data:
        print("Error:", data["error"])
    else:
        print("Wheel landed on:", data["result"])
        print("Your Choice:", data["your_choice"])
        print("You won!" if data["win"] else "Sorry, try again!")
        print("Payout:", data["payout"])
        print("Expected Value:", data["expected_value"])

if __name__ == "__main__":
    play()
