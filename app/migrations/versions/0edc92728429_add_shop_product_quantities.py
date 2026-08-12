from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '0edc92728429'
down_revision: Union[str, None] = '2c4f6a8b1d9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('shops', sa.Column("quantity_1g", sa.Integer(), nullable=False, server_default=sa.text("0")))
    op.add_column("shops", sa.Column("quantity_5g", sa.Integer(), nullable=False, server_default=sa.text("0")))
    op.add_column("shops", sa.Column("quantity_10g", sa.Integer(), nullable=False, server_default=sa.text("0")))

def downgrade() -> None:
    op.drop_column("shops", "quantity_10g")
    op.drop_column("shops", "quantity_5g")
    op.drop_column("shops", "quantity_1g")