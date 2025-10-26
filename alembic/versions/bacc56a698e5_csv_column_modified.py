"""csv column modified with JSONB and GIN index

Revision ID: bacc56a698e5
Revises: b398732fe4b1
Create Date: 2025-10-26 09:24:25.250867
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'bacc56a698e5'
down_revision: Union[str, Sequence[str], None] = 'b398732fe4b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Convert columns from JSON → JSONB
    op.alter_column(
        'csvs',
        'columns',
        existing_type=postgresql.JSON(),
        type_=postgresql.JSONB(),
        existing_nullable=True
    )

    # Add GIN index for faster JSONB queries
    op.create_index(
        'ix_csvs_columns',
        'csvs',
        ['columns'],
        postgresql_using='gin'
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop the GIN index
    op.drop_index('ix_csvs_columns', table_name='csvs')

    # Convert columns back from JSONB → JSON
    op.alter_column(
        'csvs',
        'columns',
        existing_type=postgresql.JSONB(),
        type_=postgresql.JSON(),
        existing_nullable=True
    )
