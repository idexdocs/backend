from src.error.types.http_bad_request import BadRequestError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.model_objects import Usuario
from src.repository.repo_usuario import UsuarioRepo
from src.security import create_access_token, verify_password


class TokenCreateUseCase:
    def __init__(self, usuario_repository: UsuarioRepo) -> None:
        self.usuario_repository = usuario_repository

    def execute(self, http_request: HttpRequest):
        token_data: dict = http_request.json

        usuario: Usuario = self._check_usuario_exists(token_data.get('email'))

        self._verify_password(
            token_data.get('password'), usuario.hash_password
        )

        token = self._create_access_token(usuario)

        return {'access_token': token, 'token_type': 'bearer'}

    def _check_usuario_exists(self, usuario_email: str):
        usuario = self.usuario_repository.get_usuario_by_email(usuario_email)

        if usuario is None:
            raise BadRequestError('Email ou senha incorretos')

        return usuario

    def _verify_password(self, usuario_password: str, hashed_password: str):
        result = verify_password(usuario_password, hashed_password)

        if not result:
            raise BadRequestError('Email ou senha incorretos')

    def _create_access_token(self, usuario: Usuario):
        return create_access_token(
            data={
                'sub': usuario.model_dump(
                    exclude=['data_criacao', 'data_alterado']
                )
            }
        )
