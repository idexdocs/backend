from sqlmodel import func, select

from .base_repo import create_session
from .model_objects import HistoricoObservacao


class ObservacaoRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_observacao_list_objects(self, result: list) -> dict:
        return [
            {
                'atleta_id': atleta_id,
                'tipo': tipo.value,
                'descricao': descricao,
                'data_observacao': data_observacao.strftime('%Y-%m-%d'),
            }
            for atleta_id, tipo, descricao, data_observacao in result
        ]

    def list_observacao(self, atleta_id: int, filters: dict = None):
        with self.session_factory() as session:
            query = select(
                HistoricoObservacao.id,
                HistoricoObservacao.tipo,
                HistoricoObservacao.descricao,
                HistoricoObservacao.data_criacao,
            ).filter(HistoricoObservacao.atleta_id == atleta_id)

            if tipo := filters.get('tipo'):
                query = query.filter(HistoricoObservacao.tipo == tipo)

            # conta o número total de items sem paginação
            total_count = session.exec(
                select(func.count()).select_from(query.subquery())
            ).one()

            # aplica paginação
            page = int(filters.get('page', 1))
            per_page = int(filters.get('per_page', 10))
            query = (
                query.order_by(HistoricoObservacao.data_criacao)
                .limit(per_page)
                .offset((page - 1) * per_page)
            )

            # executa query com paginação
            paginated_results = session.exec(query).all()

            return total_count, self._create_observacao_list_objects(
                paginated_results
            )

    def create_observacao(self, observacao_data: dict) -> dict:
        with self.session_factory() as session:
            new_observacao = HistoricoObservacao(**observacao_data)
            session.add(new_observacao)
            session.commit()
            session.refresh(new_observacao)
            return {'id': new_observacao.id}
