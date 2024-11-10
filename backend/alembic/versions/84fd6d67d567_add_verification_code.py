"""add verification code

Revision ID: 84fd6d67d567
Revises: 0628daa689fb
Create Date: 2024-11-10 16:07:03.249670

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84fd6d67d567'
down_revision: Union[str, None] = '0628daa689fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('verification_code', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'verification_code')
