"""Add to_delete field to download table

Revision ID: f0b87f1198a2
Revises: 6b54a1283344
Create Date: 2024-05-04 17:23:29.795675

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0b87f1198a2'
down_revision: Union[str, None] = '6b54a1283344'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('download', sa.Column('to_delete', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('download', 'to_delete')
    # ### end Alembic commands ###
