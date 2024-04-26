from sqlalchemy.orm.exc import NoResultFound
from sqlmodel import func, select

from .base_repo import create_session
from .model_objects import (
    Atleta,
    AtletaClube,
    AtletaContrato,
    AtletaPosicao,
    Clube,
    Contrato,
    Posicao,
)


class AtletaRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_atleta_list_objects(self, result: list) -> dict:
        return [
            {
                'nome': nome,
                'data_nascimento': data_nascimento.strftime('%Y-%m-%d'),
                'posicao': posicao,
                'clube_atual': clube,
            }
            for nome, data_nascimento, posicao, clube in result
        ]

    def _create_atleta_detail_object(self, result) -> dict:
        (
            nome,
            data_nascimento,
            posicao,
            clube,
            tipo,
            data_inicio,
            data_termino,
        ) = result

        return {
            'nome': result,
            'posicao': posicao,
            'data_nascimento': data_nascimento.strftime('%Y-%m-%d'),
            'clube_atual': clube,
            'contrato': {
                'tipo': tipo,
                'data_inicio': data_inicio,
                'data_termino': data_termino,
            },
        }

    def list_atleta(self, filters: dict):
        with self.session_factory() as session:
            query = (
                select(
                    Atleta.nome.label('nome'),
                    Atleta.data_nascimento.label('data_nascimento'),
                    Posicao.nome.label('posicao'),
                    Clube.nome.label('clube'),
                )
                .select_from(Atleta)
                .join(AtletaPosicao, isouter=True)
                .join(Posicao, isouter=True)
                .join(AtletaClube, isouter=True)
                .join(Clube, isouter=True)
            )

            if atleta := filters.get('atleta'):
                query = query.filter(Atleta.nome == atleta)

            if posicao := filters.get('posicao'):
                query = query.filter(Posicao.nome == posicao)

            if clube := filters.get('clube'):
                query = query.filter(Clube.nome == clube)

            # conta o número total de items sem paginação
            total_count = session.exec(
                select(func.count()).select_from(query.subquery())
            ).one()

            # aplica paginação
            if page := int(filters.get('page', 1)):
                query = (
                    query.order_by(Atleta.nome)
                    .limit(15)
                    .offset((page - 1) * 15)
                )

            # executa query com paginação
            paginated_results = session.exec(query).all()

            return total_count, self._create_atleta_list_objects(
                paginated_results
            )

    def get_atleta_by_id(self, atleta_id: int):
        with self.session_factory() as session:
            query = select(Atleta).where(Atleta.id == atleta_id)

        try:
            result = session.exec(query).one()
            # TODO implementar pydantic model do Atleta
            return result
        except NoResultFound:
            return None

    def get_atleta(self, atleta_id: int):
        #  BUG verificar não retorno do atleta ID = 5
        with self.session_factory() as session:
            query = (
                select(
                    Atleta.nome.label('nome'),
                    Atleta.data_nascimento.label('data_nascimento'),
                    Posicao.nome.label('posicao'),
                    Clube.nome.label('clube'),
                    Contrato.tipo,
                    AtletaContrato.data_inicio,
                    AtletaContrato.data_fim,
                )
                .select_from(Atleta)
                .join(AtletaContrato, Atleta.id == AtletaContrato.atleta_id)
                .join(Contrato, AtletaContrato.contrato_id == Contrato.id)
                .join(AtletaClube, Atleta.id == AtletaClube.atleta_id)
                .join(Clube, AtletaClube.clube_id == Clube.id)
                .join(AtletaPosicao, Atleta.id == AtletaPosicao.atleta_id)
                .join(Posicao, Atleta.id == Posicao.id)
                .where(Atleta.id == atleta_id)
            )

        try:
            result = session.exec(query).one()
            return self._create_atleta_detail_object(result)
        except NoResultFound:
            return None
