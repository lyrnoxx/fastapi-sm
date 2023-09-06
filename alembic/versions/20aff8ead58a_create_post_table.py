"""create post table

Revision ID: 20aff8ead58a
Revises: 
Create Date: 2023-09-06 17:23:42.966696

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20aff8ead58a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',
    sa.Column('id',sa.Integer,primary_key=True,nullable=False),
    sa.Column('title',sa.String,nullable=False),
    sa.Column('content',sa.String,nullable=False),
    sa.Column('published',sa.Boolean,server_default='TRUE',nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')),
    )

def downgrade() -> None:
    op.drop_table('posts')
