from datetime import datetime

from pydantic import BaseModel, field_validator


def validate_date_format(date_str: str) -> str:
    if date_str is not None:
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            raise ValueError('Formato de data inválido, utilize YYYY-MM-DD')


class CaracteristicaFisicaCreateSchema(BaseModel):
    caracteristica: str
    estatura: float
    envergadura: float
    peso: float
    percentual_gordura: float
    atleta_id: int
    data_avaliacao: str

    _validate_data_inicio = field_validator('data_avaliacao')(
        validate_date_format
    )


class CaracteristicaZagueiroCreateSchema(BaseModel):
    caracteristica: str
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
    atleta_id: int
    data_avaliacao: str

    _validate_data_inicio = field_validator('data_avaliacao')(
        validate_date_format
    )


class CaracteristicaLateralCreateSchema(BaseModel):
    caracteristica: str
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
    atleta_id: int
    data_avaliacao: str

    _validate_data_inicio = field_validator('data_avaliacao')(
        validate_date_format
    )

class CaracteristicaGoleiroCreateSchema(BaseModel):
    caracteristica: str
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
    atleta_id: int
    data_avaliacao: str

    _validate_data_inicio = field_validator('data_avaliacao')(
        validate_date_format
    )

class CaracteristicaVolanteCreateSchema(BaseModel):
    caracteristica: str
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
    atleta_id: int
    data_avaliacao: str

    _validate_data_inicio = field_validator('data_avaliacao')(
        validate_date_format
    )

class CaracteristicaAtacanteCreateSchema(BaseModel):
    caracteristica: str
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
    atleta_id: int
    data_avaliacao: str

    _validate_data_inicio = field_validator('data_avaliacao')(
        validate_date_format
    )

class CaracteristicaMeiaCreateSchema(BaseModel):
    caracteristica: str
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
    atleta_id: int
    data_avaliacao: str

    _validate_data_inicio = field_validator('data_avaliacao')(
        validate_date_format
    )

class CaracteristicaCreateResponse(BaseModel):
    id: int
