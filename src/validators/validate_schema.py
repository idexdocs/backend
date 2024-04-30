from fastapi import Request
from pydantic import BaseModel


async def validate_schema(request: Request, schema: BaseModel = None):
    if request.method == 'POST' and schema is not None:
        request_body = await request.json()
        schema.model_validate(request_body)
