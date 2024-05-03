from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_observacao import ObservacaoRepo


class ObservacaoListUseCase:
    def __init__(
        self,
        observacao_repository: ObservacaoRepo,
        atleta_repository: AtletaRepo,
    ):
        self.observacao_repository = observacao_repository
        self.atleta_repository = atleta_repository

    def execute(self, http_request: HttpRequest):
        atleta_id: int = int(http_request.path_params.get('id'))

        self._check_atleta_exists(atleta_id)

        result = self._list_observacao(atleta_id)
        return self._format_response(result)

    def _check_atleta_exists(self, atleta_id: int):
        atleta = self.atleta_repository.get_atleta_by_id(atleta_id)
        if atleta is None:
            raise NotFoundError('Atleta não encontrado')

    def _list_observacao(self, atleta_id: int):
        observacoes = self.observacao_repository.list_observacao(atleta_id)

        if len(observacoes) == 0:
            raise NotFoundError('O Atleta não possui observações cadastradas')

        return observacoes

    def _format_response(self, result: list[dict]) -> dict:
        return {
            'count': len(result),
            'type': 'Observações',
            'data': result,
        }