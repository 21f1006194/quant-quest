from flask_restful import Resource
from flask import Blueprint, request, jsonify
from flask_restful import Api
from app.utils.auth import admin_required
from app.models.gameplay import Game
from app import db

admin_bp = Blueprint("admin", __name__)
api = Api(admin_bp)


class AdminAPI(Resource):
    @admin_required
    def get(self):
        """Get admin dashboard data"""
        return {"message": "Admin dashboard data"}, 200


class AdminDashboardAPI(Resource):
    @admin_required
    def get(self):
        """Get admin dashboard data"""
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
        return data, 200

@admin_bp.route('/admin/games/<int:game_id>/toggle', methods=['POST'])
@admin_required
def toggle_game_status(game_id):
    """Toggle the active status of a game."""
    game = Game.query.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404

    data = request.get_json()
    is_active = data.get("isActive")
    if is_active is None:
        return jsonify({"error": "Missing 'isActive' field"}), 400

    game.is_active = is_active
    db.session.commit()
    return jsonify({"message": "Game status updated", "game": {"id": game.id, "name": game.name, "isActive": game.is_active}})

api.add_resource(AdminAPI, "/admin")
api.add_resource(AdminDashboardAPI, "/admin/dashboard")
