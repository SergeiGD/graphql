from typing import Optional
from ...models.tags import Tag
from ...models.base import db
from ...managers.tags_manager import TagsManager
from ..utils import return_validation_error, return_not_found_error, update_fields


def resolve_create_tag(*_, input: dict):
    try:
        tag = Tag(**input)
        TagsManager.save_tag(tag)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'tag': tag, 'status': {
        'success': True,
    }}


def resolve_update_tag(*_, id: int, input: dict):
    tag: Tag = db.session.query(Tag).filter(
        Tag.id == id
    ).first()
    if tag is None:
        return return_not_found_error(Tag.REPR_MODEL_NAME)
    try:
        update_fields(tag, input)
        TagsManager.save_tag(tag)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'tag': tag, 'status': {
        'success': True,
    }}


def resolve_delete_tag(*_, id: int):
    tag: Tag = db.session.query(Tag).filter(
        Tag.id == id,
    ).first()
    if tag is None:
        return return_not_found_error(Tag.REPR_MODEL_NAME)
    TagsManager.delete_tag(tag)
    return {'status': {
        'success': True,
    }}


def resolve_tags(*_, tag_id: Optional[int] = None):
    if tag_id:
        return db.session.query(Tag).filter_by(id=tag_id)
    return db.session.query(Tag).all()
