from flask_restful import Resource
from flask import Blueprint, request
from flask_restful import Api
from app.models import User, Game, GameSession
from app.utils.auth import admin_required
from app import db

admin_bp = Blueprint("admin", __name__)
api = Api(admin_bp)

class AdminAPI(Resource):
    @admin_required
    def get(self):
        """Get admin dashboard data"""
        return {"message": "Admin dashboard data"}, 200
class ManageGamesAPI(Resource):
    @admin_required
    def get(self):
        """Get all games"""
        games = Game.query.all()
        return {"games": [game.name for game in games]}, 200

    @admin_required
    def post(self):
        """Add a new game"""
        data = request.get_json()
        name = data.get("name")
        description = data.get("description")
        game_type = data.get("type")

        if not name or not game_type:
            return {"error": "Name and type are required"}, 400

        if Game.query.filter_by(name=name).first():
            return {"error": "Game with this name already exists"}, 400

        game = Game(name=name, description=description, type=game_type)
        db.session.add(game)
        db.session.commit()
        return {"message": "Game added successfully", "game": game.name}, 201

    @admin_required
    def delete(self):
        """Delete a game"""
        data = request.get_json()
        game_id = data.get("id")

        game = Game.query.get(game_id)
        if not game:
            return {"error": "Game not found"}, 404

        db.session.delete(game)
        db.session.commit()
        return {"message": "Game deleted successfully"}, 200


class PlayerStatsAPI(Resource):
    @admin_required
    def get(self):
        """Get player stats"""
        players = User.query.filter_by(is_admin=False).all()
        stats = [
            {
                "username": player.username,
                "email": player.email,
                "games_played": len(player.game_sessions),
            }
            for player in players
        ]
        return {"player_stats": stats}, 200


class RateLimitAPI(Resource):
    @admin_required
    def get(self):
        """View rate limits (mock implementation)"""
        return {"rate_limits": {"requests_per_minute": 100}}, 200

    @admin_required
    def post(self):
        """Update rate limits (mock implementation)"""
        data = request.get_json()
        new_limit = data.get("requests_per_minute")

        if not new_limit or not isinstance(new_limit, int):
            return {"error": "Invalid rate limit value"}, 400

        # Mock update logic
        return {"message": "Rate limit updated", "new_limit": new_limit}, 200




api.add_resource(AdminAPI, "/admin")
api.add_resource(ManageGamesAPI, "/games")
api.add_resource(PlayerStatsAPI, "/player-stats")
api.add_resource(RateLimitAPI, "/rate-limits")
