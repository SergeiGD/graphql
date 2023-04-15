from typing import Optional
from ..settings import settings
import uuid
import os
from starlette.datastructures import UploadFile


class FileManager:
    @staticmethod
    def save_file(file: UploadFile, old_path: Optional[str] = None):
        if old_path is not None:
            # удаляем старую фотографию, если грузим новую
            try:
                os.remove(old_path)
            except OSError:
                pass
        file_name = uuid.uuid4()
        extension = file.filename.split('.')[-1]
        full_path = f'{settings.MEDIA_DIR}/{file_name.hex}.{extension}'
        with open(full_path, 'wb') as file_object:
            content = file.file.read()
            file_object.write(content)
        return full_path

    @staticmethod
    def delete_file(path: str):
        try:
            os.remove(path)
        except OSError:
            pass
