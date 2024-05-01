import enum
from datetime import UTC, date, datetime

from sqlmodel import Column, Enum, Field, Relationship, SQLModel


def datetime_now_sec():
    return datetime.now(UTC).replace(microsecond=0)


# Many to many relationships
class AtletaContrato(SQLModel, table=True):
    data_inicio: date
    data_fim: date
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None

    atleta_id: int = Field(
        default=None, foreign_key='atleta.id', primary_key=True
    )
    contrato_id: int = Field(
        default=None, foreign_key='contrato.id', primary_key=True
    )


class AtletaPosicao(SQLModel, table=True):
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    atleta_id: int = Field(default=None, foreign_key='atleta.id')
    posicao_id: int = Field(
        default=None, foreign_key='posicao.id', primary_key=True
    )


class AtletaCaracteristica(SQLModel, table=True):
    atleta_id: int = Field(
        default=None, foreign_key='atleta.id', primary_key=True
    )
    caracteristica_id: int = Field(
        default=None, foreign_key='posicao.id', primary_key=True
    )


class Atleta(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    data_nascimento: date
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None
    ativo: bool = True

    contratos: list['Contrato'] = Relationship(
        back_populates='atletas', link_model=AtletaContrato
    )

    posicoes: list['Posicao'] = Relationship(
        back_populates='atletas', link_model=AtletaPosicao
    )


class Perfil(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None


class Caracteristica(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None

    perfil_id: int | None = Field(default=None, foreign_key='perfil.id')


class Contrato(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tipo: str

    atletas: list['Atleta'] = Relationship(
        back_populates='contratos', link_model=AtletaContrato
    )


class Posicao(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None

    atletas: list['Atleta'] = Relationship(
        back_populates='posicoes', link_model=AtletaPosicao
    )


class Relacionamento(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    receptividade_contrato: int
    satisfacao_empresa: int
    satisfacao_clube: int
    relacao_familiares: int
    influencias_externas: int
    pendencia_empresa: bool
    pendencia_clube: bool
    data_avaliacao: date
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None

    atleta_id: int | None = Field(default=None, foreign_key='atleta.id')


class HistoricoClube(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    data_inicio: date
    data_fim: date | None
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None

    atleta_id: int | None = Field(default=None, foreign_key='atleta.id')


class HistoricoCompeticao(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    data_competicao: date
    jogos_completos: int
    jogos_parciais: int
    minutagem: int
    gols: int
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None

    atleta_id: int | None = Field(default=None, foreign_key='atleta.id')


class HistoricoLesao(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    data_lesao: date
    descricao: str
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None

    atleta_id: int | None = Field(default=None, foreign_key='atleta.id')


class HistoricoMaterial(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    quantidade: int
    preco: float
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None

    atleta_id: int | None = Field(default=None, foreign_key='atleta.id')


class ObsevacaoTypes(enum.Enum):
    desempenho = 'desempenho'
    relacionamento = 'relacionamento'


class HistoricoObservacao(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    descricao: str
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )

    tipo: str = Field(sa_column=Column(Enum(ObsevacaoTypes)))
    atleta_id: int | None = Field(default=None, foreign_key='atleta.id')
