from sqlmodel import select

from .base_repo import create_session
from .model_objects import HistoricoControle


class ControleRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_controle_list_objects(self, result: list) -> dict:
        return [
            {
                'atleta_id': atleta_id,
                'nome': nome,
                'quantidade': quantidade,
                'preco': preco,
                'data_controle': data_controle.strftime('%Y-%m-%d'),
            }
            for atleta_id, nome, quantidade, preco, data_controle in result
        ]

    def list_controle(self, atleta_id: int, filters: dict = None):
        with self.session_factory() as session:
            query = (
                select(
                    HistoricoControle.id,
                    HistoricoControle.nome,
                    HistoricoControle.quantidade,
                    HistoricoControle.preco,
                    HistoricoControle.data_controle,
                )
                .filter(HistoricoControle.atleta_id == atleta_id)
                .order_by('data_criacao')
            )

            return self._create_controle_list_objects(
                session.exec(query).all()
            )

    def create_controle(self, controle_data: dict) -> dict:
        with self.session_factory() as session:
            new_controle = HistoricoControle(**controle_data)
            session.add(new_controle)
            session.commit()
            session.refresh(new_controle)
            return {'id': new_controle.id}
