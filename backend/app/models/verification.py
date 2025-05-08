from datetime import datetime, timezone
from app import db


class VerificationToken(db.Model):
    __tablename__ = "verification_tokens"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    token = db.Column(db.String(128), unique=True, nullable=False)
    purpose = db.Column(db.String(50), nullable=False)  # e.g., "email_verification", "password_reset"
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_used = db.Column(db.Boolean, default=False)
