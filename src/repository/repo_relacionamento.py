from sqlmodel import select

from src.schemas import RelacionamentoListSchema

from .base_repo import create_session
from .model_objects import Relacionamento


class RelacionamentoRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_relacionamento_list_objects(
        self, result: list
    ) -> RelacionamentoListSchema:
        relacionamento_list = [
            {
                'atleta_id': atleta_id,
                'receptividade_contrato': receptividade_contrato,
                'satisfacao_empresa': satisfacao_empresa,
                'satisfacao_clube': satisfacao_clube,
                'relacao_familiares': relacao_familiares,
                'influencias_externas': influencias_externas,
                'pendencia_empresa': pendencia_empresa,
                'pendencia_clube': pendencia_clube,
                'data_criacao': data_criacao.strftime('%Y-%m-%d'),
            }
            for atleta_id, receptividade_contrato, satisfacao_empresa, satisfacao_clube, relacao_familiares, influencias_externas, pendencia_empresa, pendencia_clube, data_criacao in result
        ]

        return RelacionamentoListSchema(
            relacionamentos=relacionamento_list
        ).model_dump()['relacionamentos']

    def list_relacionamento(self, atleta_id: int, filters: dict = None):
        with self.session_factory() as session:
            query = (
                select(
                    Relacionamento.atleta_id,
                    Relacionamento.receptividade_contrato,
                    Relacionamento.relacao_familiares,
                    Relacionamento.satisfacao_empresa,
                    Relacionamento.satisfacao_clube,
                    Relacionamento.influencias_externas,
                    Relacionamento.pendencia_clube,
                    Relacionamento.pendencia_empresa,
                    Relacionamento.data_criacao,
                )
                .filter(Relacionamento.atleta_id == atleta_id)
                .order_by('data_criacao')
            )

            return self._create_relacionamento_list_objects(
                session.exec(query).all()
            )
