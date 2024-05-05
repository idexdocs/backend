from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.controllers.atleta_create_controler import (
    AtletaCreateController,
)
from src.repository.repo_atleta import AtletaRepo
from src.use_cases.atleta_create import AtletaCreateUseCase


def atleta_create_composer():
    atleta_repository = AtletaRepo()
    use_case = AtletaCreateUseCase(
        atleta_repository=atleta_repository
    )
    controller = AtletaCreateController(use_case=use_case)

    return controller.handle
