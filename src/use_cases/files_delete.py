from urllib.parse import urlparse

from src.error.types.http_not_found import NotFoundError
from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_arquivos import ArquivoRepo


class DeleteFilesUseCase:
    def __init__(
        self,
        storage_service: AzureBlobStorage,
        arquivo_repository: ArquivoRepo,
    ):
        self.storage_service = storage_service
        self.arquivo_repository = arquivo_repository

    def execute(self, http_request: HttpRequest):
        imagem_id: int = http_request.path_params.get('id')

        return self._delete_image(imagem_id)

    def _delete_image(self, imagem_id: int):

        blob_url = self._get_imagem_blob_url(imagem_id)
        blob_name = self._extrair_path_name_do_blob_url(blob_url)
        self.storage_service.delete_imagem('atleta-imagens', blob_name)
        return self.arquivo_repository.delete_imagem(imagem_id)

    def _get_imagem_blob_url(self, imagem_id: int):
        blob = self.arquivo_repository.get_imagem_by_id(imagem_id)

        if blob is None:
            raise NotFoundError('Imagem não encontrada')
        return blob.blob_url

    def _extrair_path_name_do_blob_url(self, blob_url: str) -> str:
        # Parse the URL
        parsed_url = urlparse(blob_url)

        # Extract the path component
        path = parsed_url.path

        # Remove the leading slash if it exists and return
        return path[1:]
