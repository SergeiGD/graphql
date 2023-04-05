from typing import Optional
from ..settings import settings
from sqlalchemy import inspect, func
from ..models.photos import Photo
from ..models.base import db
from ..utils.file_manager import FileManager
from werkzeug.datastructures import FileStorage
import uuid


class PhotosManager:
    """
    Класс для управления фотографиями
    """
    @staticmethod
    def swap_photos(photo: Photo):
        """
        Метод для перестановки фотографий местами
        :param photo: фото, которому обновляем порядок
        :return:
        """
        # ищем фотографию, с которой поменяется местами
        photo_to_swap = db.session.query(Photo).filter(
            Photo.category_id == photo.category_id,
            Photo.order == photo.order
        ).first()
        if photo_to_swap is None:
            raise ValueError('Не найдена фотография с таким номером')

        # меняем местами фотографии
        current_order = db.session.query(Photo).get(photo.id).order
        photo_to_swap.order = current_order

    @staticmethod
    def delete_photo(photo: Photo):
        """
        Удалить фотографию
        :param photo: фотографию, которую нужно удалить
        :return:
        """
        # все последующий фотографии сдвигаем на 1
        db.session.query(Photo).filter(
            Photo.category_id == photo.category_id,
            Photo.order > photo.order
        ).update({'order': Photo.order - 1})
        FileManager.delete_file(photo.path)
        db.session.delete(photo)
        db.session.commit()

    @staticmethod
    def save_photo(photo: Photo, file: Optional[FileStorage]):
        db.session.add(photo)

        # если обновляли и поменяли порядок, то меняем местами
        if photo.order is not None and inspect(photo).attrs.order.history.has_changes():
            db.session.expunge(photo)
            PhotosManager.swap_photos(photo)
            db.session.merge(photo)

        # если создали новую, то автоматическа установливаем порядок (ставим последней)
        if photo.id is None and photo.order is None:
            with db.session.no_autoflush:
                #  ищем текущую крайнюю фотографию категории
                current_max = db.session.query(func.max(Photo.order)).filter(
                    Photo.category_id == photo.category_id
                ).scalar()
                if current_max is None:
                    # если это первая фотография категории, то ставим 1
                    photo.order = 1
                else:
                    photo.order = current_max + 1

        if file is not None:
            path = FileManager.save_file(file, photo.path)
            photo.path = path

        db.session.commit()

