from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask import Blueprint
from flask_restful import Api
from app.models import User
from app import db

player_bp = Blueprint("player", __name__)
api = Api(player_bp)


class Profile(Resource):
    @jwt_required()
    def get(self):
        """Get player profile"""
        user_id = int(get_jwt_identity())  # Convert string ID back to integer
        user = User.query.get(user_id)

        if not user:
            return {"error": "User not found"}, 404

        return user.to_dict(), 200


api.add_resource(Profile, "/profile")
