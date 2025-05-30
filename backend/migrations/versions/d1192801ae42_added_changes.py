"""added changes

Revision ID: d1192801ae42
Revises: 4381e2fa483a
Create Date: 2025-04-07 19:28:42.087087

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import Text

# revision identifiers, used by Alembic.
revision = "d1192801ae42"
down_revision = "4381e2fa483a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "games",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("type", sa.String(length=50), nullable=True),
        sa.Column("config_data", postgresql.JSON(astext_type=Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "game_sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("game_id", sa.Integer(), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("ended_at", sa.DateTime(), nullable=True),
        sa.Column("duration", sa.Interval(), nullable=True),
        sa.Column("result", sa.String(length=20), nullable=True),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=True),
        sa.Column("session_data", postgresql.JSON(astext_type=Text()), nullable=True),
        sa.ForeignKeyConstraint(["game_id"], ["games.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("game_sessions", schema=None) as batch_op:
        batch_op.create_index(
            "idx_session_user_game", ["user_id", "game_id"], unique=False
        )

    op.create_table(
        "user_profiles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("avatar_url", sa.String(length=255), nullable=True),
        sa.Column("location", sa.String(length=100), nullable=True),
        sa.Column("dob", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_table(
        "verification_tokens",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token", sa.String(length=128), nullable=False),
        sa.Column("purpose", sa.String(length=50), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("is_used", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token"),
    )
    op.create_table(
        "wallets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("balance", sa.Float(), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=True),
        sa.Column("last_updated", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    with op.batch_alter_table("wallets", schema=None) as batch_op:
        batch_op.create_index("idx_wallet_user", ["user_id"], unique=False)

    op.create_table(
        "bets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("placed_at", sa.DateTime(), nullable=True),
        sa.Column("outcome", sa.String(length=20), nullable=True),
        sa.Column("payout", sa.Float(), nullable=True),
        sa.Column("choice", sa.String(length=100), nullable=True),
        sa.Column("is_successful", sa.Boolean(), nullable=True),
        sa.Column("bet_details", postgresql.JSON(astext_type=Text()), nullable=True),
        sa.ForeignKeyConstraint(
            ["session_id"], ["game_sessions.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("bets", schema=None) as batch_op:
        batch_op.create_index("idx_bet_session", ["session_id"], unique=False)

    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("wallet_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column(
            "type", sa.Enum("CREDIT", "DEBIT", name="transactiontype"), nullable=False
        ),
        sa.Column(
            "category",
            sa.Enum(
                "BET", "WIN", "BONUS", "ADMIN_ADJUSTMENT", name="transactioncategory"
            ),
            nullable=True,
        ),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("transaction_info", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["wallet_id"], ["wallets.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("transactions", schema=None) as batch_op:
        batch_op.create_index("idx_transaction_category", ["category"], unique=False)
        batch_op.create_index(
            "idx_transaction_created_at", ["created_at"], unique=False
        )
        batch_op.create_index("idx_transaction_wallet", ["wallet_id"], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("transactions", schema=None) as batch_op:
        batch_op.drop_index("idx_transaction_wallet")
        batch_op.drop_index("idx_transaction_created_at")
        batch_op.drop_index("idx_transaction_category")

    op.drop_table("transactions")
    with op.batch_alter_table("bets", schema=None) as batch_op:
        batch_op.drop_index("idx_bet_session")

    op.drop_table("bets")
    with op.batch_alter_table("wallets", schema=None) as batch_op:
        batch_op.drop_index("idx_wallet_user")

    op.drop_table("wallets")
    op.drop_table("verification_tokens")
    op.drop_table("user_profiles")
    with op.batch_alter_table("game_sessions", schema=None) as batch_op:
        batch_op.drop_index("idx_session_user_game")

    op.drop_table("game_sessions")
    op.drop_table("games")
    # ### end Alembic commands ###
