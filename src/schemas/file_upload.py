from fastapi import UploadFile
from pydantic import BaseModel


class FileUploadCreateSchema(BaseModel):
    image: UploadFile
