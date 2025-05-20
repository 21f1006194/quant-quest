from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import secrets
import re

EMAIL_PATTERN = r"^\d{2}f\d{7}@ds\.study\.iitm\.ac\.in$"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(
        db.String(256), nullable=True
    )  # Made nullable for Google users
    full_name = db.Column(db.String(100), nullable=False)
    avatar_url = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_google_user = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    _api_token = db.Column("api_token", db.String(64), unique=True)
    api_token_created_at = db.Column(db.DateTime)

    # Relationships

    verification_tokens = db.relationship(
        "VerificationToken", backref="user", cascade="all, delete-orphan"
    )
    game_sessions = db.relationship(
        "GameSession", backref="user", cascade="all, delete-orphan"
    )
    wallet = db.relationship(
        "Wallet", backref="user", uselist=False, cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_api_token(self):
        """Generate a new API token for the user"""
        self._api_token = secrets.token_urlsafe(32)
        self.api_token_created_at = datetime.now(timezone.utc)
        return self.api_token

    @property
    def api_token(self):
        """Get the full API token with user ID"""
        if not self._api_token:
            return None
        return f"{self.id}.{self._api_token}"

    def revoke_api_token(self):
        """Revoke the user's API token"""
        self._api_token = None
        self.api_token_created_at = None

    @staticmethod
    def validate_api_token(api_token):
        """Validate the API token and return the user if valid"""
        if not api_token:
            return None
        try:
            user_id, token = api_token.split(".")
            user = User.query.get(user_id)
            if not user or not user._api_token or user._api_token != token:
                return None
            return user
        except (ValueError, AttributeError):
            return None

    @staticmethod
    def is_valid_iitm_email(email):
        return re.fullmatch(EMAIL_PATTERN, email) is not None

    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "avatar_url": self.avatar_url,
            "bio": self.bio,
            "is_admin": self.is_admin,
            "is_google_user": self.is_google_user,  # Added to response
            "created_at": self.created_at.isoformat(),
            "has_api_token": bool(self._api_token),
        }


class WhitelistedUser(db.Model):
    __tablename__ = "whitelisted_users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    level = db.Column(db.String(100), nullable=True)
    physical_presence = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "level": self.level,
            "physical_presence": self.physical_presence,
        }
