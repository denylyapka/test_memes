from sqlalchemy.orm import Session

from src.sql_app import models


def get_all_memes(db: Session):
    return db.query(models.Memes).filter().all()

def get_one_meme(db: Session, meme_id: int):
    return db.query(models.Memes).filter(models.Memes.id == meme_id).first()

def create_meme(db: Session, data: dict):
    meme = models.Memes(meme_name=data["meme_name"], meme_photo=data["meme_photo"])
    db.add(meme)
    db.commit()
    db.refresh(meme)
    return meme

def update_meme(db: Session, data: dict):
    meme = db.query(models.Memes).filter(models.Memes.id == data["meme_id"]).first()
    print(data)
    if data["meme_name"]:
        meme.meme_name = data["meme_name"]
    if data["meme_photo"] != "":
        meme.meme_photo = data["meme_photo"]
    db.commit()
    return {"status": 200, "message": "obj has been updated"}, db.query(models.Memes).filter().all()


def delete_meme(db: Session, meme_id: int):
    meme = db.query(models.Memes).filter(models.Memes.id == meme_id).first()
    db.delete(meme)
    db.commit()
    return {"status": 200, "message": "obj has been deleted"}, db.query(models.Memes).filter().all()

def get_last_id(db: Session):
    id_meme = 0
    for item in db.query(models.Memes).filter().all():
        id_meme = item.id
    return id_meme + 1
