"""Create tables for RawFile and ExtractedData

Revision ID: c6b152321d22
Revises: 
Create Date: 2024-11-09 20:38:30.748067

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c6b152321d22'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'raw_files',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('content', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=sa.func.now())
    )

    # Create the extracted_data table
    op.create_table(
        'extracted_data',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('file_id', sa.Integer, sa.ForeignKey('raw_files.id'), nullable=False),
        sa.Column('extracted_data', sa.JSON, nullable=True),
        sa.Column('file_data', sa.LargeBinary, nullable=True),
    )


def downgrade() -> None:
    # Drop the extracted_data table
    op.drop_table('extracted_data')

    # Drop the raw_files table
    op.drop_table('raw_files')
