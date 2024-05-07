from sqlalchemy.orm.exc import NoResultFound
from sqlmodel import select

from .base_repo import create_session
from .model_objects import Usuario


class UsuarioRepo:
    def __init__(self) -> None:
        self.session_factory = create_session

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
