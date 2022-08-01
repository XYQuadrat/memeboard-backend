from typing import Optional

from pydantic import BaseModel


def to_camel(string: str) -> str:
    return "".join(word.capitalize() for word in string.split("_"))


class Model(BaseModel):
    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class Tag(Model):
    id: int
    name: str


class MediaItem(Model):
    id: int
    filename: str
    score: int
    author: str
    tags: list[Tag]


class MediaItemTag(Model):
    media_item_id: int
    tag_id: int


class TagList(Model):
    data: list[Tag]
