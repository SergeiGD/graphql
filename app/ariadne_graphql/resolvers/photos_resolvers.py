from typing import Optional
from hotel_business_module.models.photos import Photo
from hotel_business_module.gateways.photos_gateway import PhotosGateway
from ..utils import return_validation_error, return_not_found_error, update_fields, token_required, permission_required
from werkzeug.datastructures import FileStorage
from hotel_business_module.session.session import get_session
from starlette.datastructures import UploadFile


@token_required
@permission_required(permissions=['add_photo'])
def resolve_create_photo(*_, input: dict, file: UploadFile, current_user):
    with get_session() as db:
        try:
            photo = Photo(**input)
            PhotosGateway.save_photo(
                photo=photo,
                db=db,
                file=file.file,
                file_name=file.filename,
            )
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'photo': photo, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['update_photo'])
def resolve_update_photo(*_, id: int, input: dict, file: Optional[FileStorage] = None, current_user):
    with get_session() as db:
        photo: Photo = PhotosGateway.get_by_id(id, db)
        if photo is None:
            return return_not_found_error(Photo.REPR_MODEL_NAME)
        try:
            update_fields(photo, input)
            PhotosGateway.save_photo(
                photo=photo,
                db=db,
                file=file.file,
                file_name=file.filename,
            )
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'photo': photo, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['delete_photo'])
def resolve_delete_photo(*_, id: int, current_user):
    with get_session() as db:
        photo: Photo = PhotosGateway.get_by_id(id, db)
        if photo is None:
            return return_not_found_error(Photo.REPR_MODEL_NAME)
        PhotosGateway.delete_photo(photo, db)
        return {'status': {
            'success': True,
        }}


def resolve_photos(*_, photo_id: Optional[int] = None):
    with get_session() as db:
        if photo_id:
            return {'photos': [PhotosGateway.get_by_id(photo_id, db)], 'status': {
                'success': True,
            }}
        return {'photos': PhotosGateway.get_all(db), 'status': {
            'success': True,
        }}
