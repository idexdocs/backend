from sqlmodel import select

from src.schemas import AtletaList

from .base_repo import create_session
from .model_objects import Atleta, AtletaClube, AtletaPosicao, Clube, Posicao


class AtletaRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_objects(self, result: list) -> AtletaList:
        atleta_list = [
            {
                "nome": nome,
                "data_nascimento": data_nascimento.strftime("%Y-%m-%d"),
                "posicao": posicao,
                "clube_atual": clube,
            }
            for nome, data_nascimento, posicao, clube in result
        ]
        return AtletaList(atletas=atleta_list).model_dump()["atletas"]

    def list_atleta(self, filters: None):
        with self.session_factory() as session:
            query = (
                select(
                    Atleta.nome.label("nome"),
                    Atleta.data_nascimento.label("data_nascimento"),
                    Posicao.nome.label("posicao"),
                    Clube.nome.label("clube"),
                )
                .select_from(Atleta)
                .join(AtletaPosicao)
                .join(Posicao)
                .join(AtletaClube)
                .join(Clube)
            )

            if filters is not None:
                if page := int(filters.get("page", 1)):
                    query = (
                        query.order_by(Atleta.nome)
                        .limit(15)
                        .offset((page - 1) * 15)
                    )

                if atleta := filters.get("atleta"):
                    query = query.filter(Atleta.nome == atleta)

                if posicao := filters.get("posicao"):
                    query = query.filter(Posicao.nome == posicao)

                if clube := filters.get("clube"):
                    query = query.filter(Clube.nome == clube)

            return self._create_objects(session.exec(query).all())
