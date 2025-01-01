"""adding chat tables

Revision ID: f64fb1eee242
Revises: d3292de82be9
Create Date: 2025-01-01 13:34:55.809688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f64fb1eee242'
down_revision: Union[str, None] = '685b482686ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'chat_sessions',
        sa.Column('id', sa.String(length=12),primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('user_id', sa.String(length=12), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('last_message_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        
        # Primary key and foreign key constraints
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(
            ['user_id'], ['users.id'],
            ondelete='CASCADE'
        )
    )

    
    # Create chat_messages table
    op.create_table(
        'chat_messages',
        sa.Column('id', sa.String(length=12), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('session_id', sa.String(length=12), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('is_bot', sa.Boolean(), nullable=False, server_default='false'),
        
        # Primary key and foreign key constraints
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(
            ['session_id'], ['chat_sessions.id'],
            ondelete='CASCADE'
        )
    )
    



def downgrade() -> None:
    op.drop_table('chat_messages')
    op.drop_table('chat_sessions')
    
