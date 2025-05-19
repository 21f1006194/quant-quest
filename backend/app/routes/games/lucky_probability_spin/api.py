from flask import Blueprint, request, jsonify
from .engine import spin_wheel, get_segment_by_color, get_expected_value

bp = Blueprint("lucky_probability_spin", __name__, url_prefix="/api/lucky_probability_spin")

@bp.route("/play", methods=["POST"])
def play_game():
    data = request.get_json()
    user_color = data.get("choice")

    if not user_color:
        return jsonify({"error": "No color chosen"}), 400

    segment = get_segment_by_color(user_color)
    if not segment:
        return jsonify({"error": "Invalid color"}), 400

    result = spin_wheel()
    win = result.lower() == user_color.lower()
    payout = segment["payout"] if win else 0
    ev = get_expected_value()

    return jsonify({
        "result": result,
        "your_choice": user_color,
        "win": win,
        "payout": payout,
        "expected_value": ev
    })
