from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


class AzureBlobStorage:
    # Use a class attribute for the BlobServiceClient if all instances share the same service client config
    _blob_service_client = None

    def __init__(self):
        account_url = 'https://idexdocsblob.blob.core.windows.net'

        # Initialize the BlobServiceClient once
        if AzureBlobStorage._blob_service_client is None:
            default_credential = DefaultAzureCredential()
            AzureBlobStorage._blob_service_client = BlobServiceClient(
                account_url, credential=default_credential
            )

        self.container_name = 'atleta-perfil'

    def upload_image(self, image_data: bytes, filename: str):
        try:
            # Get a blob client to perform the upload
            blob_client = self._blob_service_client.get_blob_client(
                container=self.container_name, blob=filename
            )
            blob_client.upload_blob(image_data)
            print(f'Upload of {filename} successful')
        except Exception as e:
            # Handle exceptions
            print(f'An error occurred while uploading {filename}: {e}')

    def download_image(self, filename: str) -> bytes:
        try:
            # Get a blob client to perform the download
            blob_client = self._blob_service_client.get_blob_client(
                container=self.container_name, blob=filename
            )
            # Download the blob
            blob_data = blob_client.download_blob()
            # Return the blob data
            return blob_data.readall()
        except Exception as e:
            # Handle exceptions
            print(f'An error occurred while downloading {filename}: {e}')
            return None
