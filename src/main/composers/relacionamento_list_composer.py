from src.presentation.controllers.relacionamento_list_controler import RelacionamentoListController
from src.repository.repo_relacionamento import RelacionamentoRepo
from src.use_cases.relacionamento_list import RelacionamentoListUseCase


def relacionamento_list_composer():
    repository = RelacionamentoRepo()
    use_case = RelacionamentoListUseCase(repository=repository)
    controller = RelacionamentoListController(use_case=use_case)

    return controller.handle
