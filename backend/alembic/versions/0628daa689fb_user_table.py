"""user table

Revision ID: 0628daa689fb
Revises: c6b152321d22
Create Date: 2024-11-10 14:23:40.557909

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = '0628daa689fb'
down_revision: Union[str, None] = 'c6b152321d22'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('phone_number', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('is_verified', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('phone_number')
    )
    
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_phone_number', 'users', ['phone_number'], unique=True)
    
    # Create OTP table
    op.create_table(
        'otp',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(length=12), nullable=False),
        sa.Column('code', sa.String(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('is_used', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_index('ix_otp_user_id', 'otp', ['user_id'])


def downgrade() -> None:
    op.drop_table('otp')
    op.drop_table('users')
