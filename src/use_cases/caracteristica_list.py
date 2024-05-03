from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_caracteristicas import CaracteristicasRepo


class CaracteristicaListUseCase:
    def __init__(
        self,
        atleta_repository: AtletaRepo,
        caracteristica_repository: CaracteristicasRepo,
    ):
        self.atleta_repository = atleta_repository
        self.caracteristica_repository = caracteristica_repository

    def execute(self, http_request: HttpRequest):
        atleta_id: int = int(http_request.path_params.get('id'))
        filters: dict = dict(http_request.query_params.items())

        self._check_atleta_exists(atleta_id)

        result, model_name = self._list_caracteristica(
            atleta_id, filters, filters.get('model')
        )

        return self._format_response(result, model_name)

    def _check_atleta_exists(self, atleta_id: int):
        atleta = self.atleta_repository.get_atleta_by_id(atleta_id)
        if atleta is None:
            raise NotFoundError('Atleta não encontrado')

    def _list_caracteristica(
        self, atleta_id: int, filters: dict, model_name: str
    ):
        (
            caracteristicas,
            model_name,
        ) = self.caracteristica_repository.list_caracteristica(
            atleta_id, filters
        )

        if len(caracteristicas) == 0:
            caracteristica = model_name[:14].lower()
            tipo = model_name[14:].lower()

            raise NotFoundError(
                f'O Atleta não possui {caracteristica} {tipo} cadastrada'
            )

        return caracteristicas, model_name

    def _format_response(self, result: list[dict], model_name: str) -> dict:
        return {
            'count': len(result),
            'type': model_name,
            'data': result,
        }
