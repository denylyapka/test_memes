from typing import List

from sqlalchemy import BigInteger, Date, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Memes(Base):
    __tablename__ = 'memes'

    id = Column(Integer, primary_key=True)
    meme_name = Column(String, nullable=False)
    meme_photo = Column(String, nullable=False)
