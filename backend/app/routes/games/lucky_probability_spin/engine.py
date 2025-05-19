import random

segments = [
    {"color": "Red", "angle": 36, "prob": 0.10, "payout": 100},
    {"color": "Blue", "angle": 54, "prob": 0.15, "payout": 75},
    {"color": "Green", "angle": 90, "prob": 0.25, "payout": 50},
    {"color": "Yellow", "angle": 108, "prob": 0.30, "payout": 25},
    {"color": "Purple", "angle": 72, "prob": 0.20, "payout": 40},
]

def calculate_ev():
    return sum(seg["prob"] * seg["payout"] for seg in segments)

def spin_wheel(user_choice):
    colors = [seg["color"] for seg in segments]
    weights = [seg["prob"] for seg in segments]
    result = random.choices(colors, weights=weights, k=1)[0]
    
    payout = 0
    won = False
    if result == user_choice:
        payout = next(seg["payout"] for seg in segments if seg["color"] == result)
        won = True

    return {
        "result": result,
        "payout": payout,
        "won": won,
        "expected_value": calculate_ev()
    }
