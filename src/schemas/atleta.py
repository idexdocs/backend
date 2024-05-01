from pydantic import BaseModel


class AtletaCreateSchema(BaseModel):
    class Contrato(BaseModel):
        tipo_id: int
        data_inicio: str
        data_fim: str

    nome: str
    data_nascimento: str
    clube: str
    contrato: Contrato
    posicao_id: int


class AtletaCreateResponse(BaseModel):
    id: int
