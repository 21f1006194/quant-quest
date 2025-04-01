from flask import Blueprint, jsonify

common_bp = Blueprint("main", __name__)


@common_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200
