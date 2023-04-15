from typing import Optional
from ...models.tags import Tag
from ...db_gateways.tags_gateway import TagsGateway
from ..utils import return_validation_error, return_not_found_error, update_fields, token_required, permission_required
from ...session.session import get_session


@token_required
@permission_required(permissions=['add_tag'])
def resolve_create_tag(*_, input: dict, current_user):
    with get_session() as db:
        try:
            tag = Tag(**input)
            TagsGateway.save_tag(tag, db)
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'tag': tag, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['edit_tag'])
def resolve_update_tag(*_, id: int, input: dict, current_user):
    with get_session() as db:
        tag: Tag = TagsGateway.get_by_id(id, db)
        if tag is None:
            return return_not_found_error(Tag.REPR_MODEL_NAME)
        try:
            update_fields(tag, input)
            TagsGateway.save_tag(tag, db)
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'tag': tag, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['delete_tag'])
def resolve_delete_tag(*_, id: int, current_user):
    with get_session() as db:
        tag = TagsGateway.get_by_id(id, db)
        if tag is None:
            return return_not_found_error(Tag.REPR_MODEL_NAME)
        TagsGateway.delete_tag(tag, db)
        return {'status': {
            'success': True,
        }}


def resolve_tags(*_, tag_id: Optional[int] = None):
    with get_session() as db:
        if tag_id:
            return {'tags': [TagsGateway.get_by_id(tag_id, db)], 'status': {
                'success': True,
            }}
        return {'tags': TagsGateway.get_all(db), 'status': {
            'success': True,
        }}
