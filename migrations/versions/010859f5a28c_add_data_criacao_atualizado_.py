"""add_data_criacao_atualizado_relacionamento

Revision ID: 010859f5a28c
Revises: 8fd301618910
Create Date: 2024-04-23 19:42:30.666304

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '010859f5a28c'
down_revision: Union[str, None] = '8fd301618910'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('relacionamento', sa.Column('data_criacao', sa.DateTime(), nullable=False))
    op.add_column('relacionamento', sa.Column('data_atualizado', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('relacionamento', 'data_atualizado')
    op.drop_column('relacionamento', 'data_criacao')
    # ### end Alembic commands ###
