"""add fk for posts

Revision ID: 5ed3a7d55f2d
Revises: 921d008e63eb
Create Date: 2023-09-06 19:37:42.318893

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ed3a7d55f2d'
down_revision: Union[str, None] = '921d008e63eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id',sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False))


def downgrade() -> None:
    op.drop_column('posts','user_id')
