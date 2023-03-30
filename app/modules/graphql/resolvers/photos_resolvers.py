from typing import Optional
from ...models.photos import Photo
from ...models.base import db
from ...managers.photos_manager import PhotosManager
from ..utils import return_validation_error, return_not_found_error, update_fields


def resolve_create_photo(*_, input: dict):
    try:
        photo = Photo(**input)
        PhotosManager.save_photo(photo)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'photo': photo, 'status': {
        'success': True,
    }}


def resolve_update_photo(*_, id: int, input: dict):
    photo: Photo = db.session.query(Photo).filter(
        Photo.id == id
    ).first()
    if photo is None:
        return return_not_found_error(Photo.REPR_MODEL_NAME)
    try:
        update_fields(photo, input)
        PhotosManager.save_photo(photo)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'photo': photo, 'status': {
        'success': True,
    }}


def resolve_delete_photo(*_, id: int):
    photo: Photo = db.session.query(Photo).filter(
        Photo.id == id,
    ).first()
    if photo is None:
        return return_not_found_error(Photo.REPR_MODEL_NAME)
    PhotosManager.delete_photo(photo)
    return {'status': {
        'success': True,
    }}


def resolve_photos(*_, photo_id: Optional[int] = None):
    if photo_id:
        return db.session.query(Photo).filter_by(id=photo_id)
    return db.session.query(Photo).all()
