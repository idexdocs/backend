from fastapi import UploadFile

from src.error.types.http_not_found import NotFoundError
from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_atleta import AtletaRepo


class FileUploadUseCase:
    def __init__(
        self, atleta_repository: AtletaRepo, storage_service: AzureBlobStorage
    ):
        self.storage_service = storage_service
        self.atleta_repository = atleta_repository

    def execute(self, http_request: HttpRequest):
        atleta_id: int = http_request.path_params.get('id')
        image_file: UploadFile = http_request.files.get('image')

        self._check_atleta_exists(atleta_id)
        self._upload_image(image_file, atleta_id)

        return self._format_response()

    def _check_atleta_exists(self, atleta_id: int):
        atleta = self.atleta_repository.get_atleta_by_id(atleta_id)
        if atleta is None:
            raise NotFoundError('Atleta não encontrado')

    def _upload_image(self, image_file: UploadFile, atleta_id: int):
        filename = f'atleta_{atleta_id}_{image_file.filename}'
        try:
            self.storage_service.upload_image(image_file.file.read(), filename)
        except Exception as e:
            # Handle upload failure
            raise RuntimeError(f'Failed to upload image: {e}')

    def _format_response(self) -> dict:
        return {
            'type': 'FileUpload',
            'status': True,
            'message': 'Arquivo salvo com sucesso',
        }
