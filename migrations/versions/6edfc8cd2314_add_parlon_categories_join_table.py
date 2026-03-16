"""add parlon_categories join table

Revision ID: 6edfc8cd2314
Revises: d198e43783cc
Create Date: 2026-02-13 18:12:40.453017

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '6edfc8cd2314'
down_revision: Union[str, Sequence[str], None] = 'd198e43783cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "parlon_categories",
        sa.Column("parlon_id", sa.String(36), nullable=False),
        sa.Column("main_category_id", sa.Integer(), nullable=False),
        sa.Column("create_date", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "update_date",
            sa.DateTime(), server_default=sa.func.now(),
            onupdate=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(
            ["parlon_id"],
            ["parlons.id"],
            ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["main_category_id"],
            ["main_categories.id"],
            ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("parlon_id", "main_category_id")
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("parlon_categories")
