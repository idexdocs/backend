from fastapi import Request
from pydantic import BaseModel

from src.schemas.caracteristica import *

CARACTERISTICAS_SCHEMA = {
    'fisico': CaracteristicaFisicaCreateSchema,
    'zagueiro': CaracteristicaZagueiroCreateSchema,
    'lateral': CaracteristicaLateralCreateSchema,
    'goleiro': CaracteristicaGoleiroCreateSchema,
    'volante': CaracteristicaVolanteCreateSchema,
    'atacante': CaracteristicaAtacanteCreateSchema,
    'meia': CaracteristicaMeiaCreateSchema,
}


async def validate_schema(request: Request, schema: BaseModel = None):
    if request.method == 'POST' and schema is not None:
        request_body = await request.json()
        schema.model_validate(request_body)

    if (
        request.method == 'POST'
        and '/create/caracteristica' == request.url.path
    ):
        request_body = await request.json()
        caracteristica_tipo = request_body.get('caracteristica')

        if caracteristica_tipo not in CARACTERISTICAS_SCHEMA:
            raise ValueError(
                f'Característica não é válida: {caracteristica_tipo}'
            )

        schema = CARACTERISTICAS_SCHEMA.get(caracteristica_tipo)
        schema.model_validate(request_body)
