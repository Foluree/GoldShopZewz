"""add dialog chain and timestamps

Revision ID: c9f3a1b27d6e
Revises: b7c1d92e4a63
Create Date: 2026-10-06 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c9f3a1b27d6e'
down_revision: Union[str, None] = 'b7c1d92e4a63'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'Undertable_appeal',
        sa.Column('parent_id', sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        'fk_undertable_appeal_parent',
        'Undertable_appeal',
        'Undertable_appeal',
        ['parent_id'],
        ['id'],
    )
    op.add_column(
        'Undertable_appeal',
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
    )
    op.add_column(
        'AppealAnswers',
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
    )


def downgrade() -> None:
    op.drop_column('AppealAnswers', 'created_at')
    op.drop_column('Undertable_appeal', 'created_at')
    op.drop_constraint('fk_undertable_appeal_parent', 'Undertable_appeal', type_='foreignkey')
    op.drop_column('Undertable_appeal', 'parent_id')
