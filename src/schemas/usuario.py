from pydantic import BaseModel, EmailStr, Field


class UsuarioCreateSchema(BaseModel):
    nome: str
    email: EmailStr
    password: str
    usuario_tipo_id: int = Field(..., ge=1, le=3)


class UsuarioCreateResponse(BaseModel):
    id: int
