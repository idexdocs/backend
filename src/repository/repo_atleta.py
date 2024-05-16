from datetime import datetime, timedelta

from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlmodel import func, select

from .base_repo import create_session
from .model_objects import (
    Atleta,
    AtletaContratoClube,
    AtletaContratoEmpresa,
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
                'posicao_secundaria': segunda.value if segunda else None,
                'posicao_terciaria': terceira.value if terceira else None,
                'clube_atual': clube,
                'data_proxima_avaliacao_relacionamento': (
                    data_avaliacao + timedelta(days=30)
                ).strftime('%Y-%m-%d')
                if data_avaliacao
                else None,
            }
            for id_, nome, data_nascimento, primeira, segunda, terceira, clube, data_avaliacao in result
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
                    Posicao.segunda,
                    Posicao.terceira,
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
                    Contrato.tipo,
                    AtletaContratoClube.data_inicio.label(
                        'data_inicio_contrato_clube'
                    ),
                    AtletaContratoClube.data_fim.label(
                        'data_termino_contrato_clube'
                    ),
                    AtletaContratoEmpresa.data_inicio.label(
                        'data_inicio_contrato_empresa'
                    ),
                    AtletaContratoEmpresa.data_fim.label(
                        'data_temino_contrato_empresa'
                    ),
                    HistoricoClube.nome.label('clube'),
                    UsuarioAvatar.blob_url,
                )
                .select_from(Atleta)
                .outerjoin(
                    AtletaContratoClube,
                    Atleta.id == AtletaContratoClube.atleta_id,
                )
                .outerjoin(
                    Contrato, AtletaContratoClube.contrato_id == Contrato.id
                )
                .outerjoin(Posicao, Atleta.id == Posicao.atleta_id)
                .outerjoin(
                    HistoricoClube, HistoricoClube.atleta_id == atleta_id
                )
                .outerjoin(
                    AtletaContratoEmpresa,
                    AtletaContratoEmpresa.atleta_id == atleta_id,
                )
                .outerjoin(UsuarioAvatar, UsuarioAvatar.atleta_id == atleta_id)
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
            try:
                # Criando uma instância de atleta
                new_atleta = Atleta(**atleta_data)

                # Criando atleta para recuperar o ID e usar de FK posteriormente
                session.add(new_atleta)
                session.commit()
                session.refresh(new_atleta)

                # Criando clube
                new_clube = HistoricoClube(
                    nome=atleta_data.get('clube').get('nome'),
                    atleta_id=new_atleta.id,
                    data_inicio=atleta_data.get('clube').get('data_inicio'),
                )
                session.add(new_clube)

                # Criando relacionamento N:N Atleta contrato clube
                contrato_clube = atleta_data.get('contrato_clube')
                new_atleta_contrato_clube = AtletaContratoClube(
                    atleta_id=new_atleta.id,
                    contrato_id=contrato_clube.get('tipo_id'),
                    data_inicio=datetime.strptime(
                        contrato_clube.get('data_inicio'),
                        '%Y-%m-%d',
                    ),
                    data_fim=datetime.strptime(
                        contrato_clube.get('data_fim'), '%Y-%m-%d'
                    ),
                )
                session.add(new_atleta_contrato_clube)

                # Criando relacionamento 1:1 Atleta contrato empresa
                contrato_empresa = atleta_data.get('contrato_empresa')
                new_atleta_contrato_empresa = AtletaContratoEmpresa(
                    data_inicio=contrato_empresa.get('data_inicio'),
                    data_fim=contrato_empresa.get('data_fim'),
                    atleta_id=new_atleta.id,
                )
                session.add(new_atleta_contrato_empresa)

                # Criando relacionameno N:N Atleta Posição
                new_atleta_posicao = Posicao(
                    atleta_id=new_atleta.id,
                    primeira=atleta_data.get('posicao_primaria'),
                    segunda=atleta_data.get('posicao_secundaria'),
                    terceira=atleta_data.get('posicao_terciaria'),
                )
                session.add(new_atleta_posicao)

                session.commit()

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

            if 'contrato' in atleta_data:
                contrato_data = atleta_data.get('contrato')
                atleta_contrato = AtletaContratoClube(
                    atleta_id=atleta_id,
                    contrato_id=contrato_data['tipo_id'],
                    data_inicio=contrato_data['data_inicio'],
                    data_fim=contrato_data['data_fim'],
                )
                session.add(atleta_contrato)

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
