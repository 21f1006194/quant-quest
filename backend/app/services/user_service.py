from app import db
from app.models import User, Wallet, UserProfile
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from app.services.game_service import GameService


class UserService:
    @staticmethod
    def create_user(email, username, password, full_name):
        """
        Create a new user with associated wallet, API token, and profile.
        This is an atomic operation - either everything succeeds or nothing does.
        """
        try:
            # Check if email or username already exists
            if User.query.filter_by(email=email).first():
                raise ValueError(f"User with this email already exists.")
            if User.query.filter_by(username=username).first():
                raise ValueError(f"User with this username already exists.")

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
            db.session.flush()  # to get user.id for wallet and profile creation

            # Create wallet
            initial_capital = 10000.0
            wallet = Wallet(
                user_id=user.id,
                initial_capital=initial_capital,
                current_balance=initial_capital,
            )
            db.session.add(wallet)

            # Create user profile (if you have a UserProfile model)
            profile = UserProfile(user_id=user.id)
            db.session.add(profile)

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
