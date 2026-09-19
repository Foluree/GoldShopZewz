"""create appeal tables

Revision ID: d3b7e9c51a40
Revises: 0edc92728429
Create Date: 2026-09-05 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd3b7e9c51a40'
down_revision: Union[str, None] = '0edc92728429'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'Undertable_appeal',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('email_user', sa.String(), nullable=False),
        sa.Column('table_name', sa.String(), nullable=False),
        sa.Column('appeal', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['UserProfiles.id'], name='fk_undertable_user'),
        sa.PrimaryKeyConstraint('id'),
    )
    for sub in ('PrayersAppeal', 'Request', 'Complaint', 'Gratitude'):
        op.create_table(
            sub,
            sa.Column('id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['id'], ['Undertable_appeal.id'], name=f'fk_{sub.lower()}_parent'),
            sa.PrimaryKeyConstraint('id'),
        )
    op.create_table(
        'TypesAppeal',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('table_ref', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('TypesAppeal')
    for sub in ('PrayersAppeal', 'Request', 'Complaint', 'Gratitude'):
        op.drop_table(sub)
    op.drop_table('Undertable_appeal')