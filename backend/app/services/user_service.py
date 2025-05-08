from app import db
from app.models import User, Wallet
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from app.services.game_service import GameService
from sqlalchemy.orm import joinedload


class UserService:
    @staticmethod
    def create_user(email, username, password, full_name):
        """
        Create a new user with associated wallet and API token.
        This is an atomic operation - either everything succeeds or nothing does.
        """
        try:
            # Create user
            user = User(
                email=email,
                username=username,
                full_name=full_name,
                is_admin=False,
            )
            user.set_password(password)
            user.generate_api_token()
            db.session.add(user)
            db.session.flush()

            cap = 10000.0
            # Create wallet
            wallet = Wallet(user_id=user.id, initial_capital=cap, current_balance=cap)

            # Add both to session
            db.session.add(wallet)
            # Commit transaction
            db.session.commit()
            GameService.initialize_game_pnl_for_user(user.id)

            return user

        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(
                f"User with this email or username already exists: {str(e)}"
            ) from e
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Error creating user: {str(e)}") from e

    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID with their wallet"""
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_username(username):
        """Get user by username with their wallet"""
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_user_by_email(email):
        """Get user by email with their wallet"""
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_all_users():
        """Get all users with their wallets preloaded in a single query"""
        return User.query.options(joinedload(User.wallet)).all()
