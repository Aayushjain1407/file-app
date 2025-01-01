"""Removing column verification _code from users

Revision ID: 9e482bf1fbe4
Revises: f64fb1eee242
Create Date: 2025-01-01 15:51:04.636894

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e482bf1fbe4'
down_revision: Union[str, None] = 'f64fb1eee242'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('users', 'verification_code')


def downgrade() -> None:
    op.add_column('users', sa.Column('verification_code', sa.String(length=255), nullable=True))
