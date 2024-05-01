from src.presentation.controllers.clube_list_controler import (
    ClubeListController,
)
from src.repository.repo_clube import ClubeRepo
from src.use_cases.clube_list import ClubeListUseCase


def clube_list_composer():
    repository = ClubeRepo()

    use_case = ClubeListUseCase(repository)
    controller = ClubeListController(use_case=use_case)

    return controller.handle
