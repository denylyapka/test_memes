from sqlalchemy.orm import Session

from src.models import models


def get_last_id(db: Session):
    id_meme = 0
    for item in db.query(models.Memes).filter().all():
        id_meme = item.id
    return id_meme + 1
