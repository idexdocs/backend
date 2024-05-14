from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


class AzureBlobStorage:
    # Use a class attribute for the BlobServiceClient if all instances share the same service client config
    _blob_service_client = None
    account_url = 'https://idexdocsblob.blob.core.windows.net'

    def __init__(self):

        # Initialize the BlobServiceClient once
        if AzureBlobStorage._blob_service_client is None:
            default_credential = DefaultAzureCredential()
            AzureBlobStorage._blob_service_client = BlobServiceClient(
                AzureBlobStorage.account_url, credential=default_credential
            )

        self.container_name = 'atleta-perfil'

    def upload_image(self, image_data: bytes, filename: str):
        try:
            # Get a blob client to perform the upload
            blob_client = self._blob_service_client.get_blob_client(
                container=self.container_name, blob=filename
            )
            blob_client.upload_blob(image_data, overwrite=True)
        except Exception as e:
            # Handle exceptions
            print(f'An error occurred while uploading {filename}: {e}')

    def get_image_url(self, blob_name: str) -> bytes:
        try:
            # Get a blob client to perform the download
            blob_client = self._blob_service_client.get_blob_client(
                container=self.container_name, blob=blob_name
            )
            # Verificando a existência do blob
            blob_client.get_blob_properties()

            return blob_client.url
        except ResourceNotFoundError:
            print(f'O blob nome {blob_name} não existe')
            return None
