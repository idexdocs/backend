from pydantic import BaseModel


class Atleta(BaseModel):
    nome: str
    posicao: str | None
    data_nascimento: str
    clube_atual: str | None


class AtletaList(BaseModel):
    atletas: list[Atleta]


class ContratoSchema(BaseModel):
    tipo: str
    inicio: str
    termino: str


class AtletaDetail(Atleta):
    contrato: ContratoSchema
