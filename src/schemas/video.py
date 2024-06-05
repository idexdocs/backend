from pydantic import BaseModel


class VideoCreateSchema(BaseModel):
    video_url: str
