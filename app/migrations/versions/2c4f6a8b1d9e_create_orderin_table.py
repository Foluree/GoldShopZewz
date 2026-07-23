"""create OrderIn table

Revision ID: 2c4f6a88b1d9e
Revises: 719e6b11e909
Create Date: 2026-07-22 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

#revision indentifiers, used by Alembic.
revision: str = '2c4f6a8b1d9e'
down_revision: Union[str, None] = '719e6b11e909'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'OrderIn',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('offer_id', sa.Integer(), nullable=False),
        sa.Column('shop_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('OrderIn')