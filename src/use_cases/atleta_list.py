from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo


class AtletaListUseCase:
    def __init__(self, atleta_repository: AtletaRepo):
        self.atleta_repository = atleta_repository

    def execute(self, http_request: HttpRequest):
        filters: dict = dict(http_request.query_params.items())

        result = self._list_atletas(filters)
        return self._format_response(result)

    def _list_atletas(self, filters):
        return self.atleta_repository.list_atleta(filters)

    def _format_response(self, result: list[dict]) -> dict:
        return {
            "count": len(result),
            "type": "Atleta",
            "data": result,
        }
