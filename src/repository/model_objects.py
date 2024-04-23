from datetime import UTC, date, datetime

from sqlmodel import Field, Relationship, SQLModel


def datetime_now_sec():
    return datetime.now(UTC).replace(microsecond=0)


# Many to many relationships
class AtletaClube(SQLModel, table=True):
    atleta_id: int = Field(default=None, foreign_key="atleta.id", primary_key=True)
    clube_id: int = Field(default=None, foreign_key="clube.id", primary_key=True)


class AtletaContrato(SQLModel, table=True):
    atleta_id: int = Field(default=None, foreign_key="atleta.id", primary_key=True)
    contrato_id: int = Field(default=None, foreign_key="contrato.id", primary_key=True)
    data_inicio: date
    data_fim: date
    data_criacao: datetime = Field(default_factory=datetime_now_sec, nullable=False)
    data_atualizado: datetime | None = None


class AtletaPosicao(SQLModel, table=True):
    atleta_id: int = Field(default=None, foreign_key="atleta.id", primary_key=True)
    posicao_id: int = Field(default=None, foreign_key="posicao.id", primary_key=True)


class Atleta(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    data_nascimento: date
    data_criacao: datetime = Field(default_factory=datetime_now_sec, nullable=False)
    data_atualizado: datetime | None = None
    ativo: bool = True

    clubes: list["Clube"] = Relationship(
        back_populates="atletas", link_model=AtletaClube
    )

    contratos: list["Contrato"] = Relationship(
        back_populates="atletas", link_model=AtletaContrato
    )

    posicoes: list["Posicao"] = Relationship(
        back_populates="atletas", link_model=AtletaPosicao
    )


class Clube(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    data_criacao: datetime = Field(default_factory=datetime_now_sec, nullable=False)
    data_atualizado: datetime | None = None
    ativo: bool = True

    atletas: list["Atleta"] = Relationship(
        back_populates="clubes", link_model=AtletaClube
    )


class Contrato(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tipo: str

    atletas: list["Atleta"] = Relationship(
        back_populates="contratos", link_model=AtletaContrato
    )


class Posicao(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    data_criacao: datetime = Field(default_factory=datetime_now_sec, nullable=False)
    data_atualizado: datetime | None = None

    atletas: list["Atleta"] = Relationship(
        back_populates="posicoes", link_model=AtletaPosicao
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
    data_criacao: datetime = Field(default_factory=datetime_now_sec, nullable=False)
    data_atualizado: datetime | None = None

    atleta_id: int | None = Field(default=None, foreign_key="atleta.id") 