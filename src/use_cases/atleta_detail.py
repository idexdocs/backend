from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo


class AtletaDetailUseCase:
    def __init__(self, atleta_repository: AtletaRepo):
        self.atleta_repository = atleta_repository

    def execute(self, http_request: HttpRequest):
        atleta_id: int = http_request.path_params.get("id")
        result = self._get_atleta(atleta_id)
        
        return self._format_response(result)

    def _get_atleta(self, atleta_id: int) -> dict:
        atleta = self.atleta_repository.get_atleta(atleta_id)

        if atleta is not None:
            return atleta

        raise NotFoundError("Atleta não encontrado")

    def _format_response(self, result: dict) -> dict:
        return {
            "count": 1,
            "type": "Atleta",
            "data": result,
        }
