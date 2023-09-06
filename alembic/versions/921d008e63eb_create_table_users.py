"""create table users

Revision ID: 921d008e63eb
Revises: 20aff8ead58a
Create Date: 2023-09-06 17:39:00.843652

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '921d008e63eb'
down_revision: Union[str, None] = '20aff8ead58a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id',sa.Integer,primary_key=True,nullable=False),
    sa.Column('email',sa.String,nullable=False,unique=True),
   sa.Column('password',sa.String,nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()'))
)


def downgrade() -> None:
    op.drop_table('users')