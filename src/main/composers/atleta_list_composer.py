from src.presentation.controllers.atleta_list_controler import AtletaListController
from src.repository.repo_atleta import AtletaRepo
from src.use_cases.atleta_list import AtletaListUseCase


def atleta_list_composer():
    repository = AtletaRepo()
    atleta_list_use_case = AtletaListUseCase(atleta_repository=repository)
    controller = AtletaListController(use_case=atleta_list_use_case)

    return controller.handle
