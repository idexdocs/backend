from sqlmodel import select

from src.repository.model_objects import HistoricoClube

from .base_repo import create_session


class ClubeRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_clube_objects(self, result: list) -> list[dict]:
        clube_list = [
            {
                'nome': nome,
                'data_inicio': data_inicio.strftime('%Y-%m-%d'),
                'data_fim': data_fim.strftime('%Y-%m-%d')
                if data_fim is not None
                else None,
            }
            for nome, data_inicio, data_fim in result
        ]

        return clube_list

    def list_clube(self, atleta_id: int, filters: dict = None):
        with self.session_factory() as session:
            query = select(
                HistoricoClube.nome,
                HistoricoClube.data_inicio,
                HistoricoClube.data_fim,
            ).where(HistoricoClube.atleta_id == atleta_id)

            return self._create_clube_objects(session.exec(query).all())

    def create_clube(self, clube_data: int) -> dict:
        with self.session_factory() as session:
            new_clube = HistoricoClube(**clube_data)
            session.add(new_clube)
            session.commit()
            session.refresh(new_clube)
            return {'id': new_clube.id}
