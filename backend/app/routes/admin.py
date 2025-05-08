from flask_restful import Resource
from flask import Blueprint, request
from flask_restful import Api
from app.utils.auth import admin_required
from app.models.gameplay import Game
from app.services.wallet_service import WalletService
from app.models.wallet import TransactionCategory


admin_bp = Blueprint("admin", __name__)
api = Api(admin_bp)
game_bp = Blueprint("game_bp", __name__)


class AdminAPI(Resource):
    @admin_required
    def get(self):
        """Get admin dashboard data"""
        return {"message": "Admin dashboard data"}, 200


"""List of all games"""


class GameListAPI(Resource):
    @admin_required
    def get(self):
        try:
            games = Game.query.all()
            return {"games": [g.to_dict() for g in games]}, 200
        except Exception as e:
            return {"error": str(e)}, 500


class UserBonusAPI(Resource):
    @admin_required
    def post(self, user_id):
        """Give bonus to a user"""
        try:
            data = request.get_json()
            if not data or "amount" not in data:
                return {"error": "Amount is required"}, 400

            amount = float(data["amount"])
            if amount <= 0:
                return {"error": "Amount must be positive"}, 400

            description = data.get("description")
            if not description:
                return {"error": "Description is required"}, 400

            transaction = WalletService.create_transaction(
                user_id=user_id,
                amount=amount,
                category=TransactionCategory.BONUS,
                description=description,
                transaction_info=data.get("transaction_info"),
            )

            return {
                "message": "Bonus added successfully",
                "transaction": transaction.to_dict(),
            }, 200
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": str(e)}, 500


class UserPenaltyAPI(Resource):
    @admin_required
    def post(self, user_id):
        """Give penalty to a user"""
        try:
            data = request.get_json()
            if not data or "amount" not in data:
                return {"error": "Amount is required"}, 400

            amount = float(data["amount"])
            if amount <= 0:
                return {"error": "Amount must be positive"}, 400

            description = data.get("description")
            if not description:
                return {"error": "Description is required"}, 400

            transaction = WalletService.create_transaction(
                user_id=user_id,
                amount=amount,
                category=TransactionCategory.PENALTY,
                description=description,
                transaction_info=data.get("transaction_info"),
            )

            return {
                "message": "Penalty added successfully",
                "transaction": transaction.to_dict(),
            }, 200
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": str(e)}, 500


class AllUsersBonusAPI(Resource):
    @admin_required
    def post(self):
        """Give bonus to all users"""
        try:
            data = request.get_json()
            if not data or "amount" not in data:
                return {"error": "Amount is required"}, 400

            amount = float(data["amount"])
            if amount <= 0:
                return {"error": "Amount must be positive"}, 400

            description = data.get("description")
            if not description:
                return {"error": "Description is required"}, 400

            result = WalletService.create_bonus_for_all_users(
                amount=amount,
                description=description,
                transaction_info=data.get("transaction_info"),
            )

            return {
                "message": "Bonus distribution completed",
                "total_successful": result["total_successful"],
                "total_failed": result["total_failed"],
                "failed_users": result["failed_users"],
            }, 200
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": str(e)}, 500


api.add_resource(AdminAPI, "/admin")
api.add_resource(GameListAPI, "/admin/games")
api.add_resource(UserBonusAPI, "/admin/bonus/<int:user_id>")
api.add_resource(UserPenaltyAPI, "/admin/penalty/<int:user_id>")
api.add_resource(AllUsersBonusAPI, "/admin/bonus/to_all")
