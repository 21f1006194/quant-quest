from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import JSON
from app import db
from enum import Enum
from sqlalchemy import Enum as SQLEnum


class Wallet(db.Model):
    __tablename__ = "wallets"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    initial_capital = db.Column(db.Float, default=0.0, nullable=False)
    current_balance = db.Column(db.Float, default=0.0, nullable=False)

    last_updated = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    transactions = db.relationship(
        "Transaction", backref="wallet", cascade="all, delete", passive_deletes=True
    )

    __table_args__ = (db.Index("idx_wallet_user", "user_id"),)


class TransactionType(Enum):
    CREDIT = "credit"
    DEBIT = "debit"

    def __str__(self):
        return self.value


class TransactionCategory(Enum):
    BONUS = "bonus"
    PENALTY = "penalty"
    EXPENSE = "expense"

    def __str__(self):
        return self.value


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(
        db.Integer, db.ForeignKey("wallets.id", ondelete="CASCADE"), nullable=False
    )

    amount = db.Column(db.Float, nullable=False)
    type = db.Column(SQLEnum(TransactionType), nullable=False)
    category = db.Column(SQLEnum(TransactionCategory), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    transaction_info = db.Column(
        db.JSON, nullable=True
    )  # Additional data like ref_id, admin_id, etc.

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    deleted_at = db.Column(db.DateTime, nullable=True)

    __table_args__ = (
        db.Index("idx_transaction_wallet", "wallet_id"),
        db.Index("idx_transaction_category", "category"),
        db.Index(
            "idx_transaction_created_at", "created_at"
        ),  # Index on created_at for time-based queries
    )

    def __init__(self, **kwargs):
        category = kwargs.get("category")
        if category == TransactionCategory.BONUS:
            kwargs["type"] = TransactionType.CREDIT
        elif category in [TransactionCategory.PENALTY, TransactionCategory.EXPENSE]:
            kwargs["type"] = TransactionType.DEBIT
        else:
            raise ValueError("Invalid transaction category")

        super().__init__(**kwargs)

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": str(self.category),
            "type": str(self.type),
            "description": self.description,
        }
