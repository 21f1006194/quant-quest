from flask_restful import Resource
from flask import Blueprint
from flask_restful import Api
from app.utils.auth import api_token_required

game_bp = Blueprint("game", __name__)
api = Api(game_bp)


class GameTest(Resource):
    @api_token_required
    def get(self):
        return {"message": "Game test successful"}, 200


api.add_resource(GameTest, "/game-test")
