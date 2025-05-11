# This is the template code for playing the game.
import requests
import json

BASE_URL = "%%API_BASE_URL%%"
API_TOKEN = "%%API_TOKEN%%"

# New game
# curl --location --request POST 'http://localhost:5000/play/three_card_poker' \
# --header 'X-API-Token: 2.SkohXTszTArmWJqKGPUmQ4kuUk7rWiWnR9Jix6S1vY8' \
# --header 'Content-Type: application/json' \
# --data-raw '{
# }'

## REsponse:
# {
#     "session_id": 2
# }
#

## Base Bet
# curl --location --request PATCH 'http://localhost:5000/play/three_card_poker' \
# --header 'X-API-Token: 2.SkohXTszTArmWJqKGPUmQ4kuUk7rWiWnR9Jix6S1vY8' \
# --header 'Content-Type: application/json' \
# --data-raw '{
#     "session_id": 2,
#     "base_bet": 1000
# }'

# response
# {
#     "bet_id": 4,
#     "hand": [
#         "5C",
#         "2D",
#         "6D"
#     ]
# }

## Raise or Fold
# curl --location --request PATCH 'http://localhost:5000/play/three_card_poker' \
# --header 'X-API-Token: 2.SkohXTszTArmWJqKGPUmQ4kuUk7rWiWnR9Jix6S1vY8' \
# --header 'Content-Type: application/json' \
# --data-raw '{
#     "session_id": 2,
#     "bet_id": 4,
#     "raise_bet": 0
# }'

# Response
# {
#     "bet_id": 4,
#     "hand": [
#         "5C",
#         "2D",
#         "6D"
#     ],
#     "house_hand": [
#         "3D",
#         "JS",
#         "AS"
#     ],
#     "total_bet": 1000,
#     "action": "fold",
#     "payout": 0.0
#     "current_balance": 10000
# }


def play():
    pass


if __name__ == "__main__":
    play()
