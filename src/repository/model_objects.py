import enum
from datetime import UTC, date, datetime

from sqlmodel import Column, Enum, Field, Relationship, SQLModel


def datetime_now_sec():
    return datetime.now(UTC).replace(microsecond=0)


class UsuarioTipoTypes(enum.Enum):
    admin = 'admin'
    treinador = 'treinador'
    externo = 'externo'


class UsuarioTipo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tipo: str = Field(sa_column=Column(Enum(UsuarioTipoTypes)))


class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    email: str = Field(index=False, unique=True)
    hash_password: str
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None

    usuario_tipo_id: int | None = Field(
        default=None, foreign_key='usuariotipo.id'
    )


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
    tipo: str = Field(sa_column=Column(Enum(ObsevacaoTypes)))
    descricao: str
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )

    atleta_id: int | None = Field(default=None, foreign_key='atleta.id')


class CaracteristicaFisica(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    estatura: float | None
    envergadura: float | None
    peso: float | None
    percentual_gordura: float | None
    data_avaliacao: date | None = None
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None

    atleta_id: int | None = Field(default=None, foreign_key='atleta.id')


class CaracteristicaZagueiro(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    estatura_fis: int
    força_fis: int
    passe_curto_fis: int
    passe_longo_fis: int
    jogo_aereo_fis: int
    confronto_defensivo_fis: int
    leitura_jogo_tec: int
    ambidestria_tec: int
    participacao_ofensica_tec: int
    cabeceio_ofensivo_tec: int
    passe_entre_linhas_tec: int
    lideranca_psi: int
    confianca_psi: int
    inteligencia_tatica_psi: int
    competitividade_psi: int
    data_avaliacao: date | None = None
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None

    atleta_id: int | None = Field(default=None, foreign_key='atleta.id')


class CaracteristicaLateral(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    estatura_fis: int
    velocidade_fis: int
    passe_curto_fis: int
    passe_longo_fis: int
    capacidade_aerobia_fis: int
    fechemanento_defensivo_fis: int
    leitura_jogo_tec: int
    participacao_ofensiva_tec: int
    cruzamento_tec: int
    jogo_aereo_tec: int
    conducao_bola_tec: int
    lideranca_psi: int
    confianca_psi: int
    inteligencia_tatica_psi: int
    competitividade_psi: int
    data_avaliacao: date | None = None
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None

    atleta_id: int | None = Field(default=None, foreign_key='atleta.id')


class CaracteristicaGoleiro(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    perfil_fis: int
    maturacao_fis: int
    agilidade_fis: int
    velocidade_membros_superiores_fis: int
    flexibilidade_fis: int
    posicionamento_fis: int
    leitura_jogo_tec: int
    jogo_com_pes_tec: int
    organizacao_da_defesa_tec: int
    dominio_coberturas_e_saidas_tec: int
    lideranca_psi: int
    coragem_psi: int
    concentracao_psi: int
    controle_estresse_psi: int
    data_avaliacao: date | None = None
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None

    atleta_id: int | None = Field(default=None, foreign_key='atleta.id')


class CaracteristicaVolante(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    estatura_fis: int
    forca_fis: int
    passe_curto_fis: int
    capacidade_aerobia_fis: int
    dinamica_fis: int
    visao_espacial_fis: int
    leitura_jogo_tec: int
    dominio_orientado_tec: int
    jogo_aereo_ofensivo_tec: int
    passes_verticais_tec: int
    finalizacao_media_distancia_tec: int
    lideranca_psi: int
    confianca_psi: int
    inteligencia_tatica_psi: int
    competitividade_psi: int
    data_avaliacao: date | None = None
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None

    atleta_id: int | None = Field(default=None, foreign_key='atleta.id')


class CaracteristicaAtacante(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    estatura_fis: int
    velocidade_fis: int
    um_contra_um_ofensivo_fis: int
    desmarques_fis: int
    controle_bola_fis: int
    cruzamentos_fis: int
    finalizacao_fis: int
    visao_espacial_tec: int
    dominio_orientado_tec: int
    dribles_em_diagonal_tec: int
    leitura_jogo_tec: int
    reacao_pos_perda_tec: int
    criatividade_psi: int
    capacidade_decisao_psi: int
    inteligencia_tatica_psi: int
    competitividade_psi: int
    data_avaliacao: date | None = None
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None

    atleta_id: int | None = Field(default=None, foreign_key='atleta.id')


class CaracteristicaMeia(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    estatura_fis: int
    velocidade_fis: int
    leitura_jogo_fis: int
    desmarques_fis: int
    controle_bola_fis: int
    capacidade_aerobia_fis: int
    finalizacao_fis: int
    visao_espacial_tec: int
    dominio_orientado_tec: int
    dribles_tec: int
    organizacao_acao_ofensica_tec: int
    pisada_na_area_para_finalizar_tec: int
    criatividade_psi: int
    capacidade_decisao_psi: int
    confianca_psi: int
    inteligencia_tatica_psi: int
    competitividade_psi: int
    data_avaliacao: date | None = None
    data_criacao: datetime = Field(
        default_factory=datetime_now_sec, nullable=False
    )
    data_atualizado: datetime | None = None

    atleta_id: int | None = Field(default=None, foreign_key='atleta.id')
