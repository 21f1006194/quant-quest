from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import secrets
import re

EMAIL_PATTERN = r'^\d{2}f\d{7}@ds\.study\.iitm\.ac\.in$'


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)

    password_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)

    mfa_enabled = db.Column(db.Boolean, default=False)
    mfa_secret = db.Column(db.String(64), nullable=True)

    failed_login_attempts = db.Column(db.Integer, default=0)
    last_login = db.Column(db.DateTime)

    api_token = db.Column(db.String(64), unique=True)
    api_token_created_at = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    roles = db.relationship("UserRole", backref="user", cascade="all, delete-orphan")
    verification_tokens = db.relationship("VerificationToken", backref="user", cascade="all, delete-orphan")
    audit_logs = db.relationship("AuditLog", backref="user", cascade="all, delete-orphan")
    profile = db.relationship("UserProfile", backref=db.backref("user", uselist=False), cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_api_token(self):
        self.api_token = secrets.token_urlsafe(32)
        self.api_token_created_at = datetime.now(timezone.utc)
        return self.api_token

    def revoke_api_token(self):
        self.api_token = None
        self.api_token_created_at = None

    @staticmethod
    def is_valid_iitm_email(email):
        return re.fullmatch(EMAIL_PATTERN, email) is not None

    def to_dict(self):
        return {
            "id": self.id,
            "roll_number": self.roll_number,
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "email_verified": self.email_verified,
            "mfa_enabled": self.mfa_enabled,
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "roles": [ur.role.name for ur in self.roles],
        }


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # e.g., 'admin', 'participant'
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    users = db.relationship("UserRole", backref="role", cascade="all, delete")


class UserRole(db.Model):
    __tablename__ = "user_roles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    assigned_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
