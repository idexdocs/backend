from urllib.parse import urlparse

from src.error.types.http_not_found import NotFoundError
from src.main.adapters.azure_blob_storage import AzureBlobStorage
from src.presentation.http_types.http_request import HttpRequest
from src.repository.repo_videos import VideoRepo


class VideoDeleteUseCase:
    def __init__(
        self,
        storage_service: AzureBlobStorage,
        video_repository: VideoRepo,
    ):
        self.storage_service = storage_service
        self.video_repository = video_repository

    def execute(self, http_request: HttpRequest):
        video_id: int = int(http_request.path_params.get('id'))

        blob = self._get_video_blob(video_id)
        self._delete_blob_assets(blob)
        return self.video_repository.delete_video(video_id)

    def _get_video_blob(self, video_id: int):
        blob = self.video_repository.get_video_by_id(video_id)
        if blob is None:
            raise NotFoundError('Vídeo não encontrado')
        return blob

    def _delete_blob_assets(self, blob):
        if blob.tipo == 'video':
            blob_name = self._extrair_blob_path_name(blob.blob_url)
            self.storage_service.delete_imagem('atleta-videos', blob_name)

    def _extrair_blob_path_name(self, blob_url: str) -> str:
        # Parse the URL
        parsed_url = urlparse(blob_url)
        # Extract the path component
        path = parsed_url.path
        # Remove the leading slash if it exists and return
        return path[1:]
