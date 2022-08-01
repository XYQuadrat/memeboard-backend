from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import object_session

from database import Base


class Tag(Base):
    __tablename__ = "Tag"

    id = Column("Id", Integer, primary_key=True)
    name = Column("Name", String)


class MediaItem(Base):
    __tablename__ = "MediaItem"

    id = Column("Id", Integer, primary_key=True)
    filename = Column("Filename", String)
    author = Column("Author", String)
    score = Column("Score", Integer)

    @property
    def tags(self):
        statement = """
            SELECT tmp.* FROM (
                SELECT
                    Tag.*,
                    MediaItemTag.MediaItemId
                FROM Tag JOIN MediaItemTag ON Tag.Id = MediaItemTag.TagId
            ) AS tmp
            JOIN MediaItem ON MediaItem.Id = tmp.MediaItemId
            WHERE MediaItem.Id = :id
        """
        return (
            object_session(self).execute(statement, params={"id": self.id}).fetchall()
        )


class MediaItemTag(Base):
    __tablename__ = "MediaItemTag"

    media_item_id = Column(
        "MediaItemId", Integer, ForeignKey(MediaItem.id), primary_key=True
    )
    tag_id = Column("TagId", Integer, ForeignKey(Tag.id), primary_key=True)
