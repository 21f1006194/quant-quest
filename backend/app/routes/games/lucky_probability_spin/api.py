from flask import Blueprint, request, jsonify
from .engine import spin_wheel

bp = Blueprint("lucky_spin", __name__, url_prefix="/api/lucky_spin")

@bp.route("/", methods=["POST"])
def play_spin():
    data = request.get_json()
    user_choice = data.get("choice", "").capitalize()
    if not user_choice:
        return jsonify({"error": "Color choice is required."}), 400
    
    result = spin_wheel(user_choice)
    return jsonify(result)
