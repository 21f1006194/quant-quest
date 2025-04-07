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


class APIToken(Resource):
    @jwt_required()
    def get(self):
        """Get API token status"""
        user_id = int(get_jwt_identity())  # Convert string ID back to integer
        user = User.query.get(user_id)

        if not user:
            return {"error": "User not found"}, 404

        return {
            "has_api_token": bool(user.api_token),
            "created_at": (
                user.api_token_created_at.isoformat()
                if user.api_token_created_at
                else None
            ),
        }, 200

    @jwt_required()
    def post(self):
        """Generate new API token"""
        user_id = int(get_jwt_identity())  # Convert string ID back to integer
        user = User.query.get(user_id)

        if not user:
            return {"error": "User not found"}, 404

        api_token = user.generate_api_token()
        db.session.commit()

        return {
            "api_token": api_token,
            "message": "API token generated successfully",
        }, 200

    @jwt_required()
    def delete(self):
        """Revoke API token"""
        user_id = int(get_jwt_identity())  # Convert string ID back to integer
        user = User.query.get(user_id)

        if not user:
            return {"error": "User not found"}, 404

        user.revoke_api_token()
        db.session.commit()

        return {"message": "API token revoked successfully"}, 200


api.add_resource(APIToken, "/api-token")
api.add_resource(Profile, "/profile")
