"""Add MainCategory table

Revision ID: 41ec523bb5c7
Revises: 9e7f2624ebd2
Create Date: 2026-02-11 22:23:44.492618

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '41ec523bb5c7'
down_revision: Union[str, Sequence[str], None] = '9e7f2624ebd2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "main_categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), index=True),
        sa.Column('create_date', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('update_date', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("main_category")

    # ### end Alembic commands ###
