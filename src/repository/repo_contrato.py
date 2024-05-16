from sqlmodel import func, select

from src.repository.model_objects import (
    Contrato,
    ContratoSubTipo,
    ContratoTipo,
)

from .base_repo import create_session


class ContratoRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_contrato_objects(self, result: list) -> list[dict]:
        lesao_list = [
            {
                'contrato_tipo': tipo,
                'contrato_nome': nome,
                'data_inicio': data_inicio.strftime('%Y-%m-%d'),
                'data_termino': data_termino.strftime('%Y-%m-%d'),
                'observacao': observacao,
                'ativo': ativo,
            }
            for tipo, nome, data_inicio, data_termino, observacao, ativo in result
        ]

        return lesao_list

    def list_contrato(self, atleta_id: int, filters: dict):
        with self.session_factory() as session:
            query = (
                select(
                    ContratoTipo.tipo,
                    ContratoSubTipo.nome,
                    Contrato.data_inicio,
                    Contrato.data_termino,
                    Contrato.observacao,
                    Contrato.ativo,
                )
                .select_from(Contrato)
                .join(
                    ContratoSubTipo,
                    Contrato.contrato_sub_tipo_id == ContratoSubTipo.id,
                )
                .join(
                    ContratoTipo,
                    ContratoSubTipo.contrato_tipo_id == ContratoTipo.id,
                )
                .where(Contrato.atleta_id == atleta_id)
            )

            # conta o número total de items sem paginação
            total_count = session.exec(
                select(func.count()).select_from(query.subquery())
            ).one()

            # aplica paginação
            page = int(filters.get('page', 1))
            per_page = int(filters.get('per_page', 10))
            query = (
                query.order_by(Contrato.data_termino)
                .limit(per_page)
                .offset((page - 1) * per_page)
            )

            # executa query com paginação
            paginated_results = session.exec(query).all()

        return total_count, self._create_contrato_objects(paginated_results)
