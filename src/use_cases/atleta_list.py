from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo


class AtletaListUseCase:
    def __init__(self, repository: AtletaRepo):
        self.repository = repository

    def execute(self, http_request: HttpRequest):
        filters: dict = dict(http_request.query_params.items())

        total_count, result = self._list_atletas(filters)
        return self._format_response(total_count, result)

    def _list_atletas(self, filters):
        return self.repository.list_atleta(filters)

    def _format_response(self, total_count: int, result: list[dict]) -> dict:
        return {
            'count': len(result),
            'total': total_count,
            'type': 'Atleta',
            'data': result,
        }
