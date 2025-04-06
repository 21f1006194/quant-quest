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

        user = User.query.filter_by(api_token=api_token).first()
        if not user:
            return {"error": "Invalid API token"}, 401

        # Add user to request context for use in the route
        request.user = user
        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {"error": "Admin privileges required"}, 403
        return f(*args, **kwargs)

    return decorated
