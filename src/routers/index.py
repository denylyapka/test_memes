from typing import Annotated

from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy.orm import Session

from src.routers.api_photo import photo_upload
from src.sql_app import crud
from src.sql_app.main import get_db
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="src/templates")
router = APIRouter(prefix="/memes", tags=["Мемы"])


@router.get("")
async def get_all(db: Session = Depends(get_db)):
    return crud.get_all_memes(db=db)


@router.get("/{id}")
async def get_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_one_meme(db=db, meme_id=id)


@router.post("")
async def create(meme_name: Annotated[str, Form()],
                 meme_photo: Annotated[UploadFile, File()],
                 db: Session = Depends(get_db)):
    if "image" not in meme_photo.content_type:
        return {"status": 500, "message": "Отправьте пожалуйста фотографию"}
    photo_link_s3 = await photo_upload(id_meme=0, meme_photo=meme_photo, db=db)
    return crud.create_meme(db=db, data={"meme_name": meme_name, "meme_photo": photo_link_s3})


@router.put("/{id}")
async def update(id: int,
                 meme_name: Annotated[str, Form()] = None,
                 meme_photo: Annotated[UploadFile, File()] = None,
                 db: Session = Depends(get_db)):
    photo_link_s3 = ""
    if meme_photo:
        photo_link_s3 = await photo_upload(id_meme=id, meme_photo=meme_photo, db=db)
    return crud.update_meme(db=db, data={"meme_id": id, "meme_name": meme_name, "meme_photo": photo_link_s3})


@router.delete("/{id}")
async def delete(id: int, db: Session = Depends(get_db)):
    return crud.delete_meme(db=db, meme_id=id)

