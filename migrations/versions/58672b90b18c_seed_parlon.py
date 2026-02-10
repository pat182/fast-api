"""seed parlons with readable UUIDs

Revision ID: 58672b90b18c
Revises: 4637a23cb1b0
Create Date: 2026-02-02 01:24:11.644003
"""
import os
import json
import uuid
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from app.core.config import settings

# Revision identifiers
revision: str = '58672b90b18c'
down_revision: Union[str, Sequence[str], None] = '4637a23cb1b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema and seed parlons with readable UUIDs."""

    # Drop the existing foreign key constraint
    op.drop_constraint("fk_users_parlon", "users", type_="foreignkey")

    # Alter both columns to CHAR(36)
    op.alter_column(
        "parlons",
        "id",
        existing_type=sa.LargeBinary(16),
        type_=sa.String(36),
        existing_nullable=False
    )
    op.alter_column(
        "users",
        "parlon_id",
        existing_type=sa.LargeBinary(16),
        type_=sa.String(36),
        existing_nullable=True  # adjust if NOT NULL
    )

    # Recreate the foreign key constraint
    op.create_foreign_key(
        "fk_users_parlon",
        "users",
        "parlons",
        ["parlon_id"],
        ["id"]
    )

    # Add timestamp columns
    op.add_column(
        "parlons",
        sa.Column("create_date", sa.DateTime, server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.add_column(
        "parlons",
        sa.Column("update_date", sa.DateTime, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), nullable=False),
    )

    # Load seed data
    file_path = os.path.join(settings.BASE_DIR, "old_data", "parlons-data.json")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Generate readable UUIDs
    for entry in data:
        entry["id"] = str(uuid.uuid4())

    # Bulk insert
    op.bulk_insert(
        sa.table(
            "parlons",
            sa.column("id", sa.String(36)),
            sa.column("country_id", sa.Integer),
            sa.column("business_name", sa.String),
        ),
        data,
    )


def downgrade() -> None:
    """Downgrade schema and remove seeded parlons."""

    # Drop the foreign key constraint
    op.drop_constraint("fk_users_parlon", "users", type_="foreignkey")

    # Delete seeded data and drop timestamp columns
    op.execute("DELETE FROM parlons")
    op.drop_column("parlons", "create_date")
    op.drop_column("parlons", "update_date")

    # Revert both columns back to BINARY(16)
    op.alter_column(
        "users",
        "parlon_id",
        existing_type=sa.String(36),
        type_=sa.LargeBinary(16),
        existing_nullable=True
    )
    op.alter_column(
        "parlons",
        "id",
        existing_type=sa.String(36),
        type_=sa.LargeBinary(16),
        existing_nullable=False
    )

    # Recreate the foreign key constraint
    op.create_foreign_key(
        "fk_users_parlon",
        "users",
        "parlons",
        ["parlon_id"],
        ["id"]
    )