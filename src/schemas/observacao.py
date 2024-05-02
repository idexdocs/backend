from pydantic import BaseModel, Field


class ObservacaoCreateSchema(BaseModel):
    atleta_id: int = Field(..., gt=0)
    tipo: str
    descricao: str


class ObservacaoCreateResponse(BaseModel):
    id: int


class ObservacaoListSchema(BaseModel):
    atleta_id: int
    tipo: str
    descricao: str
    data_observacao: str


class ObservacaoListResponse(BaseModel):
    count: int
    type: str
    data: list[ObservacaoListSchema]
