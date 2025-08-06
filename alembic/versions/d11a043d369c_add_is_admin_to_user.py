"""add_is_admin_to_user

Revision ID: d11a043d369c
Revises: 96ea67854306
Create Date: 2025-08-06 02:29:15.071303

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd11a043d369c'
down_revision: Union[str, Sequence[str], None] = '96ea67854306'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users',
                  sa.Column('is_admin',
                            sa.Boolean(),
                            server_default='false',
                            nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'is_admin')
