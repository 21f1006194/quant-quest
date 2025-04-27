from flask_restful import Resource
from flask import Blueprint
from flask_restful import Api
from app.utils.auth import admin_required
from app.models.gameplay import Game


admin_bp = Blueprint("admin", __name__)
api = Api(admin_bp)
game_bp = Blueprint('game_bp', __name__)


class AdminAPI(Resource):
    @admin_required
    def get(self):
        """Get admin dashboard data"""
        return {"message": "Admin dashboard data"}, 200

"""List of all games"""
class GameListAPI(Resource):
    @admin_required
    def get(self):
        try:
            games = Game.query.all()
            return {"games": [g.to_dict() for g in games]}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        
"""Total number of games"""
class GameCountResource(Resource):
    @admin_required
    def get(self):
        try:
            game_count = Game.query.count()
            return {"game_count": game_count}, 200
        except Exception as e:
            return {"error": str(e)}, 500

api.add_resource(AdminAPI, "/admin")
api.add_resource(GameListAPI, "/admin/games")
api.add_resource(GameCountResource, "/admin/games/count")
# Register the admin blueprint
