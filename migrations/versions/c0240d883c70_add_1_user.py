"""add 1 user

Revision ID: c0240d883c70
Revises: 58672b90b18c
Create Date: 2026-02-02 03:26:56.674157
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

from app.core.security import SecurityInstance  # import your hasher

revision: str = 'c0240d883c70'
down_revision: Union[str, Sequence[str], None] = '58672b90b18c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column("users", sa.Column("create_date", sa.DateTime(), server_default=sa.func.now(), nullable=False))
    op.add_column("users", sa.Column("update_date", sa.DateTime(), server_default=sa.func.now(), nullable=False))

    users_table = sa.table(
        "users",
        sa.column("email", sa.String),
        sa.column("password", sa.String),
        sa.column("role_id", sa.Integer),
        sa.column("verified", sa.Boolean),
        sa.column("parlon_id", sa.String(36)),  # nullable FK
    )

    # Hash passwords with your Security class
    pw = SecurityInstance.hash_password("test123")

    op.bulk_insert(users_table, [
        {"email": "thebackdoors182@gmail.com", "password": pw, "role_id": 1, "verified": True, "parlon_id": None},
        {"email": "patrickc@parlon.ph", "password": pw, "role_id": 2, "verified": True, "parlon_id": "4111fbae-07b3-4858-bf67-14db596c4337"},
        {"email": "patrick.chua182@gmail.com", "password": pw, "role_id": 3, "verified": True, "parlon_id": "4111fbae-07b3-4858-bf67-14db596c4337"},
    ])


def downgrade() -> None:
    op.execute(
        "DELETE FROM users WHERE email IN "
        "('thebackdoors182@gmail.com','patrickc@parlon.ph','patrick.chua182@gmail.com')"
    )
    op.drop_column("users", "create_date")
    op.drop_column("users", "update_date")
