"""add appeal moderation

Revision ID: b7c1d92e4a63
Revises: d3b7e9c51a40
Create Date: 2026-09-30 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b7c1d92e4a63'
down_revision: Union[str, None] = 'd3b7e9c51a40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'Undertable_appeal',
        sa.Column('canceled', sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.create_table(
        'AppealAnswers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('appeal_id', sa.Integer(), nullable=False),
        sa.Column('reaction', sa.Boolean(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('email_user', sa.String(), nullable=False),
        sa.Column('answer', sa.String(), nullable=False, server_default=''),
        sa.ForeignKeyConstraint(['appeal_id'], ['Undertable_appeal.id'], name='fk_appeal_answers_appeal'),
        sa.ForeignKeyConstraint(['user_id'], ['UserProfiles.id'], name='fk_appeal_answers_user'),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('AppealAnswers')
    op.drop_column('Undertable_appeal', 'canceled')
