from flask_restful import Resource
from flask import Blueprint
from flask_restful import Api
from app.utils.auth import admin_required

admin_bp = Blueprint("admin", __name__)
api = Api(admin_bp)


class AdminAPI(Resource):
    @admin_required
    def get(self):
        """Get admin dashboard data"""
        return {"message": "Admin dashboard data"}, 200


api.add_resource(AdminAPI, "/admin")
