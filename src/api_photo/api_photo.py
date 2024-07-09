from fastapi import UploadFile, Depends
from sqlalchemy.orm import Session

from src.api_photo.exceptions import ErrorS3
from src.api_photo.s3 import *
from src.api_photo import crud
from src.main import get_db


async def photo_upload(id_meme: int, meme_photo: UploadFile, db: Session = Depends(get_db)) -> str:  # Сохранение файла в s3-хранилище
    # Получение формата
    frmt = ''.join(str(meme_photo.filename).split('.')[-1])

    # Получение последнего айди мема
    if id_meme == 0:
        id_meme = crud.get_last_id(db)

    # Сохранение файла в s3-хранилище
    try:
        with open(f"storage/meme_{id_meme}.{frmt}", 'wb') as file:
            file.write(bytes(meme_photo.file.read()))
            await get_name_and_file_remove(f"meme_{id_meme}.{frmt}")
            await get_name_and_file_upload(f"storage/meme_{id_meme}.{frmt}")
            photo_link_s3 = s3_base_link + f"meme_{id_meme}.{frmt}"

        # Удаление файла из локального хранилища (storage)
        os.remove(f"storage/meme_{id_meme}.png")
        return photo_link_s3
    except Exception:
        raise ErrorS3
