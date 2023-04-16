from typing import Optional
from hotel_business_module.models.groups import Group
from hotel_business_module.models.permissions import Permission
from hotel_business_module.gateways.groups_gateway import GroupsGateway
from hotel_business_module.gateways.permissions_gateway import PermissionsGateway
from ..utils import return_validation_error, return_not_found_error, update_fields, token_required, permission_required
from hotel_business_module.session.session import get_session


@token_required
@permission_required(permissions=['add_group'])
def resolve_create_group(*_, input: dict, current_user):
    with get_session() as db:
        try:
            group = Group(**input)
            GroupsGateway.save_group(group, db)
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'group': group, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['edit_group'])
def resolve_update_group(*_, id: int, input: dict, current_user):
    with get_session() as db:
        group: Group = GroupsGateway.get_by_id(id, db)
        if group is None:
            return return_not_found_error(Group.REPR_MODEL_NAME)
        try:
            update_fields(group, input)
            GroupsGateway.save_group(group, db)
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'group': group, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['delete_group'])
def resolve_delete_group(*_, id: int, current_user):
    with get_session() as db:
        group: Group = GroupsGateway.get_by_id(id, db)
        if group is None:
            return return_not_found_error(Group.REPR_MODEL_NAME)
        GroupsGateway.delete_group(group, db)
        return {'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['show_group'])
def resolve_groups(*_, group_id: Optional[int] = None, current_user):
    with get_session() as db:
        if group_id:
            return {'groups': [GroupsGateway.get_by_id(group_id, db)], 'status': {
                'success': True,
            }}
        return {'groups': GroupsGateway.get_all(db), 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['edit_group', 'edit_worker'])
def resolve_add_permission_to_group(*_, permission_id: int, group_id: int, current_user):
    with get_session() as db:
        permission: Permission = PermissionsGateway.get_by_id(permission_id, db)
        if permission is None:
            return return_not_found_error(Permission.REPR_MODEL_NAME)
        group: Group = GroupsGateway.get_by_id(group_id, db)
        if group is None:
            return return_not_found_error(Group.REPR_MODEL_NAME)
        GroupsGateway.add_permission_to_group(group, permission, db)
        return {'permission': permission, 'group': group, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['edit_group', 'edit_worker'])
def resolve_remove_permission_from_group(*_, permission_id: int, group_id: int, current_user):
    with get_session() as db:
        permission: Permission = PermissionsGateway.get_by_id(permission_id, db)
        if permission is None:
            return return_not_found_error(Permission.REPR_MODEL_NAME)
        group: Group = GroupsGateway.get_by_id(group_id, db)
        if group is None:
            return return_not_found_error(Group.REPR_MODEL_NAME)
        GroupsGateway.remove_permission_from_group(group, permission, db)
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
