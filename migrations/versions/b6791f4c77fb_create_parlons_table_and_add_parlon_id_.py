"""create parlons table and add parlon_id to users

Revision ID: b6791f4c77fb
Revises: 928a18a5a3b1
Create Date: 2026-02-01 19:52:23.786814

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'b6791f4c77fb'
down_revision: Union[str, Sequence[str], None] = '928a18a5a3b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'parlons',
        sa.Column('id', sa.BINARY(length=16), nullable=False),
        sa.Column('business_name', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('business_name')
    )

    # Add parlon_id column after id
    op.execute("""
        ALTER TABLE users
        ADD COLUMN parlon_id BINARY(16) NULL AFTER id
    """)

    # Add foreign key constraint
    op.create_foreign_key(
        "fk_users_parlon",   # name of the constraint
        "users",             # source table
        "parlons",           # target table
        ["parlon_id"],       # local column(s)
        ["id"]               # remote column(s)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_users_parlon", "users", type_="foreignkey")
    op.drop_column("users", "parlon_id")
    op.drop_table("parlons")