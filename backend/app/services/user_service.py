from app import db
from app.models import User, Wallet, WhitelistedUser
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from app.services.game_service import GameService
from app.services.wallet_service import WalletService
from app.models.wallet import TransactionCategory
from sqlalchemy.orm import joinedload
from app.utils.image_upload import upload_profile_picture_from_url


class UserService:
    @staticmethod
    def create_user(
        email,
        username,
        password,
        full_name,
        avatar_url=None,
        bio=None,
        is_google_user=False,
    ):
        """
        Create a new user with associated walle
        This is an atomic operation - either everything succeeds or nothing does.

        Args:
            email (str): User's email address
            username (str): User's username
            password (str): User's password (can be None for Google users)
            full_name (str): User's full name
            avatar_url (str): User's avatar URL
            bio (str): User's bio
            is_google_user (bool): Whether this is a Google-authenticated user
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
                avatar_url=avatar_url,
                bio=bio,
                is_admin=False,
                is_google_user=is_google_user,  # Store whether this is a Google user
            )

            # Only set password if not a Google user
            if not is_google_user:
                if not password:
                    raise ValueError("Password is required for non-Google users")
                user.set_password(password)
            else:
                # For Google users, we don't need a password
                user.password_hash = None

            user.generate_api_token()
            db.session.add(user)
            db.session.flush()  # to get user.id for wallet creation

            if avatar_url:
                new_avatar, error = upload_profile_picture_from_url(avatar_url, user.id)
                if not error:
                    user.avatar_url = new_avatar
                else:
                    print(f"Error uploading profile picture: {avatar_url}")

            # Create wallet
            initial_capital = 10000.0
            wallet = Wallet(
                user_id=user.id,
                initial_capital=initial_capital,
                current_balance=initial_capital,
            )
            db.session.add(wallet)

            # Commit transaction
            db.session.commit()

            # Add joining bonus
            try:
                WalletService.create_transaction(
                    user_id=user.id,
                    amount=2000.0,
                    category=TransactionCategory.BONUS,
                    description="Welcome bonus!",
                )
            except Exception as e:
                # Log the error but don't fail the user creation
                print(f"Failed to add joining bonus for user {user.id}: {str(e)}")

            GameService.initialize_game_pnl_for_user(user.id)

            return user

        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(
                f"User with this email or username already exists: {str(e)}"
            ) from e
        except Exception as e:
            import traceback

            traceback.print_exc()
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

    @staticmethod
    def whitelist_user(email, name, level, physical_presence):
        """Whitelist a user for the game"""
        if WhitelistedUser.query.filter_by(email=email).first():
            raise ValueError(f"User with this email already exists.")
        try:
            whitelisted_user = WhitelistedUser(
                email=email,
                name=name,
                level=level,
                physical_presence=physical_presence,
            )
            db.session.add(whitelisted_user)
            db.session.commit()
            return whitelisted_user
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"User with this email already exists: {str(e)}") from e
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_whitelisted_users():
        """Get all whitelisted users"""
        return WhitelistedUser.query.all()

    @staticmethod
    def get_whitelisted_user_by_email(email):
        """Get a whitelisted user by email"""
        return WhitelistedUser.query.filter_by(email=email).first()

    @staticmethod
    def delete_whitelisted_user(w_id):
        """Delete a whitelisted user by id"""
        whitelisted_user = WhitelistedUser.query.get(w_id)
        if whitelisted_user:
            db.session.delete(whitelisted_user)
            db.session.commit()
            return True
        return False

    @staticmethod
    def bulk_whitelist_users(users):
        """Bulk whitelist users as a single transaction"""
        try:
            db.session.bulk_insert_mappings(WhitelistedUser, users)
            db.session.commit()
            return True
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"User with this email already exists: {str(e)}") from e
        except Exception as e:
            db.session.rollback()
            raise e
