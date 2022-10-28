from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Model(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class Tag(Model):
    id: int
    name: str


class MediaItem(Model):
    id: int
    filename: str
    score: int
    author_id: str
    message_url: str
    created_date: datetime
    tags: list[Tag]


class MediaItemTag(Model):
    media_item_id: int
    tag_id: int


class TagList(Model):
    data: list[Tag]
