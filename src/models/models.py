from sqlalchemy import Column, Integer, String

from src.database import Base


class Memes(Base):
    __tablename__ = 'memes'

    id = Column(Integer, primary_key=True)
    meme_name = Column(String, nullable=False)
    meme_photo = Column(String, nullable=False)
