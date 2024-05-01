from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_clube import ClubeRepo


class ClubeListUseCase:
    def __init__(self, repository: ClubeRepo):
        self.repository = repository

    def execute(self, http_request: HttpRequest):
        atleta_id: int = int(http_request.path_params.get('id'))

        result = self._list_clube(atleta_id)
        return self._format_response(result)

    def _list_clube(self, atleta_id: int):
        clubes = self.repository.list_clube(atleta_id)

        if len(clubes) == 0:
            raise NotFoundError('O Atleta não possui clubes cadastradas')

        return clubes

    def _format_response(self, result: list[dict]) -> dict:
        return {
            'count': len(result),
            'type': 'Clubes',
            'data': result,
        }
