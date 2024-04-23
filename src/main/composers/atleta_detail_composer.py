from src.presentation.controllers.atleta_detail_controler import (
    AtletaDetailController,
)
from src.repository.repo_atleta import AtletaRepo
from src.use_cases.atleta_detail import AtletaDetailUseCase


def atleta_detail_composer():
    repository = AtletaRepo()
    atleta_list_use_case = AtletaDetailUseCase(atleta_repository=repository)
    controller = AtletaDetailController(use_case=atleta_list_use_case)

    return controller.handle
