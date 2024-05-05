from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo


class AtletaCreateUseCase:
    def __init__(self, atleta_repository: AtletaRepo):
        self.atleta_repository = atleta_repository

    def execute(self, http_request: HttpRequest):
        atleta_data: dict = http_request.json
        result = self._create_atleta(atleta_data)

        return result

    def _create_atleta(self, atleta_data: dict) -> dict:
        return self.atleta_repository.create_atleta(atleta_data)
