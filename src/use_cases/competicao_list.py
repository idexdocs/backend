from src.error.types.http_not_found import NotFoundError
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
        competicoes = self.repository.list_competicao(atleta_id)

        if len(competicoes) == 0:
            raise NotFoundError(
                "O Atleta não possui competições cadastradas"
            )
        
        return competicoes

    def _format_response(self, result: list[dict]) -> dict:
        return {
            "count": len(result),
            "type": "Competicao",
            "data": result,
        }
