from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_relacionamento import RelacionamentoRepo


class RelacionamentoListUseCase:
    def __init__(
        self,
        relacionamento_repository: RelacionamentoRepo,
        atleta_repository: AtletaRepo,
    ):
        self.relacionamento_repository = relacionamento_repository
        self.atleta_repository = atleta_repository

    def execute(self, http_request: HttpRequest):
        atleta_id: int = int(http_request.path_params.get("id"))
        filters: dict = dict(http_request.query_params.items())

        self._check_atleta_exists(atleta_id)

        result = self._list_relacionamentos(atleta_id, filters)
        return self._format_response(result)

    def _check_atleta_exists(self, atleta_id: int):
        atleta = self.atleta_repository.get_atleta_by_id(atleta_id)
        if atleta is None:
            raise NotFoundError("Atleta não encontrado")

    def _list_relacionamentos(self, atleta_id: int, filters: dict):
        relacionamentos = self.relacionamento_repository.list_relacionamento(
            atleta_id, filters
        )

        if len(relacionamentos) == 0:
            raise NotFoundError(
                "O Atleta nao possui questionarios cadastrados"
            )

        return relacionamentos

    def _format_response(self, result: list[dict]) -> dict:
        return {
            "count": len(result),
            "type": "Relacionamento",
            "data": result,
        }
