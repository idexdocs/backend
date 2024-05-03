from sqlmodel import SQLModel

from src.error.types.http_not_found import NotFoundError
from src.presentation.http_types.http_request import HttpRequest
from src.repository.model_objects import (
    CaracteristicaAtacante,
    CaracteristicaFisica,
    CaracteristicaGoleiro,
    CaracteristicaLateral,
    CaracteristicaMeia,
    CaracteristicaVolante,
    CaracteristicaZagueiro,
)
from src.repository.repo_atleta import AtletaRepo
from src.repository.repo_caracteristicas import CaracteristicasRepo


class CaracteristicaListUseCase:
    MODELS = {
        'fisico': CaracteristicaFisica,
        'zagueiro': CaracteristicaZagueiro,
        'lateral': CaracteristicaLateral,
        'goleiro': CaracteristicaGoleiro,
        'volante': CaracteristicaVolante,
        'atacante': CaracteristicaAtacante,
        'meia': CaracteristicaMeia,
    }

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
        # seleciona a tabela de característica correspondente à posição do jogador
        model = self._get_model(filters.get('model'))

        self._check_atleta_exists(atleta_id)

        result, model_name = self._list_caracteristica(
            atleta_id, filters, model
        )
        return self._format_response(result, model_name)

    def _check_atleta_exists(self, atleta_id: int):
        atleta = self.atleta_repository.get_atleta_by_id(atleta_id)
        if atleta is None:
            raise NotFoundError('Atleta não encontrado')

    def _get_model(self, model: SQLModel):

        if model not in self.MODELS:
            raise ValueError(f'Característica não é válida: {model}')

        return self.MODELS.get(model)

    def _list_caracteristica(
        self, atleta_id: int, filters: dict, model: SQLModel
    ):
        caracteristicas = self.caracteristica_repository.list_caracteristica(
            atleta_id, filters, model
        )

        if len(caracteristicas) == 0:
            caracteristica = model.__name__[:14].lower()
            tipo = model.__name__[14:].lower()

            raise NotFoundError(
                f'O Atleta não possui {caracteristica} {tipo} cadastrada'
            )

        return caracteristicas

    def _format_response(self, result: list[dict], model_name: str) -> dict:
        return {
            'count': len(result),
            'type': model_name,
            'data': result,
        }
