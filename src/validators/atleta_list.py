from datetime import date

from fastapi import Request
from pydantic import BaseModel


class AtletaListSchema(BaseModel):
    nome: str
    posicao: str
    data_nascimento: date
    clube_atual: str


async def regra_validate_schema(request: Request):
    request_body = await request.body()
    # AtletaListSchema.model_validate(request_body)
    # TODO
