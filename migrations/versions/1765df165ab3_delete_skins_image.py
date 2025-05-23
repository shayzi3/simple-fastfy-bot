"""delete skins.image

Revision ID: 1765df165ab3
Revises: 1e6939a657b0
Create Date: 2025-05-19 20:16:10.227039

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1765df165ab3'
down_revision: Union[str, None] = '1e6939a657b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('skins', 'image')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('skins', sa.Column('image', sa.VARCHAR(), nullable=False))
    # ### end Alembic commands ###
