from datetime import datetime, timezone
from app import db


class AuditLog(db.Model):
    """
    Generic log for user-related activities.
    Captures login/logout, password changes, failed attempts, etc.
    """
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)  # Null = anonymous
    action = db.Column(db.String(100), nullable=False)  # e.g., "login_success", "password_change"
    metadata = db.Column(db.JSON, nullable=True)        # structured data: {"ip": "...", "user_agent": "..."}
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship("User", backref="audit_logs")

    __table_args__ = (
        db.Index("idx_audit_user", "user_id"),
        db.Index("idx_audit_action", "action"),
    )


class AdminActivityLog(db.Model):
    """
    Logs actions taken by admin users, with optional target user reference.
    """
    __tablename__ = "admin_activity_logs"

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    action = db.Column(db.String(100), nullable=False)  # e.g., "banned_user", "added_bonus", "adjusted_wallet"
    target_user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    metadata = db.Column(db.JSON, nullable=True)  # e.g., {"wallet_delta": 100, "reason": "manual adjustment"}
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    admin = db.relationship("User", foreign_keys=[admin_id], backref="admin_logs")
    target_user = db.relationship("User", foreign_keys=[target_user_id], backref="target_logs")

    __table_args__ = (
        db.Index("idx_admin_action", "action"),
        db.Index("idx_admin_target", "target_user_id"),
    )
