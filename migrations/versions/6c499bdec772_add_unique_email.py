"""add_unique_email

Revision ID: 6c499bdec772
Revises: a25b62ab1d3b
Create Date: 2024-05-06 23:17:02.370429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c499bdec772'
down_revision: Union[str, None] = 'a25b62ab1d3b'
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
