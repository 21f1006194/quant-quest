from functools import wraps
from flask import request
from app.models import User
from flask_jwt_extended import verify_jwt_in_request, get_jwt, jwt_required


def api_token_required(f):
    pass


def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {"error": "Admin privileges required"}, 403
        return f(*args, **kwargs)

    return decorated
