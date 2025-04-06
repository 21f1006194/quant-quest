from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import JSON
from app import db


class Wallet(db.Model):
    __tablename__ = "wallets"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    balance = db.Column(db.Float, default=0.0, nullable=False)
    currency = db.Column(db.String(10), default="INR")

    last_updated = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    transactions = db.relationship("Transaction", backref="wallet", cascade="all, delete", passive_deletes=True)

    __table_args__ = (
        db.Index("idx_wallet_user", "user_id"),
    )


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey("wallets.id", ondelete="CASCADE"), nullable=False)

    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'credit' or 'debit'
    category = db.Column(db.String(50))              # 'bet', 'win', 'bonus', 'admin_adjustment', etc.
    description = db.Column(db.String(255))
    metadata = db.Column(JSON, nullable=True)        # Additional data like ref_id, admin_id, etc.

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.Index("idx_transaction_wallet", "wallet_id"),
        db.Index("idx_transaction_category", "category"),
    )
