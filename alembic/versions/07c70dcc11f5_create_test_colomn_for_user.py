"""Create test colomn for user

Revision ID: 07c70dcc11f5
Revises: 
Create Date: 2024-10-06 16:59:53.057843

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07c70dcc11f5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',sa.Column('test',sa.String(),nullable=True))


def downgrade() -> None:
    op.drop_column('users','test')
