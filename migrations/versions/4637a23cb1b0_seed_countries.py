"""seed countries

Revision ID: 4637a23cb1b0
Revises: d80b77159d3b
Create Date: 2026-02-02 00:33:43.455253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pycountry

# revision identifiers, used by Alembic.
revision: str = '4637a23cb1b0'
down_revision: Union[str, Sequence[str], None] = 'd80b77159d3b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('countries', sa.Column('create_date', sa.DateTime(), server_default=sa.func.now(), nullable=False))
    op.add_column('countries', sa.Column('update_date', sa.DateTime(), server_default=sa.func.now(), nullable=False))

    countries_table = sa.table(
        'countries',
        sa.column('country_name', sa.String),
        sa.column('code', sa.String),
    )
    data = [{"country_name": country.name, "code": country.alpha_2} for country in pycountry.countries]
    op.bulk_insert(countries_table, data)


def downgrade() -> None:
    op.execute("DELETE FROM countries")
