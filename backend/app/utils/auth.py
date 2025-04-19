from functools import wraps
from flask import request
from app.models import User
from flask_jwt_extended import verify_jwt_in_request, get_jwt, jwt_required


def api_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_token = request.headers.get("X-API-Token")

        if not api_token:
            return {"error": "API token is required"}, 401

        # Validate token and get user
        user = User.validate_api_token(api_token)
        if not user:
            return {"error": "Invalid API token"}, 401

        # Store user in request context
        request.user = user
        return f(*args, **kwargs)

    return decorated


def get_api_user():
    """Get the user from the request context when using API token authentication"""
    user = getattr(request, "user", None)
    return user if user else None


def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {"error": "Admin privileges required"}, 403
        return f(*args, **kwargs)

    return decorated
