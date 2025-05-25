from functools import wraps
from flask import request
from flask_jwt_extended import get_jwt, jwt_required
from app.services.user_service import UserService


def validate_api_token(api_token):
    """Validate the API token and return the user if valid"""
    if not api_token:
        return None
    try:
        user_id, token = api_token.split(".")
        # Use the cached get_user_by_id method
        user = UserService.get_user_by_id(int(user_id))
        if not user or not user._api_token or user._api_token != token:
            return None
        return user
    except (ValueError, AttributeError):
        return None


def api_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_token = request.headers.get("X-API-Token")

        if not api_token:
            return {"error": "API token is required"}, 401

        # Validate token and get user
        user = validate_api_token(api_token)
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
