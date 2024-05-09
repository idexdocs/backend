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
                'nome': nome,
                'email': email,
                'data_criacao': data_criacao.strftime('%Y-%m-%d'),
                'tipo': tipo.value,
            }
            for nome, email, data_criacao, tipo in result
        ]

        return usuario_list

    def create_usuario(self, usuario_data: dict) -> dict:
        with self.session_factory() as session:
            new_usuario = Usuario(**usuario_data)
            session.add(new_usuario)
            session.commit()
            session.refresh(new_usuario)

            return {'id': new_usuario.id}

    def get_usuario_by_email(self, usuario_email: str) -> dict:
        with self.session_factory() as session:
            query = select(Usuario).where(Usuario.email == usuario_email)

        try:
            result = session.exec(query).one()
            return result
        except NoResultFound:
            return None

    def list_usuario(self, filters: dict = {}):
        with self.session_factory() as session:
            query = select(
                Usuario.nome,
                Usuario.email,
                Usuario.data_criacao,
                UsuarioTipo.tipo
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