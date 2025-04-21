from flask_restful import Resource
from flask import Blueprint
from flask_restful import Api
from app.utils.auth import admin_required

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

api.add_resource(AdminAPI, "/admin")
api.add_resource(AdminDashboardAPI, "/admin/dashboard")
