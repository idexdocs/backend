from pydantic import BaseModel


class Atleta(BaseModel):
    nome: str
    posicao: str
    data_nascimento: str
    clube_atual: str


class AtletaList(BaseModel):
    atletas: list[Atleta]
