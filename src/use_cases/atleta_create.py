from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo


class AtletaCreateUseCase:
    def __init__(self, repository: AtletaRepo):
        self.repository = repository

    def execute(self, http_request: HttpRequest):
        atleta_data: dict = http_request.json
        result = self._create_atleta(atleta_data)

        return result

    def _create_atleta(self, atleta_data: dict) -> dict:
        return self.repository.create_atleta(atleta_data)
