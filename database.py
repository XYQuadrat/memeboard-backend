from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import DB_PATH

SQLALCHEMY_DB_URL = "sqlite:///" + DB_PATH

engine = create_engine(SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False})

MediaItemMeta = MetaData(engine)
MediaItem = Table("media_item", MediaItemMeta, autoload=True)

TagMeta = MetaData(engine)
Tag = Table("tag", TagMeta, autoload=True)

MediaItemTagMeta = MetaData(engine)
MediaItemTag = Table("media_item_tag", MediaItemTagMeta, autoload=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
