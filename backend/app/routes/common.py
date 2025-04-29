from flask import Blueprint, jsonify
from flask import Blueprint, request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from flask_restful import Resource, Api
from app.utils import is_password_strong
from datetime import timedelta
from app.services.user_service import UserService

common_bp = Blueprint("common", __name__)
api = Api(common_bp)


class HealthAPI(Resource):
    def get(self):
        return {"status": "healthy"}, 200


class RegisterAPI(Resource):
    def post(self):
        data = request.get_json()

        # Validate required fields
        required_fields = ["email", "username", "password", "full_name"]
        for field in required_fields:
            if not data.get(field):
                return {"error": f"{field} is required"}, 400

        # Check if password is strong
        if not is_password_strong(data["password"]):
            return {"error": "Password is not strong enough"}, 400

        try:
            # Create user using service
            user = UserService.create_user(
                email=data["email"],
                username=data["username"],
                password=data["password"],
                full_name=data["full_name"],
            )

            return {
                "message": "User registered successfully",
                "user": user.to_dict(),
            }, 201

        except ValueError as e:
            import traceback

            traceback.print_exc()
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": "Error creating user"}, 500


class LoginAPI(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"error": "Username and password are required"}, 400

        user = UserService.get_user_by_username(username)
        if not user or not user.check_password(password):
            return {"error": "Invalid username or password"}, 401

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin},
            expires_delta=timedelta(days=1),
        )

        return {
            "access_token": access_token,
            "api_token": user.api_token,
            "user": user.to_dict(),
        }, 200


class LogoutAPI(Resource):
    @jwt_required()
    def post(self):
        # In JWT, we don't actually need to do anything server-side
        # The client should remove the token from their storage
        return {"message": "Successfully logged out"}, 200


api.add_resource(RegisterAPI, "/register")
api.add_resource(LoginAPI, "/login")
api.add_resource(HealthAPI, "/health")
api.add_resource(LogoutAPI, "/logout")
