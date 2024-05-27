
from sqlmodel import select

from .base_repo import create_session
from .model_objects import AtletaImagens


class ArquivoRepo:
    def __init__(self) -> None:
        self.sessio_factory = create_session

    def save_imagens_url(self, imagem_data: dict):
        with self.session_factory() as session:
            atleta_imagem = AtletaImagens(**imagem_data)
            session.add(atleta_imagem)
            session.commit()

    def get_blob_urls(self, atleta_id: int):
        with self.session_factory() as session:
            query = select(AtletaImagens).where(
                AtletaImagens.atleta_id == atleta_id
            )

            return session.exec(query).one()