"""add_unique_email

Revision ID: a25b62ab1d3b
Revises: f1a96c5313df
Create Date: 2024-05-06 23:15:15.277146

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a25b62ab1d3b'
down_revision: Union[str, None] = 'f1a96c5313df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###