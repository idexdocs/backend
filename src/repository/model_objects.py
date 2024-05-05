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


class PosicaoTypes(enum.Enum):
    atacante = 'atacante'
    goleiro = 'goleiro'
    lateral = 'lateral'
    meia = 'meia'
    volante = 'volante'
    zagueiro = 'zagueiro'


class Posicao(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    primeira: str = Field(sa_column=Column(Enum(PosicaoTypes)))
    segunda: str | None = Field(sa_column=Column(Enum(PosicaoTypes)))
    terceira: str | None = Field(sa_column=Column(Enum(PosicaoTypes)))
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None

    atleta_id: int = Field(default=None, foreign_key='atleta.id')


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


class HistoricoControle(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    quantidade: int
    preco: float
    data_controle: date
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


class CaracteristicaFisica(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    estatura: float | None
    envergadura: float | None
    peso: float | None
    percentual_gordura: float | None
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None

    atleta_id: int | None = Field(default=None, foreign_key='atleta.id')


class CaracteristicaZagueiro(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    estatura: int
    força: int
    passe_curto: int
    passe_longo: int
    jogo_aereo: int
    confronto_defensivo: int
    leitura_jogo: int
    ambidestria: int
    participacao_ofensica: int
    cabeceio_ofensivo: int
    passe_entre_linhas: int
    lideranca: int
    confianca: int
    inteligencia_tatica: int
    competitividade: int
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None

    atleta_id: int | None = Field(default=None, foreign_key='atleta.id')


class CaracteristicaLateral(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    estatura: int
    velocidade: int
    passe_curto: int
    passe_longo: int
    capacidade_aerobia: int
    fechemanento_defensivo: int
    leitura_jogo: int
    participacao_ofensiva: int
    cruzamento: int
    jogo_aereo: int
    conducao_bola: int
    lideranca: int
    confianca: int
    inteligencia_tatica: int
    competitividade: int
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None

    atleta_id: int | None = Field(default=None, foreign_key='atleta.id')


class CaracteristicaGoleiro(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    perfil: int
    maturacao: int
    agilidade: int
    velocidade_membros_superiores: int
    flexibilidade: int
    leitura_jogo: int
    jogo_com_pes: int
    organizacao_da_defesa: int
    dominio_coberturas_e_saidas: int
    lideranca: int
    coragem: int
    concentracao: int
    controle_estresse: int
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None

    atleta_id: int | None = Field(default=None, foreign_key='atleta.id')


class CaracteristicaVolante(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    estatura: int
    forca: int
    passe_curto: int
    capacidade_aerobia: int
    dinamica: int
    visao_espacial: int
    leitura_jogo: int
    dominio_orientado: int
    jogo_aereo_ofensivo: int
    passes_verticais: int
    finalizacao_media_distancia: int
    lideranca: int
    confianca: int
    inteligencia_tatica: int
    competitividade: int
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None

    atleta_id: int | None = Field(default=None, foreign_key='atleta.id')


class CaracteristicaAtacante(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    estatura: int
    velocidade: int
    um_contra_um_ofensivo: int
    desmarques: int
    controle_bola: int
    cruzamentos: int
    finalizacao: int
    visao_espacial: int
    dominio_orientado: int
    dribles_em_diagonal: int
    leitura_jogo: int
    reacao_pos_perda: int
    criatividade: int
    capacidade_decisao: int
    inteligencia_tatica: int
    competitividade: int
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None

    atleta_id: int | None = Field(default=None, foreign_key='atleta.id')


class CaracteristicaMeia(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    estatura: int
    velocidade: int
    leitura_jogo: int
    desmarques: int
    controle_bola: int
    capacidade_aerobia: int
    finalizacao: int
    visao_espacial: int
    dominio_orientado: int
    dribles: int
    organizacao_acao_ofensica: int
    pisada_na_area_para_finalizar: int
    criatividade: int
    capacidade_decisao: int
    confianca: int
    inteligencia_tatica: int
    competitividade: int
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None

    atleta_id: int | None = Field(default=None, foreign_key='atleta.id')
