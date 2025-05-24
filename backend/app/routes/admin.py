from flask_restful import Resource
from flask import Blueprint, request
from flask_restful import Api
from app.utils.auth import admin_required
from app.models.gameplay import Game
from app.services.wallet_service import WalletService
from app.models.wallet import TransactionCategory
from app.services.user_service import UserService
from app.utils.helpers import process_whitelist_csv


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

            transaction = WalletService.create_bonus(
                user_id=user_id,
                amount=amount,
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

            transaction = WalletService.create_penalty(
                user_id=user_id,
                amount=amount,
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


class AllUsersAPI(Resource):
    @admin_required
    def get(self):
        """Get list of all users with their wallet information"""
        try:
            # Get all users with their wallets preloaded in a single query
            users = UserService.get_all_users()

            users_data = []
            for user in users:
                # Since we used joinedload, accessing wallet won't trigger additional queries
                if user.is_admin:
                    continue
                wallet = user.wallet
                user_dict = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "full_name": user.full_name,
                    "wallet_balance": wallet.current_balance if wallet else None,
                    "wallet_last_updated": (
                        wallet.last_updated.isoformat()
                        if wallet and wallet.last_updated
                        else None
                    ),
                }
                users_data.append(user_dict)

            return {"users": users_data}, 200
        except Exception as e:
            return {"error": str(e)}, 500


class WhitelistUserAPI(Resource):
    @admin_required
    def post(self):
        """Whitelist a user"""
        try:
            data = request.get_json()
            if not data or "email" not in data:
                return {"error": "Email is required"}, 400

            email = data["email"]
            name = data.get("name")
            level = data.get("level")
            physical_presence = data.get("physical_presence", False)

            whitelisted_user = UserService.whitelist_user(
                email, name, level, physical_presence
            )
            return {
                "message": "User whitelisted successfully",
                "user": whitelisted_user.to_dict(),
            }, 201
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": str(e)}, 500

    def get(self):
        """Get all whitelisted users"""
        try:
            whitelisted_users = UserService.get_whitelisted_users()
            return {"whitelisted_users": [u.to_dict() for u in whitelisted_users]}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def delete(self, w_id):
        """Delete a whitelisted user by email"""
        try:
            print(f"Deleting user with id: {w_id}")
            UserService.delete_whitelisted_user(w_id)
            return {"message": "User deleted successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500


class BulkWhitelistAPI(Resource):
    @admin_required
    def post(self):
        """Bulk whitelist users from CSV file"""
        try:
            if "file" not in request.files:
                return {"error": "No file provided"}, 400

            file = request.files["file"]
            if not file.filename.endswith(".csv"):
                return {"error": "File must be a CSV"}, 400

            # Read and process the CSV file
            csv_content = file.read().decode("utf-8")
            users = process_whitelist_csv(csv_content)

            # Bulk whitelist the users
            result = UserService.bulk_whitelist_users(users)

            return {
                "message": result["message"],
                "added": result.get("added", 0),
                "skipped": result.get("skipped", 0),
                "total_processed": len(users),
            }, 201

        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": str(e)}, 500


api.add_resource(AdminAPI, "/admin")
api.add_resource(GameListAPI, "/admin/games")
api.add_resource(UserBonusAPI, "/admin/bonus/<int:user_id>")
api.add_resource(UserPenaltyAPI, "/admin/penalty/<int:user_id>")
api.add_resource(AllUsersBonusAPI, "/admin/bonus/to_all")
api.add_resource(AllUsersAPI, "/admin/all_users")
api.add_resource(WhitelistUserAPI, "/admin/whitelist")
api.add_resource(
    WhitelistUserAPI, "/admin/whitelist/<int:w_id>", endpoint="whitelist_user"
)
api.add_resource(BulkWhitelistAPI, "/admin/whitelist/bulk")
