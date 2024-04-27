from fastapi import Request
from pydantic import BaseModel


async def validate_schema(request: Request, schema: BaseModel):
    request_body = await request.json()
    schema.model_validate(request_body)
