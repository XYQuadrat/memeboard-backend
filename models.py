from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import object_session
from sqlalchemy.ext.hybrid import hybrid_property

from database import Base


class Tag(Base):
    __tablename__ = "tag"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)


class MediaItem(Base):
    __tablename__ = "media_item"

    id = Column("id", Integer, primary_key=True)
    filename = Column("filename", String)
    author_id = Column("author_id", Integer)
    score = Column("score", Integer)
    message_url = Column("message_url", String)
    created_date = Column("created_date", DateTime)

    @hybrid_property
    def tags(self) -> list[Tag]:
        statement = """
            SELECT tmp.* FROM (
                SELECT
                    tag.*,
                    media_item_tag.media_item_id
                FROM tag JOIN media_item_tag ON tag.id = media_item_tag.tag_id
            ) AS tmp
            JOIN media_item ON media_item.id = tmp.media_item_id
            WHERE media_item.id = :id
        """
        return (
            object_session(self).execute(statement, params={"id": self.id}).fetchall()
        )

    @tags.expression
    def tags(cls):
        return [Tag]

    @property
    def author_name(self):
        statement = """
            SELECT username.username
            FROM username
            JOIN media_item ON media_item.author_id = username.author_id
            WHERE media_item.author_id = :author_id
            LIMIT 1
        """

        result = object_session(self).execute(statement, params={"author_id": self.author_id}).fetchone()
        return result[0] if result is not None else "Unknown"


class MediaItemTag(Base):
    __tablename__ = "media_item_tag"

    media_item_id = Column(
        "media_item_id", Integer, ForeignKey(MediaItem.id), primary_key=True
    )
    tag_id = Column("tag_id", Integer, ForeignKey(Tag.id), primary_key=True)


class Username(Base):
    __tablename__ = "username"

    author_id = Column("author_id", Integer, primary_key=True)
    username = Column("username", String)