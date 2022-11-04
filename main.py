from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session
from sqlalchemy import func

from typing import Union

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import schemas, database, models

from database import MediaItem, Tag, MediaItemTag

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

session: Session = database.SessionLocal()


@app.get("/media/{id}", response_model=schemas.MediaItem)
async def read_media(id: int):
    return session.query(models.MediaItem).filter(models.MediaItem.id == id).first()


@app.get("/media/top/", response_model=list[schemas.MediaItem])
async def get_top_media(skip: int = 0, limit: int = 10, tag_id: Union[int,None] = Query(default=None)):
    if limit > 100:
        raise HTTPException(status_code=418, detail="Exceeded maximum allowed limit.")

    query = (
        session.query(models.MediaItem)
    )

    if tag_id:
        query = query.join(models.MediaItemTag).filter(models.MediaItemTag.tag_id == tag_id)

    return (
        query
        .order_by(MediaItem.c.score.desc())
        .group_by(MediaItem.c.id)
        .limit(limit)
        .offset(skip)
        .all()
    )


@app.get("/tags/", response_model=list[schemas.Tag])
async def get_all_tags():
    return session.query(Tag).all()


@app.get("/media/{id}/tags/", response_model=list[schemas.Tag])
async def get_tags(id: int):
    return (
        session.query(Tag)
        .join(MediaItemTag, MediaItemTag.columns.tag_id == Tag.columns.id)
        .filter(MediaItemTag.columns.media_item_id == id)
        .all()
    )


@app.post("/media/{media_item_id}/tags/")
async def write_tags(media_item_id: int, tags: schemas.TagList):
    media_item_tags: list[models.MediaItemTag] = [
        models.MediaItemTag(media_item_id=media_item_id, tag_id=tag.id)
        for tag in tags.data
    ]

    session.execute(
        MediaItemTag.delete().where(MediaItemTag.c.media_item_id == media_item_id)
    )
    session.commit()

    for media_item_tag in media_item_tags:
        session.execute(
            insert(models.MediaItemTag)
            .values(
                media_item_id=media_item_tag.media_item_id, tag_id=media_item_tag.tag_id
            )
            .on_conflict_do_nothing(index_elements=["media_item_id", "tag_id"])
        )
        session.commit()


@app.get("/tag-queue/", response_model=schemas.MediaItem)
async def get_untagged_id():
    all_media_items = session.query(models.MediaItem.id.label("id"))
    all_tags = session.query(models.MediaItemTag.media_item_id.label("id"))
    untagged_media_item_id = (
        all_media_items.except_(all_tags).order_by(func.random()).limit(1)
    )

    untagged_media_item: schemas.MediaItem = session.query(models.MediaItem).filter(
        models.MediaItem.id == untagged_media_item_id.scalar_subquery()
    )

    return untagged_media_item.first()