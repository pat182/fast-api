"""create role table and add fk to user then drop created_at and updated_at col in countries, with seeders

Revision ID: d80b77159d3b
Revises: 2d3ba8f73df0
Create Date: 2026-02-01 23:16:08.622541
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd80b77159d3b'
down_revision: Union[str, Sequence[str], None] = '2d3ba8f73df0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create roles table
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('create_date', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column('update_date', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_roles_id'), 'roles', ['id'], unique=False)
    # Seed roles
    op.bulk_insert(
        sa.table(
            'roles',
            sa.column('id', sa.Integer),
            sa.column('name', sa.String)
        ), [{"id": 1, "name": "superadmin"}, {"id": 2, "name": "adminpartner"}, {"id": 3, "name": "employee"}, ]

    )
    ###################
    # Add role_id column to users (portable)
    op.add_column('users', sa.Column('role_id', sa.Integer(), nullable=False))
    # Reorder column for MySQL
    op.execute("ALTER TABLE users MODIFY COLUMN role_id INT NOT NULL AFTER id")

    # Add foreign key
    op.create_foreign_key('fk_users_role', 'users', 'roles', ['role_id'], ['id'])

    # Drop columns from countries
    op.drop_column('countries', 'created_at')
    op.drop_column('countries', 'updated_at')


def downgrade() -> None:
    """Downgrade schema."""
    # Restore columns in countries
    op.add_column('countries', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('countries', sa.Column('updated_at', sa.DateTime(), nullable=True))

    # Remove foreign key and role_id column from users
    op.drop_constraint('fk_users_role', 'users', type_='foreignkey')
    op.drop_column('users', 'role_id')

    # Drop index and roles table
    op.drop_index(op.f('ix_roles_id'), table_name='roles')
    op.drop_table('roles')