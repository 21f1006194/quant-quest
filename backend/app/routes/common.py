from flask import Blueprint, jsonify, request, current_app, redirect, url_for
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    verify_jwt_in_request,
    get_jwt,
    decode_token,
)
from flask_restful import Resource, Api
from app.utils import is_password_strong
from datetime import timedelta
from app.services.user_service import UserService
from app.services.sse_service import SSEService
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import json

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


@common_bp.route("/sse", methods=["GET"])
def sse_events():
    """SSE endpoint for real-time updates"""
    # Get token from URL parameters
    token = request.args.get("auth_token")
    if not token:
        current_app.logger.error("No token provided in SSE request")
        return {"error": "Missing token"}, 401

    try:
        # Decode and verify the token directly
        decoded_token = decode_token(token)
        user_id = decoded_token[
            "sub"
        ]  # 'sub' is the standard JWT claim for subject/user_id

        current_app.logger.info(f"SSE connection established for user {user_id}")

        sse_service = SSEService()
        return sse_service.subscribe_to_user_events(user_id)
    except Exception as e:
        current_app.logger.error(f"SSE Authentication Error: {str(e)}")
        return {"error": "Invalid token"}, 401


class GoogleAuthAPI(Resource):
    def post(self):
        data = request.get_json()
        token = data.get("token")

        if not token:
            return {"error": "No token provided"}, 400

        try:
            # Verify the token
            idinfo = id_token.verify_oauth2_token(
                token, google_requests.Request(), current_app.config["GOOGLE_CLIENT_ID"]
            )

            # Get user info
            email = idinfo["email"]
            name = idinfo.get("name", email.split("@")[0])
            name = " ".join(word.capitalize() for word in name.split(" ")).strip()
            avatar_url = idinfo.get("picture", None)
            bio = idinfo.get("bio", None)

            # Check if email is whitelisted
            whitelisted_user = UserService.get_whitelisted_user_by_email(email)
            if not whitelisted_user:
                return {
                    "error": "Unauthorized email, register for the event or contact the admin"
                }, 403

            # Get or create user
            user = UserService.get_user_by_email(email)
            if not user:
                # Create new user with Google info
                user = UserService.create_user(
                    email=email,
                    username=email.split("@")[0],  # Use email prefix as username
                    password=None,  # No password for Google users
                    full_name=name,
                    avatar_url=avatar_url,
                    bio=bio,
                    is_google_user=True,
                )
                if not user:
                    return {"error": "Error creating user"}, 500

            # Create JWT token
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

        except ValueError as e:
            return {"error": "Invalid token"}, 401
        except Exception as e:
            current_app.logger.error(f"Google auth error: {str(e)}")
            return {"error": "Authentication failed"}, 500


api.add_resource(RegisterAPI, "/register")
api.add_resource(LoginAPI, "/login")
api.add_resource(HealthAPI, "/health")
api.add_resource(LogoutAPI, "/logout")
api.add_resource(GoogleAuthAPI, "/auth/google")
