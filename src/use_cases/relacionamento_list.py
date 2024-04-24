from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_relacionamento import RelacionamentoRepo


class RelacionamentoListUseCase:
    def __init__(self, repository: RelacionamentoRepo):
        self.repository = repository

    def execute(self, http_request: HttpRequest):
        atleta_id: int = int(http_request.path_params.get("id"))
        filters: dict = dict(http_request.query_params.items())

        result = self._list_relacionamentos(atleta_id, filters)
        return self._format_response(result)

    def _list_relacionamentos(self, atleta_id: int, filters: dict):
        return self.repository.list_relacionamento(
            atleta_id, filters
        )

    def _format_response(self, result: list[dict]) -> dict:
        return {
            "count": len(result),
            "type": "Relacionamento",
            "data": result,
        }
