from sqlmodel import select

from src.repository.model_objects import HistoricoCompeticao

from .base_repo import create_session


class CompeticaoRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_competicao_object(self, result: list) -> list[dict]:
        competicao_list = [
            {
                'nome': nome,
                'data_competicao': data_competicao.strftime('%Y-%m-%d'),
                'jogos_completos': jogos_completos,
                'jogos_parciais': jogos_parciais,
                'minutagem': minutagem,
            }
            for nome, data_competicao, jogos_completos, jogos_parciais, minutagem in result
        ]

        return competicao_list

    def list_competicao(self, atleta_id: int):
        with self.session_factory() as session:
            query = select(
                HistoricoCompeticao.nome,
                HistoricoCompeticao.data_competicao,
                HistoricoCompeticao.jogos_completos,
                HistoricoCompeticao.jogos_parciais,
                HistoricoCompeticao.minutagem,
            ).where(HistoricoCompeticao.atleta_id == atleta_id)

            return self._create_competicao_object(session.exec(query).all())

    def create_competicao(self, competicao_data: dict) -> dict:
        with self.session_factory() as session:
            new_competicao = HistoricoCompeticao(**competicao_data)
            session.add(new_competicao)
            session.commit()
            session.refresh(new_competicao)
            return {'id': new_competicao.id}
