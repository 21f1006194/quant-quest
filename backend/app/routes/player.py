from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask import Blueprint
from flask_restful import Api
from app.models import User, Bet, GameSession, Game, Wallet
from app import db
from sqlalchemy.orm import joinedload
from datetime import datetime
from app.services.game_service import GameService

player_bp = Blueprint("player", __name__)
api = Api(player_bp)


class PlayerProfile(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        user = User.query.options(joinedload(User.profile)).get(user_id)

        if not user:
            return {"error": "User not found"}, 404

        return {"profile": user.to_dict()}, 200


class WalletInfo(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        user = User.query.options(joinedload(User.wallet)).get(user_id)

        if not user:
            return {"error": "User not found"}, 404

        wallet = user.wallet
        wallet_data = {
            "balance": wallet.current_balance if wallet else 0.0,
            "last_updated": (
                wallet.last_updated.isoformat()
                if wallet and wallet.last_updated
                else None
            ),
        }
        return {"wallet": wallet_data}, 200


class RecentBets(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        try:
            recent_bets = (
                Bet.query.filter_by(user_id=user_id)
                .order_by(Bet.placed_at.desc())
                .limit(20)
                .all()
            )
        except Exception as e:
            return {"error": f"Error fetching bets: {str(e)}"}, 500

        return {"recent_bets": [bet.to_dict() for bet in recent_bets]}, 200


class APIToken(Resource):
    @jwt_required()
    def get(self):
        """Get API token status"""
        user_id = int(get_jwt_identity())  # Convert string ID back to integer
        user = User.query.get(user_id)

        if not user:
            return {"error": "User not found"}, 404

        return {
            "has_api_token": bool(user.api_token),
            "created_at": (
                user.api_token_created_at.isoformat()
                if user.api_token_created_at
                else None
            ),
        }, 200

    @jwt_required()
    def post(self):
        """Generate new API token"""
        user_id = int(get_jwt_identity())  # Convert string ID back to integer
        user = User.query.get(user_id)

        if not user:
            return {"error": "User not found"}, 404

        api_token = user.generate_api_token()
        db.session.commit()

        return {
            "api_token": api_token,
            "message": "API token generated successfully",
        }, 200

    @jwt_required()
    def delete(self):
        """Revoke API token"""
        user_id = int(get_jwt_identity())  # Convert string ID back to integer
        user = User.query.get(user_id)

        if not user:
            return {"error": "User not found"}, 404

        user.revoke_api_token()
        db.session.commit()

        return {"message": "API token revoked successfully"}, 200


class PlayerGames(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        print(user_id)
        games = GameService.get_active_games()
        played_game_counts, played_game_pnl = GameService.get_games_played_data_by_user(
            user_id
        )
        resp = []
        for game in games:
            resp.append(game.to_dict())
            resp[-1]["plays_remaining"] = (
                game.max_sessions_per_user - played_game_counts.get(game.id, 0)
            )
            resp[-1]["pnl"] = played_game_pnl.get(game.id, 0)
        return {"games": resp}, 200


api.add_resource(APIToken, "/api-token")
api.add_resource(PlayerProfile, "/profile")
api.add_resource(WalletInfo, "/wallet")
api.add_resource(RecentBets, "/recent-bets")
api.add_resource(PlayerGames, "/games")
