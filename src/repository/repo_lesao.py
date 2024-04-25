from sqlmodel import select

from src.repository.model_objects import HistoricoLesao

from .base_repo import create_session


class LesaoRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_lesao_objects(self, result: list) -> list[dict]:
        lesao_list = [
            {
                "data_lesao": data_lesao.strftime("%Y-%m-%d"),
                "descricao": descricao,
            }
            for data_lesao, descricao in result
        ]

        return lesao_list

    def list_lesao(self, atleta_id: int):
        with self.session_factory() as session:
            query = select(
                HistoricoLesao.data_lesao, HistoricoLesao.descricao
            ).where(HistoricoLesao.atleta_id == atleta_id)

            return self._create_lesao_objects(session.exec(query).all())
