import random

segments = [
    {"color": "Red", "angle": 36, "prob": 0.10, "payout": 100},
    {"color": "Blue", "angle": 54, "prob": 0.15, "payout": 75},
    {"color": "Green", "angle": 90, "prob": 0.25, "payout": 50},
    {"color": "Yellow", "angle": 108, "prob": 0.30, "payout": 25},
    {"color": "Purple", "angle": 72, "prob": 0.20, "payout": 40},
]

def spin_wheel():
    colors = [seg["color"] for seg in segments]
    weights = [seg["prob"] for seg in segments]
    result = random.choices(colors, weights=weights, k=1)[0]
    return result

def get_segment_by_color(color):
    return next((seg for seg in segments if seg["color"].lower() == color.lower()), None)

def get_expected_value():
    return sum(seg["prob"] * seg["payout"] for seg in segments)
