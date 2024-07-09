import os

from fastapi import UploadFile, Depends
from sqlalchemy.orm import Session

from src.aws_app.s3 import *
from src.sql_app import crud
from src.sql_app.main import get_db


async def photo_upload(id_meme: int, meme_photo: UploadFile, db: Session = Depends(get_db)) -> str:  # Сохранение файла в s3-хранилище
    # Получение формата
    frmt = ''.join(str(meme_photo.filename).split('.')[-1])

    # Получение последнего айди мема
    if id_meme == 0:
        id_meme = crud.get_last_id(db)

    # Сохранение файла в s3-хранилище
    with open(f"storage/meme_{id_meme}.{frmt}", 'wb') as file:
        file.write(bytes(meme_photo.file.read()))
        await get_name_and_file_remove(f"meme_{id_meme}.{frmt}")
        await get_name_and_file_upload(f"storage/meme_{id_meme}.{frmt}")
        photo_link_s3 = s3_base_link + f"meme_{id_meme}.{frmt}"

    # Удаление файла из локального хранилища (storage)
    try:
        os.remove(f"storage/user/meme_{id_meme}.png")
    except FileNotFoundError:
        pass
    return photo_link_s3
