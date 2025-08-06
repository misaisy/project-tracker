"""add_cascade_delete_to_comments

Revision ID: 86357d97baf8
Revises: d11a043d369c
Create Date: 2025-08-06 02:50:55.487759

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86357d97baf8'
down_revision: Union[str, Sequence[str], None] = 'd11a043d369c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint('comments_task_id_fkey', 'comments', type_='foreignkey')

    op.create_foreign_key(
        'comments_task_id_fkey',
        'comments',
        'tasks',
        ['task_id'],
        ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('comments_task_id_fkey', 'comments', type_='foreignkey')
    op.create_foreign_key(
        'comments_task_id_fkey',
        'comments',
        'tasks',
        ['task_id'],
        ['id']
    )
