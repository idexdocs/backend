from pydantic import BaseModel


class RelacionamentoCreateSchema(BaseModel):
    atleta_id: int
    receptividade_contrato: int
    satisfacao_empresa: int
    satisfacao_clube: int
    relacao_familiares: int
    influencias_externas: int
    pendencia_empresa: bool
    pendencia_clube: bool
