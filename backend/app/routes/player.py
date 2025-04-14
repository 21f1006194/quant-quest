from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask import Blueprint
from flask_restful import Api
from app.models import User, Bet, GameSession, Game, Wallet
from app import db
from sqlalchemy.orm import joinedload
from datetime import datetime
import pytz

player_bp = Blueprint("player", __name__)
api = Api(player_bp)
IST = pytz.timezone("Asia/Kolkata") # IST in Profile but UTC in DB


class PlayerProfile(Resource): 
    @jwt_required()
    def get(self):
        """Player dashboard with profile, wallet info, and last 20 (n = 20, open to be modified) bets"""
        user_id = int(get_jwt_identity())
        
        # Fetching the user with joined profile and wallet data
        try:
            user = (
                User.query
                .options(joinedload(User.profile), joinedload(User.wallet))
                .get(user_id)
            )
        except Exception as e:
            return {"error": f"Error fetching user: {str(e)}"}, 500
        
        if not user:
            return {"error": "User not found"}, 404

        # Profile data
        profile = user.to_dict()

        # Wallet data with error handling
        if user.wallet:
            wallet = {
                "balance": user.wallet.balance,
                "currency": user.wallet.currency,
                "last_updated": user.wallet.last_updated.astimezone(IST).isoformat() if user.wallet.last_updated else None,
            }
        else:
            wallet = {"balance": 0.0, "currency": "INR", "last_updated": None}

        # Fetching the latest (Atmost) 20 bets of the user
        try:
            recent_bets = (
                db.session.query(Bet)
                .join(GameSession, Bet.session_id == GameSession.id)
                .join(Game, GameSession.game_id == Game.id)
                .filter(GameSession.user_id == user_id)
                .order_by(Bet.placed_at.desc())
                .limit(20)
                .all()
            )
        except Exception as e:
            return {"error": f"Error fetching bets: {str(e)}"}, 500

        # Bet data and convert timestamps to IST
        bets = []
        for bet in recent_bets:
            game = bet.session.game
            placed_at_ist = bet.placed_at.astimezone(IST).isoformat() if bet.placed_at else None
            bets.append({
                "game_id": game.id,
                "game_name": game.name,
                "amount": bet.amount,
                "choice": bet.choice,
                "outcome": bet.outcome,
                "payout": bet.payout,
                "is_successful": bet.is_successful,
                "placed_at": placed_at_ist,
                "bet_details": bet.bet_details,
            })

        return {
            "profile": profile,
            "wallet": wallet,
            "recent_bets": bets if recent_bets else []
        }, 200


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


api.add_resource(APIToken, "/api-token")
api.add_resource(PlayerProfile, "/profile")
