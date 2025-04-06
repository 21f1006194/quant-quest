from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import secrets
import re

EMAIL_PATTERN = r'^\d{2}f\d{7}@ds\.study\.iitm\.ac\.in$'

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    api_token = db.Column(db.String(64), unique=True)
    api_token_created_at = db.Column(db.DateTime)

    # Relationships
    verification_tokens = db.relationship("VerificationToken", backref="user", cascade="all, delete-orphan")
    game_sessions = db.relationship("GameSession", backref="user", cascade="all, delete-orphan")
    wallet = db.relationship("Wallet", backref="user", uselist=False, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_api_token(self):
        """Generate a new API token for the user"""
        self.api_token = secrets.token_urlsafe(32)
        self.api_token_created_at = datetime.now(timezone.utc)
        return self.api_token

    def revoke_api_token(self):
        """Revoke the user's API token"""
        self.api_token = None
        self.api_token_created_at = None

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
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "has_api_token": bool(self.api_token),
        }