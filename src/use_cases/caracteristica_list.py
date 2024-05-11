from collections import defaultdict

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

        total_count, result, model_name = self._list_caracteristica(
            atleta_id, filters, filters.get('model')
        )

        return self._format_response(total_count, result, model_name)

    def _check_atleta_exists(self, atleta_id: int):
        atleta = self.atleta_repository.get_atleta_by_id(atleta_id)
        if atleta is None:
            raise NotFoundError('Atleta não encontrado')

    def _list_caracteristica(
        self, atleta_id: int, filters: dict, model_name: str
    ):
        (
            total_count,
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

        agregado = self._agrega_total_e_media(caracteristicas)

        return total_count, agregado, model_name

    def _agrega_total_e_media(self, caracteristicas: list):
        data = caracteristicas

        result = defaultdict(list)
        suffixes = ['_fis', '_tec', '_psi']
        mapper = {'_fis': 'fisico', '_tec': 'tecnico', '_psi': 'psicologico'}

        # Collect keys that don't need processing for sums and means just once
        excluded_keys = {'id', 'data_avaliacao'}
        for item in data:
            for suffix in suffixes:
                extracted = {
                    key: value
                    for key, value in item.items()
                    if key.endswith(suffix) or key in excluded_keys
                }

                # Calculate the sum and mean outside of the innermost loop
                numeric_values = [
                    value
                    for key, value in extracted.items()
                    if key not in excluded_keys
                ]
                total = sum(numeric_values)
                mean = total / len(numeric_values)

                extracted['sum'] = total
                extracted['mean'] = mean

                result[mapper.get(suffix)].append(extracted)

        return dict(result)

    def _format_response(
        self, total_count: int, result: list[dict], model_name: str
    ) -> dict:
        return {
            'count': len(result),
            'total': total_count,
            'type': model_name,
            'data': result,
        }
