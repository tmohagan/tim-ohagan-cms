"""add post category

Revision ID: 306fe860d753
Revises: 206fe860d752
Create Date: 2026-10-01 14:55:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '306fe860d753'
down_revision: Union[str, Sequence[str], None] = '206fe860d752'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('category', sa.String(length=100), nullable=True, server_default='Autonomous SRE'))
    op.create_index(op.f('ix_posts_category'), 'posts', ['category'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_posts_category'), table_name='posts')
    op.drop_column('posts', 'category')
