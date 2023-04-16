from typing import Optional
from hotel_business_module.models.users import Worker
from hotel_business_module.models.groups import Group
from hotel_business_module.gateways.workers_gateway import WorkersGateway
from hotel_business_module.gateways.groups_gateway import GroupsGateway
from ..utils import return_validation_error, return_not_found_error, update_fields, token_required, permission_required
from hotel_business_module.session.session import get_session


@token_required
@permission_required(permissions=['add_worker'])
def resolve_create_worker(*_, input: dict, current_user):
    with get_session() as db:
        try:
            worker = Worker(**input)
            WorkersGateway.save_worker(worker, db)
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'worker': worker, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['edit_worker'])
def resolve_update_worker(*_, id: int, input: dict, current_user):
    with get_session() as db:
        worker: Worker = WorkersGateway.get_by_id(id, db)
        if worker is None:
            return return_not_found_error(Worker.REPR_MODEL_NAME)
        try:
            update_fields(worker, input)
            WorkersGateway.save_worker(worker, db)
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'worker': worker, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['delete_worker'])
def resolve_delete_worker(*_, id: int, current_user):
    with get_session() as db:
        worker: Worker = WorkersGateway.get_by_id(id, db)
        if worker is None:
            return return_not_found_error(Worker.REPR_MODEL_NAME)
        WorkersGateway.delete_worker(worker, db)
        return {'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['show_worker'])
def resolve_workers(*_, worker_id: Optional[int] = None, current_user):
    with get_session() as db:
        if worker_id:
            return {'workers': [WorkersGateway.get_by_id(worker_id, db)], 'status': {
                'success': True,
            }}
        return {'workers': WorkersGateway.get_all(db), 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['edit_worker', 'edit_group'])
def resolve_add_group_to_worker(*_, worker_id: int, group_id: int, current_user):
    with get_session() as db:
        worker: Worker = WorkersGateway.get_by_id(worker_id, db)
        if worker is None:
            return return_not_found_error(Worker.REPR_MODEL_NAME)
        group: Group = GroupsGateway.get_by_id(group_id, db)
        if group is None:
            return return_not_found_error(Group.REPR_MODEL_NAME)
        WorkersGateway.add_group_to_worker(worker, group, db)
        return {'worker': worker, 'group': group, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['edit_worker', 'edit_group'])
def resolve_remove_group_from_worker(*_, worker_id: int, group_id: int, current_user):
    with get_session() as db:
        worker: Worker = WorkersGateway.get_by_id(worker_id, db)
        if worker is None:
            return return_not_found_error(Worker.REPR_MODEL_NAME)
        group: Group = GroupsGateway.get_by_id(group_id, db)
        if group is None:
            return return_not_found_error(Group.REPR_MODEL_NAME)
        WorkersGateway.remove_group_from_worker(worker, group, db)
        return {'worker': worker, 'group': group, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['show_worker', 'show_group'])
def resolve_worker_groups(obj: Worker, *_, current_user):
    return {'groups': obj.groups, 'status': {
        'success': True,
    }}
