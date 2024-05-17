from datetime import datetime, timedelta

from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlmodel import func, select

from .base_repo import create_session
from .model_objects import (
    Atleta,
    Contrato,
    HistoricoClube,
    Posicao,
    Relacionamento,
    UsuarioAvatar,
)


class AtletaRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_atleta_list_objects(self, result: list) -> dict:
        return [
            {
                'id': id_,
                'nome': nome,
                'data_nascimento': data_nascimento.strftime('%Y-%m-%d'),
                'posicao_primaria': primeira.value if primeira else None,
                'clube_atual': clube,
                'data_proxima_avaliacao_relacionamento': (
                    data_avaliacao + timedelta(days=30)
                ).strftime('%Y-%m-%d')
                if data_avaliacao
                else None,
            }
            for id_, nome, data_nascimento, primeira, clube, data_avaliacao in result
        ]

    def _create_atleta_detail_object(self, result) -> dict:
        (
            nome,
            data_nascimento,
            primeira,
            segunda,
            terceira,
            tipo,
            data_inicio_contrato_clube,
            data_termino_contrato_clube,
            data_inicio_contrato_empresa,
            data_temino_contrato_empresa,
            clube,
            blob_url,
        ) = result

        return {
            'nome': nome,
            'data_nascimento': data_nascimento.strftime('%Y-%m-%d'),
            'posicao_primaria': primeira.value if primeira else None,
            'posicao_secundaria': segunda.value if segunda else None,
            'posicao_terciaria': terceira.value if terceira else None,
            'clube_atual': clube,
            'contrato_clube': {
                'tipo': tipo,
                'data_inicio': data_inicio_contrato_clube.strftime('%Y-%m-%d')
                if data_inicio_contrato_clube is not None
                else None,
                'data_termino': data_termino_contrato_clube.strftime(
                    '%Y-%m-%d'
                )
                if data_termino_contrato_clube is not None
                else None,
                'data_expiracao': (
                    data_termino_contrato_clube - timedelta(days=180)
                ).strftime('%Y-%m-%d')
                if data_termino_contrato_clube
                else None,
            },
            'contrato_empresa': {
                'data_inicio': data_inicio_contrato_empresa.strftime(
                    '%Y-%m-%d'
                )
                if data_inicio_contrato_empresa is not None
                else None,
                'data_termino': data_temino_contrato_empresa.strftime(
                    '%Y-%m-%d'
                )
                if data_temino_contrato_empresa is not None
                else None,
                'data_expiracao': (
                    data_temino_contrato_empresa - timedelta(days=180)
                ).strftime('%Y-%m-%d')
                if data_temino_contrato_empresa
                else None,
            },
            'blob_url': blob_url,
        }

    def list_atleta(self, filters: dict):
        with self.session_factory() as session:
            subquery = (
                select(
                    Relacionamento.atleta_id,
                    func.max(Relacionamento.data_avaliacao).label(
                        'max_data_avaliacao'
                    ),
                )
                .group_by(Relacionamento.atleta_id)
                .subquery()
            )

            query = (
                select(
                    Atleta.id.label('id_'),
                    Atleta.nome.label('nome'),
                    Atleta.data_nascimento.label('data_nascimento'),
                    Posicao.primeira,
                    HistoricoClube.nome.label('clube'),
                    Relacionamento.data_avaliacao,
                )
                .select_from(Atleta)
                .outerjoin(Posicao, Posicao.atleta_id == Atleta.id)
                .outerjoin(
                    HistoricoClube, Atleta.id == HistoricoClube.atleta_id
                )
                .outerjoin(subquery, subquery.c.atleta_id == Atleta.id)
                .outerjoin(
                    Relacionamento,
                    (
                        (Relacionamento.atleta_id == subquery.c.atleta_id)
                        & (
                            Relacionamento.data_avaliacao
                            == subquery.c.max_data_avaliacao
                        )
                    ),
                )
                .where(HistoricoClube.data_fim.is_(None))
                .order_by(Atleta.id)
            )

            if atleta := filters.get('atleta'):
                query = query.filter(Atleta.nome == atleta)

            if posicao := filters.get('posicao'):
                query = query.filter(Posicao.primeira == posicao)

            if clube := filters.get('clube'):
                query = query.filter(HistoricoClube.nome == clube)

            # conta o número total de items sem paginação
            total_count = session.exec(
                select(func.count()).select_from(query.subquery())
            ).one()

            # aplica paginação
            page = int(filters.get('page', 1))
            per_page = int(filters.get('per_page', 10))
            query = (
                query.order_by(Atleta.nome)
                .limit(per_page)
                .offset((page - 1) * per_page)
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
                    Posicao.primeira,
                    Posicao.segunda,
                    Posicao.terceira,
                    HistoricoClube.nome.label('clube'),
                    UsuarioAvatar.blob_url,
                )
                .select_from(Atleta)
                .outerjoin(Posicao, Atleta.id == Posicao.atleta_id)
                .outerjoin(HistoricoClube, HistoricoClube.atleta_id == atleta_id)
                .outerjoin(UsuarioAvatar, UsuarioAvatar.atleta_id == atleta_id)
                .where(Atleta.id == atleta_id, HistoricoClube.data_fim.is_(None)
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
            try:
                # Criando uma instância de atleta
                new_atleta = Atleta(**atleta_data)

                session.add(new_atleta)
                session.commit()
                session.refresh(new_atleta)

                return {'id': new_atleta.id}
            except Exception:
                session.rollback()
                raise

    def update_atleta(self, atleta_id: int, atleta_data: dict) -> dict:
        with self.session_factory() as session:
            atleta: Atleta = session.exec(
                select(Atleta).where(Atleta.id == atleta_id)
            ).one()

            # Configurando horário da atualização
            data_atualizacao = datetime.strftime(
                datetime.now(), '%Y-%m-%d %H:%M:%S'
            )

            # Preparando os campos de atleta para atualização
            atleta_update_fields = {
                'nome': atleta_data.get('nome', atleta.nome),
                'data_nascimento': atleta_data.get(
                    'data_nascimento', atleta.data_nascimento
                ),
                'ativo': atleta_data.get('ativo', atleta.ativo),
                'data_atualizado': data_atualizacao,
            }

            # Apenas inclue campos que são novos para atualizar
            updated_fields = {
                k: v
                for k, v in atleta_update_fields.items()
                if getattr(atleta, k) != v
            }

            # Faz a atualização se existirem valores novos para atualizar
            if updated_fields:
                for key, value in updated_fields.items():
                    setattr(atleta, key, value)

            # Faz a atualização de posições se existirem valores novos para atualizar
            posicao = session.exec(
                select(Posicao).where(Posicao.atleta_id == atleta_id)
            ).one()
            posicao.primeira = atleta_data['posicao_primaria']
            posicao.segunda = atleta_data['posicao_secundaria']
            posicao.terceira = atleta_data['posicao_terciaria']
            posicao.data_atualizado = data_atualizacao

            session.commit()

    def save_blob_url(self, atleta_id: int, blob_url: str):
        with self.session_factory() as session:
            new_user_avatar = UsuarioAvatar(
                blob_url=blob_url, atleta_id=atleta_id
            )
            session.add(new_user_avatar)
            session.commit()

    def get_blob_url(self, atleta_id: int):
        with self.session_factory() as session:
            query = select(UsuarioAvatar).where(
                UsuarioAvatar.atleta_id == atleta_id
            )

        try:
            result = session.exec(query).one()
            return result.blob_url
        except NoResultFound:
            return None
