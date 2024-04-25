from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_competicao import CompeticaoRepo


class CompeticaoListUseCase:
    def __init__(self, repository: CompeticaoRepo):
        self.repository = repository

    def execute(self, http_request: HttpRequest):
        atleta_id: int = int(http_request.path_params.get("id"))

        result = self._list_competicao(atleta_id)
        return self._format_response(result)

    def _list_competicao(self, atleta_id: int):
        return self.repository.list_competicao(atleta_id)

    def _format_response(self, result: list[dict]) -> dict:
        return {
            "count": len(result),
            "type": "Competicao",
            "data": result,
        }
