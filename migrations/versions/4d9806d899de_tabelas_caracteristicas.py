"""tabelas_caracteristicas

Revision ID: 4d9806d899de
Revises: a2226cd86e5e
Create Date: 2024-05-02 20:40:54.523456

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d9806d899de'
down_revision: Union[str, None] = 'a2226cd86e5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('caracteristicaatacante',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('estatura', sa.Integer(), nullable=False),
    sa.Column('velocidade', sa.Integer(), nullable=False),
    sa.Column('um_contra_um_ofensivo', sa.Integer(), nullable=False),
    sa.Column('desmarques', sa.Integer(), nullable=False),
    sa.Column('controle_bola', sa.Integer(), nullable=False),
    sa.Column('cruzamentos', sa.Integer(), nullable=False),
    sa.Column('finalizacao', sa.Integer(), nullable=False),
    sa.Column('visao_espacial', sa.Integer(), nullable=False),
    sa.Column('dominio_orientado', sa.Integer(), nullable=False),
    sa.Column('dribles_em_diagonal', sa.Integer(), nullable=False),
    sa.Column('leitura_jogo', sa.Integer(), nullable=False),
    sa.Column('reacao_pos_perda', sa.Integer(), nullable=False),
    sa.Column('criatividade', sa.Integer(), nullable=False),
    sa.Column('capacidade_decisao', sa.Integer(), nullable=False),
    sa.Column('inteligencia_tatica', sa.Integer(), nullable=False),
    sa.Column('competitividade', sa.Integer(), nullable=False),
    sa.Column('data_criacao', sa.DateTime(), nullable=False),
    sa.Column('data_atualizado', sa.DateTime(), nullable=True),
    sa.Column('atleta_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['atleta_id'], ['atleta.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('caracteristicafisica',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('estatura', sa.Float(), nullable=True),
    sa.Column('envergadura', sa.Float(), nullable=True),
    sa.Column('peso', sa.Float(), nullable=True),
    sa.Column('percentual_gordura', sa.Float(), nullable=True),
    sa.Column('data_criacao', sa.DateTime(), nullable=False),
    sa.Column('data_atualizado', sa.DateTime(), nullable=True),
    sa.Column('atleta_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['atleta_id'], ['atleta.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('caracteristicagoleiro',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('perfil', sa.Integer(), nullable=False),
    sa.Column('maturacao', sa.Integer(), nullable=False),
    sa.Column('agilidade', sa.Integer(), nullable=False),
    sa.Column('velocidade_membros_superiores', sa.Integer(), nullable=False),
    sa.Column('flexibilidade', sa.Integer(), nullable=False),
    sa.Column('leitura_jogo', sa.Integer(), nullable=False),
    sa.Column('jogo_com_pes', sa.Integer(), nullable=False),
    sa.Column('organizacao_da_defesa', sa.Integer(), nullable=False),
    sa.Column('dominio_coberturas_e_saidas', sa.Integer(), nullable=False),
    sa.Column('lideranca', sa.Integer(), nullable=False),
    sa.Column('coragem', sa.Integer(), nullable=False),
    sa.Column('concentracao', sa.Integer(), nullable=False),
    sa.Column('controle_estresse', sa.Integer(), nullable=False),
    sa.Column('data_criacao', sa.DateTime(), nullable=False),
    sa.Column('data_atualizado', sa.DateTime(), nullable=True),
    sa.Column('atleta_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['atleta_id'], ['atleta.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('caracteristicalateral',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('estatura', sa.Integer(), nullable=False),
    sa.Column('velocidade', sa.Integer(), nullable=False),
    sa.Column('passe_curto', sa.Integer(), nullable=False),
    sa.Column('passe_longo', sa.Integer(), nullable=False),
    sa.Column('capacidade_aerobia', sa.Integer(), nullable=False),
    sa.Column('fechemanento_defensivo', sa.Integer(), nullable=False),
    sa.Column('leitura_jogo', sa.Integer(), nullable=False),
    sa.Column('participacao_ofensiva', sa.Integer(), nullable=False),
    sa.Column('cruzamento', sa.Integer(), nullable=False),
    sa.Column('jogo_aereo', sa.Integer(), nullable=False),
    sa.Column('conducao_bola', sa.Integer(), nullable=False),
    sa.Column('lideranca', sa.Integer(), nullable=False),
    sa.Column('confianca', sa.Integer(), nullable=False),
    sa.Column('inteligencia_tatica', sa.Integer(), nullable=False),
    sa.Column('competitividade', sa.Integer(), nullable=False),
    sa.Column('data_criacao', sa.DateTime(), nullable=False),
    sa.Column('data_atualizado', sa.DateTime(), nullable=True),
    sa.Column('atleta_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['atleta_id'], ['atleta.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('caracteristicameia',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('estatura', sa.Integer(), nullable=False),
    sa.Column('velocidade', sa.Integer(), nullable=False),
    sa.Column('leitura_jogo', sa.Integer(), nullable=False),
    sa.Column('desmarques', sa.Integer(), nullable=False),
    sa.Column('controle_bola', sa.Integer(), nullable=False),
    sa.Column('capacidade_aerobia', sa.Integer(), nullable=False),
    sa.Column('finalizacao', sa.Integer(), nullable=False),
    sa.Column('visao_espacial', sa.Integer(), nullable=False),
    sa.Column('dominio_orientado', sa.Integer(), nullable=False),
    sa.Column('dribles', sa.Integer(), nullable=False),
    sa.Column('organizacao_acao_ofensica', sa.Integer(), nullable=False),
    sa.Column('pisada_na_area_para_finalizar', sa.Integer(), nullable=False),
    sa.Column('criatividade', sa.Integer(), nullable=False),
    sa.Column('capacidade_decisao', sa.Integer(), nullable=False),
    sa.Column('confianca', sa.Integer(), nullable=False),
    sa.Column('inteligencia_tatica', sa.Integer(), nullable=False),
    sa.Column('competitividade', sa.Integer(), nullable=False),
    sa.Column('data_criacao', sa.DateTime(), nullable=False),
    sa.Column('data_atualizado', sa.DateTime(), nullable=True),
    sa.Column('atleta_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['atleta_id'], ['atleta.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('caracteristicavolante',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('estatura', sa.Integer(), nullable=False),
    sa.Column('forca', sa.Integer(), nullable=False),
    sa.Column('passe_curto', sa.Integer(), nullable=False),
    sa.Column('capacidade_aerobia', sa.Integer(), nullable=False),
    sa.Column('dinamica', sa.Integer(), nullable=False),
    sa.Column('visao_espacial', sa.Integer(), nullable=False),
    sa.Column('leitura_jogo', sa.Integer(), nullable=False),
    sa.Column('dominio_orientado', sa.Integer(), nullable=False),
    sa.Column('jogo_aereo_ofensivo', sa.Integer(), nullable=False),
    sa.Column('passes_verticais', sa.Integer(), nullable=False),
    sa.Column('finalizacao_media_distancia', sa.Integer(), nullable=False),
    sa.Column('lideranca', sa.Integer(), nullable=False),
    sa.Column('confianca', sa.Integer(), nullable=False),
    sa.Column('inteligencia_tatica', sa.Integer(), nullable=False),
    sa.Column('competitividade', sa.Integer(), nullable=False),
    sa.Column('data_criacao', sa.DateTime(), nullable=False),
    sa.Column('data_atualizado', sa.DateTime(), nullable=True),
    sa.Column('atleta_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['atleta_id'], ['atleta.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('caracteristicazagueiro',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('estatura', sa.Integer(), nullable=False),
    sa.Column('força', sa.Integer(), nullable=False),
    sa.Column('passe_curto', sa.Integer(), nullable=False),
    sa.Column('passe_longo', sa.Integer(), nullable=False),
    sa.Column('jogo_aereo', sa.Integer(), nullable=False),
    sa.Column('confronto_defensivo', sa.Integer(), nullable=False),
    sa.Column('leitura_jogo', sa.Integer(), nullable=False),
    sa.Column('ambidestria', sa.Integer(), nullable=False),
    sa.Column('participacao_ofensica', sa.Integer(), nullable=False),
    sa.Column('cabeceio_ofensivo', sa.Integer(), nullable=False),
    sa.Column('passe_entre_linhas', sa.Integer(), nullable=False),
    sa.Column('lideranca', sa.Integer(), nullable=False),
    sa.Column('confianca', sa.Integer(), nullable=False),
    sa.Column('inteligencia_tatica', sa.Integer(), nullable=False),
    sa.Column('competitividade', sa.Integer(), nullable=False),
    sa.Column('data_criacao', sa.DateTime(), nullable=False),
    sa.Column('data_atualizado', sa.DateTime(), nullable=True),
    sa.Column('atleta_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['atleta_id'], ['atleta.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('caracteristicazagueiro')
    op.drop_table('caracteristicavolante')
    op.drop_table('caracteristicameia')
    op.drop_table('caracteristicalateral')
    op.drop_table('caracteristicagoleiro')
    op.drop_table('caracteristicafisica')
    op.drop_table('caracteristicaatacante')
    # ### end Alembic commands ###
