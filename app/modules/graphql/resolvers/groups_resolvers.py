from typing import Optional
from ...models.groups import Group
from ...models.permissions import Permission
from ...models.base import db
from ...managers.groups_manager import GroupsManager
from ..utils import return_validation_error, return_not_found_error, update_fields, token_required, permission_required


@token_required
@permission_required(permissions=['add_group'])
def resolve_create_group(*_, input: dict, current_user):
    try:
        group = Group(**input)
        GroupsManager.save_group(group)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'group': group, 'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['edit_group'])
def resolve_update_group(*_, id: int, input: dict, current_user):
    group: Group = db.session.query(Group).filter(
        Group.id == id
    ).first()
    if group is None:
        return return_not_found_error(Group.REPR_MODEL_NAME)
    try:
        update_fields(group, input)
        GroupsManager.save_group(group)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'group': group, 'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['delete_group'])
def resolve_delete_group(*_, id: int, current_user):
    group: Group = db.session.query(Group).filter(
        Group.id == id,
    ).first()
    if group is None:
        return return_not_found_error(Group.REPR_MODEL_NAME)
    GroupsManager.delete_group(group)
    return {'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['show_group'])
def resolve_groups(*_, photo_id: Optional[int] = None, current_user):
    if photo_id:
        group = db.session.query(Group).filter_by(id=photo_id)
        return {'groups': group, 'status': {
            'success': True,
        }}
    groups = db.session.query(Group).all()
    return {'groups': groups, 'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['edit_group', 'edit_worker'])
def resolve_add_permission_to_group(*_, permission_id: int, group_id: int, current_user):
    permission: Permission = db.session.query(Permission).filter(
        Permission.id == permission_id,
    ).first()
    if permission is None:
        return return_not_found_error(Permission.REPR_MODEL_NAME)
    group: Group = db.session.query(Group).filter(
        Group.id == group_id,
    ).first()
    if group is None:
        return return_not_found_error(Group.REPR_MODEL_NAME)
    GroupsManager.add_permission_to_group(group, permission)
    return {'permission': permission, 'group': group, 'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['edit_group', 'edit_worker'])
def resolve_remove_permission_from_group(*_, permission_id: int, group_id: int, current_user):
    permission: Permission = db.session.query(Permission).filter(
        Permission.id == permission_id,
    ).first()
    if permission is None:
        return return_not_found_error(Permission.REPR_MODEL_NAME)
    group: Group = db.session.query(Group).filter(
        Group.id == group_id,
    ).first()
    if group is None:
        return return_not_found_error(Group.REPR_MODEL_NAME)
    GroupsManager.remove_permission_from_group(group, permission)
    return {'permission': permission, 'group': group, 'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['show_permission'])
def resolve_group_permissions(obj: Group, *_, current_user):
    return {'permissions': obj.permissions, 'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['show_worker', 'show_client'])
def resolve_group_users(obj: Group, *_, current_user):
    return {'users': obj.users, 'status': {
        'success': True,
    }}
