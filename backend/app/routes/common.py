from flask import Blueprint, jsonify
from flask import Blueprint, request

from app.models.user import User, db
from flask_restful import Resource
from flask_restful import Api
from app.utils import is_password_strong

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

        # Check if email already exists
        if User.query.filter_by(email=data["email"]).first():
            return {"error": "Email already registered"}, 400

        # Check if username already exists
        if User.query.filter_by(username=data["username"]).first():
            return {"error": "Username already taken"}, 400

        # Create new user
        user = User(
            email=data["email"],
            username=data["username"],
            full_name=data["full_name"],
            is_admin=False,
        )
        user.set_password(data["password"])

        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            import traceback

            traceback.print_exc()
            return {"error": "Error creating user"}, 500

        # return user details
        return {
            "message": "User registered successfully",
            "user": user.to_dict(),
        }, 201


api.add_resource(RegisterAPI, "/register")
api.add_resource(HealthAPI, "/health")
