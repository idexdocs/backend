"""adicionar_data_atualizado_tabela_contrato

Revision ID: d880b040be88
Revises: 0d176e78452a
Create Date: 2024-05-16 22:27:45.304830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd880b040be88'
down_revision: Union[str, None] = '0d176e78452a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contrato', sa.Column('data_atualizado', sa.DateTime(), nullable=True))
    op.add_column('contratoversao', sa.Column('data_inicio', sa.Date(), nullable=False))
    op.add_column('contratoversao', sa.Column('data_termino', sa.Date(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contratoversao', 'data_termino')
    op.drop_column('contratoversao', 'data_inicio')
    op.drop_column('contrato', 'data_atualizado')
    # ### end Alembic commands ###