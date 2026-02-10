"""alter parlon table add column logo

Revision ID: b5c1be901755
Revises: c0240d883c70
Create Date: 2026-02-03 05:26:55.476447

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5c1be901755'
down_revision: Union[str, Sequence[str], None] = 'c0240d883c70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
               ALTER TABLE parlons
                   ADD COLUMN logo VARCHAR(512) NULL AFTER business_name
               """)



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('parlons', 'logo')

