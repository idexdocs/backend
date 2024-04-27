"""remover_atleta_clube

Revision ID: b509b0b19669
Revises: aa30511a5296
Create Date: 2024-04-27 00:27:26.767855

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b509b0b19669'
down_revision: Union[str, None] = 'aa30511a5296'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('atletaclube')
    op.add_column('clube', sa.Column('atleta_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'clube', 'atleta', ['atleta_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'clube', type_='foreignkey')
    op.drop_column('clube', 'atleta_id')
    op.create_table('atletaclube',
    sa.Column('atleta_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('clube_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['atleta_id'], ['atleta.id'], name='FK__atletaclu__atlet__412EB0B6'),
    sa.ForeignKeyConstraint(['clube_id'], ['clube.id'], name='FK__atletaclu__clube__4222D4EF'),
    sa.PrimaryKeyConstraint('atleta_id', 'clube_id', name='PK__atletacl__8C2B2DDCA5A88EAD')
    )
    # ### end Alembic commands ###
