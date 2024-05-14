from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound
from sqlmodel import func, select

from .base_repo import create_session
from .model_objects import Usuario, UsuarioTipo


class UsuarioRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

    def _create_usuario_objects(self, result: list) -> list[dict]:
        usuario_list = [
            {
                'id': id_,
                'nome': nome,
                'email': email,
                'data_criacao': data_criacao.strftime('%Y-%m-%d'),
                'tipo': tipo.value,
            }
            for id_, nome, email, data_criacao, tipo in result
        ]

        return usuario_list

    def _create_usuario_token_objects(self, usuario: Usuario) -> list[dict]:
        usuario = {
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'data_criacao': usuario.data_criacao.strftime('%Y-%m-%d'),
            'hash_password': usuario.hash_password,
            'tipo': usuario.tipo.value,
        }

        return usuario

    def create_usuario(self, usuario_data: dict) -> dict:
        with self.session_factory() as session:
            new_usuario = Usuario(**usuario_data)
            session.add(new_usuario)
            session.commit()
            session.refresh(new_usuario)

            return {'id': new_usuario.id}

    def get_usuario_by_email(self, usuario_email: str) -> dict:
        with self.session_factory() as session:
            query = (
                select(
                    Usuario.id,
                    Usuario.nome,
                    Usuario.email,
                    Usuario.data_criacao,
                    Usuario.hash_password,
                    UsuarioTipo.tipo,
                )
                .join(UsuarioTipo)
                .where(Usuario.email == usuario_email)
            )

        try:
            result = session.exec(query).one()
            return self._create_usuario_token_objects(result)
        except NoResultFound:
            return None

    def get_usuario_by_id(self, usuario_id: int) -> dict:
        with self.session_factory() as session:
            query = (
                select(
                    Usuario.id,
                    Usuario.nome,
                    Usuario.email,
                    Usuario.data_criacao,
                    Usuario.hash_password,
                    UsuarioTipo.tipo,
                )
                .join(UsuarioTipo)
                .where(Usuario.id == usuario_id)
            )

        try:
            result = session.exec(query).one()
            return self._create_usuario_token_objects(result)
        except NoResultFound:
            return None

    def list_usuario(self, filters: dict = {}):
        with self.session_factory() as session:
            query = select(
                Usuario.id,
                Usuario.nome,
                Usuario.email,
                Usuario.data_criacao,
                UsuarioTipo.tipo,
            ).join(UsuarioTipo)

            # conta o Usuarionúmero total de items sem paginação
            total_count = session.exec(
                select(func.count()).select_from(query.subquery())
            ).one()

            # aplica paginação
            page = int(filters.get('page', 1))
            per_page = int(filters.get('per_page', 10))
            query = (
                query.order_by(Usuario.nome)
                .limit(per_page)
                .offset((page - 1) * per_page)
            )

            # executa query com paginação
            paginated_results = session.exec(query).all()

            return total_count, self._create_usuario_objects(paginated_results)

    def update_usuario(self, usuario_id: int, usuario_data: dict) -> dict:
        with self.session_factory() as session:
            usuario: Usuario = session.exec(
                select(Usuario).where(Usuario.id == usuario_id)
            ).one()

            for key, value in usuario_data.items():
                if value is not None:
                    setattr(usuario, key, value)

            usuario.data_atualizado = datetime.strftime(
                datetime.now(), '%Y-%m-%d %H:%M:%S'
            )
            session.commit()
            session.refresh(usuario)

            return usuario.model_dump(exclude=['data_criacao', 'data_atualizado', 'hash_password'])
        

    def update_usurio_password(self, usuario_id: int, new_password: str):
        with self.session_factory() as session:
            try:
                usuario: Usuario = session.exec(
                    select(Usuario).where(Usuario.id == usuario_id)
                ).one()

                import sys
                from pprint import pprint
                print('*'*10,__name__,': line',sys._getframe().f_lineno,'*'*10, flush=True)
                pprint(usuario)
                pprint(new_password)

                usuario.hash_password = new_password
                session.commit()
                return {'status': True, 'message': 'Senha alterada com sucesso'}
            except Exception:
                session.rollback()
                return {'status': False, 'message': 'Operação não realizada'}



