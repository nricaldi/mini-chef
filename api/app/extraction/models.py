from pydantic import BaseModel, HttpUrl


class Recipe(BaseModel):
    name: str
    description: str


class VideoMetadata(BaseModel):
    description: str
    image_url: str
    title: str


class VideoRequest(BaseModel):
    url: HttpUrl


