from flask import Blueprint, jsonify

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard', methods=['GET'])
def get_admin_dashboard():
    # Mock data for demonstration purposes
    data = {
        "totalUsers": 100,
        "totalGames": 10,
        "recentActivities": [
            {"id": 1, "description": "User A joined a game"},
            {"id": 2, "description": "User B scored 100 points"}
        ],
        "games": [
            {"id": 1, "name": "Game 1", "isActive": True},
            {"id": 2, "name": "Game 2", "isActive": False}
        ],
        "gameScores": [
            {"gameId": 1, "gameName": "Game 1", "score": 200},
            {"gameId": 2, "gameName": "Game 2", "score": 150}
        ],
        "rateLimits": [
            {"id": 1, "name": "API Limit", "value": 1000},
            {"id": 2, "name": "Game Limit", "value": 500}
        ]
    }
    return jsonify(data)