from typing import Optional
from sqlalchemy import inspect, func
from ..models.photos import Photo
from ..models.base import db


class PhotosManager:
    @staticmethod
    def swap_photos(photo: Photo):
        photo_to_swap = db.session.query(Photo).filter(
            Photo.category_id == photo.category_id,
            Photo.order == photo.order
        ).first()
        if photo_to_swap is None:
            raise ValueError('Не найдена фотография с таким номером')

        current_order = db.session.query(Photo).get(photo.id).order
        photo_to_swap.order = current_order

    @staticmethod
    def delete_photo(photo: Photo):
        db.session.query(Photo).filter(
            Photo.category_id == photo.category_id,
            Photo.order > photo.order
        ).update({'order': Photo.order - 1})
        db.session.delete(photo)
        db.session.commit()

    @staticmethod
    def save_photo(photo: Photo):
        db.session.add(photo)

        if photo.order is not None and inspect(photo).attrs.order.history.has_changes():
            db.session.expunge(photo)
            PhotosManager.swap_photos(photo)
            db.session.merge(photo)

        if photo.id is None and photo.order is None:
            with db.session.no_autoflush:
                current_max = db.session.query(func.max(Photo.order)).filter(
                    Photo.category_id == photo.category_id
                ).scalar()
                if current_max is None:
                    photo.order = 1
                else:
                    photo.order = current_max + 1

        db.session.commit()

