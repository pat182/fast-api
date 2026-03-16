"""seed  MainCategory table

Revision ID: d198e43783cc
Revises: 41ec523bb5c7
Create Date: 2026-02-11 22:36:44.318529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd198e43783cc'
down_revision: Union[str, Sequence[str], None] = '41ec523bb5c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    categories = [
        "brows",
        "facial and aesthetics",
        "hair",
        "hair removal",
        "lashes",
        "make up",
        "massage",
        "nails",
    ]
    op.bulk_insert(
        sa.table(
            "main_categories",
            sa.Column('name',sa.String),
        ),
        [{"name" : cat} for cat in categories],
    )



def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM main_category")
