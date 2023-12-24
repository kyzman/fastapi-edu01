"""Add content column to post tables

Revision ID: 8bc65b3ce69b
Revises: 4968904382fb
Create Date: 2023-12-24 14:07:17.139187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bc65b3ce69b'
down_revision: Union[str, None] = '4968904382fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
