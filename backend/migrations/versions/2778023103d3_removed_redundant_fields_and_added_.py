"""Removed redundant fields and added netflow property in gameplay

Revision ID: 2778023103d3
Revises: 30229cae655c
Create Date: 2025-04-23 17:59:22.911217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2778023103d3'
down_revision = '30229cae655c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bets', schema=None) as batch_op:
        batch_op.alter_column('payout',
               existing_type=sa.FLOAT(),
               nullable=False)
        batch_op.alter_column('choice',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.drop_column('is_successful')
        batch_op.drop_column('outcome')

    with op.batch_alter_table('game_sessions', schema=None) as batch_op:
        batch_op.drop_column('ended_at')
        batch_op.drop_column('duration')
        batch_op.drop_column('result')
        batch_op.drop_column('started_at')
        batch_op.drop_column('status')
        batch_op.drop_column('score')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game_sessions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('score', sa.FLOAT(), nullable=True))
        batch_op.add_column(sa.Column('status', sa.VARCHAR(length=20), nullable=True))
        batch_op.add_column(sa.Column('started_at', sa.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('result', sa.VARCHAR(length=20), nullable=True))
        batch_op.add_column(sa.Column('duration', sa.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('ended_at', sa.DATETIME(), nullable=True))

    with op.batch_alter_table('bets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('outcome', sa.VARCHAR(length=20), nullable=True))
        batch_op.add_column(sa.Column('is_successful', sa.BOOLEAN(), nullable=True))
        batch_op.alter_column('choice',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('payout',
               existing_type=sa.FLOAT(),
               nullable=True)

    # ### end Alembic commands ###
