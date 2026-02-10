"""alter parlon table add visibility column and adjust business_name index

Revision ID: 9e7f2624ebd2
Revises: b5c1be901755
Create Date: 2026-02-05 00:10:23.517275
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '9e7f2624ebd2'
down_revision: Union[str, Sequence[str], None] = 'b5c1be901755'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the unique constraint/index on business_name if it exists
    # Adjust the name to match your DB (check SHOW INDEXES FROM parlon;)
    op.drop_constraint("business_name", "parlons", type_="unique")

    # Recreate as a non-unique index using SQLAlchemy syntax
    op.create_index("idx_business_name", "parlons", ["business_name"], unique=False)

    # Add visibility column with default false after logo (MySQL-specific)
    op.execute("""
        ALTER TABLE parlons
        ADD COLUMN visibility BOOLEAN NOT NULL DEFAULT FALSE AFTER logo
    """)




def downgrade() -> None:
    # Remove visibility column
    op.execute("""
        ALTER TABLE parlons
        DROP COLUMN visibility
    """)

    # Drop the non-unique index
    op.drop_index("idx_business_name", table_name="parlons")

    # Restore unique constraint/index
    op.create_unique_constraint("business_name", "parlons", ["business_name"])