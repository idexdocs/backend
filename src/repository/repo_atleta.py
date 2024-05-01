from datetime import datetime

from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlmodel import func, select

from .base_repo import create_session
from .model_objects import (
    Atleta,
    AtletaContrato,
    AtletaPosicao,
    Contrato,
    HistoricoClube,
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
            tipo,
            data_inicio,
            data_termino,
            clube,
        ) = result

        return {
            'nome': nome,
            'data_nascimento': data_nascimento.strftime('%Y-%m-%d'),
            'posicao': posicao,
            'clube_atual': clube,
            'contrato': {
                'tipo': tipo,
                'data_inicio': data_inicio.strftime('%Y-%m-%d')
                if data_inicio is not None
                else None,
                'data_termino': data_termino.strftime('%Y-%m-%d')
                if data_inicio is not None
                else None,
            },
        }

    def list_atleta(self, filters: dict):
        with self.session_factory() as session:
            query = (
                select(
                    Atleta.nome.label('nome'),
                    Atleta.data_nascimento.label('data_nascimento'),
                    Posicao.nome.label('posicao'),
                    HistoricoClube.nome.label('clube'),
                )
                .select_from(Atleta)
                .join(AtletaPosicao, isouter=True)
                .join(Posicao, isouter=True)
                .join(HistoricoClube, isouter=True)
            )

            if atleta := filters.get('atleta'):
                query = query.filter(Atleta.nome == atleta)

            if posicao := filters.get('posicao'):
                query = query.filter(Posicao.nome == posicao)

            if clube := filters.get('clube'):
                query = query.filter(HistoricoClube.nome == clube)

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
            return result
        except NoResultFound:
            return None

    def get_atleta(self, atleta_id: int):
        with self.session_factory() as session:
            query = (
                select(
                    Atleta.nome,
                    Atleta.data_nascimento,
                    Posicao.nome.label('posicao'),
                    Contrato.tipo,
                    AtletaContrato.data_inicio,
                    AtletaContrato.data_fim,
                    HistoricoClube.nome.label('clube'),
                )
                .select_from(Atleta)
                .outerjoin(
                    AtletaContrato, Atleta.id == AtletaContrato.atleta_id
                )
                .outerjoin(Contrato, AtletaContrato.contrato_id == Contrato.id)
                .outerjoin(AtletaPosicao, Atleta.id == AtletaPosicao.atleta_id)
                .outerjoin(Posicao, Atleta.id == Posicao.id)
                .outerjoin(
                    HistoricoClube, HistoricoClube.atleta_id == atleta_id
                )
                .where(
                    Atleta.id == atleta_id, HistoricoClube.data_fim.is_(None)
                )
            )

        try:
            result = session.exec(query).one()
            return self._create_atleta_detail_object(result)
        except NoResultFound:
            return None
        except MultipleResultsFound:
            raise

    def create_atleta(self, atleta_data: dict) -> dict:
        with self.session_factory() as session:
            # Criando uma instância de atleta
            new_atleta = Atleta(**atleta_data)

            try:

                # Criando atleta
                session.add(new_atleta)
                session.commit()
                session.refresh(new_atleta)

                # Criando clube
                new_clube = HistoricoClube(
                    nome=atleta_data.get('clube'), atleta_id=new_atleta.id
                )
                session.add(new_clube)

                # Criando relacionamento N:N Atleta contrato
                new_atleta_contrato = AtletaContrato(
                    atleta_id=new_atleta.id,
                    contrato_id=atleta_data.get('contrato').get('tipo_id'),
                    data_inicio=datetime.strptime(
                        atleta_data.get('contrato').get('data_inicio'),
                        '%Y-%m-%d',
                    ),
                    data_fim=datetime.strptime(
                        atleta_data.get('contrato').get('data_fim'), '%Y-%m-%d'
                    ),
                )
                session.add(new_atleta_contrato)

                # Criando relacionameno N:N Atleta Posição
                new_atleta_posicao = AtletaPosicao(
                    atleta_id=new_atleta.id,
                    posicao_id=atleta_data.get('posicao_id'),
                )
                session.add(new_atleta_posicao)

                session.commit()

                atleta_data.update({'id': new_atleta.id})

                return atleta_data
            except Exception:
                session.rollback()
                raise
