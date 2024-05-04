from datetime import datetime

from pydantic import BaseModel, field_validator


def validate_date_format(date_str: str) -> str:
    if date_str is not None:
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            raise ValueError('Formato de data inválido, utilize YYYY-MM-DD')


class Clube(BaseModel):
    nome: str
    data_inicio: str

    _validate_data_inicio = field_validator('data_inicio')(
        validate_date_format
    )


class Contrato(BaseModel):
    tipo_id: int
    data_inicio: str
    data_fim: str

    _validate_data_inicio = field_validator('data_inicio')(
        validate_date_format
    )
    _validate_data_fim = field_validator('data_fim')(validate_date_format)


class AtletaCreateSchema(BaseModel):
    nome: str
    data_nascimento: str
    clube: Clube
    contrato: Contrato
    posicao_id: int
    image: bytes | None

    _validate_data_nascimento = field_validator('data_nascimento')(
        validate_date_format
    )


class AtletaCreateResponse(BaseModel):
    id: int
