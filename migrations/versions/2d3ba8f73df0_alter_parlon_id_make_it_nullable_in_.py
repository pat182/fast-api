"""alter parlon_id make it nullable in user table

Revision ID: 2d3ba8f73df0
Revises: 95446ad1dcc7
Create Date: 2026-02-01 22:30:32.821793

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision: str = '2d3ba8f73df0'
down_revision: Union[str, Sequence[str], None] = '95446ad1dcc7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'users',
        'parlon_id',
        existing_type=mysql.BINARY(16),
        nullable=True
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'users',
        'parlon_id',
        existing_type=mysql.BINARY(16),
        nullable=False
    )


