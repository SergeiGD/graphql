from typing import Optional
from ...models.users import Worker
from ...models.groups import Group
from ...models.base import db
from ...managers.workers_manager import WorkersManager
from ..utils import return_validation_error, return_not_found_error, update_fields, token_required, permission_required


@token_required
@permission_required(permissions=['add_worker'])
def resolve_create_worker(*_, input: dict, current_user):
    try:
        worker = Worker(**input)
        WorkersManager.save_worker(worker)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'worker': worker, 'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['edit_worker'])
def resolve_update_worker(*_, id: int, input: dict, current_user):
    worker: Worker = db.session.query(Worker).filter(
        Worker.id == id,
        Worker.date_deleted == None,
    ).first()
    if worker is None:
        return return_not_found_error(Worker.REPR_MODEL_NAME)
    try:
        update_fields(worker, input)
        WorkersManager.save_worker(worker)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'worker': worker, 'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['delete_worker'])
def resolve_delete_worker(*_, id: int, current_user):
    worker: Worker = db.session.query(Worker).filter(
        Worker.id == id,
        Worker.date_deleted == None,
    ).first()
    if worker is None:
        return return_not_found_error(Worker.REPR_MODEL_NAME)
    WorkersManager.delete_worker(worker)
    return {'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['show_worker'])
def resolve_workers(*_, worker_id: Optional[int] = None, current_user):
    if worker_id:
        worker = db.session.query(Worker).filter_by(id=worker_id, date_deleted=None)
        return {'workers': worker, 'status': {
            'success': True,
        }}
    workers = db.session.query(Worker).filter_by(date_deleted=None)
    return {'workers': workers, 'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['edit_worker', 'edit_group'])
def resolve_add_group_to_worker(*_, worker_id: int, group_id: int, current_user):
    worker: Worker = db.session.query(Worker).filter(
        Worker.id == worker_id,
        Worker.date_deleted == None,
    ).first()
    if worker is None:
        return return_not_found_error(Worker.REPR_MODEL_NAME)
    group: Group = db.session.query(Group).filter(
        Group.id == group_id,
    ).first()
    if group is None:
        return return_not_found_error(Group.REPR_MODEL_NAME)
    WorkersManager.add_group_to_worker(worker, group)
    return {'worker': worker, 'group': group, 'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['edit_worker', 'edit_group'])
def resolve_remove_group_from_worker(*_, worker_id: int, group_id: int, current_user):
    worker: Worker = db.session.query(Worker).filter(
        Worker.id == worker_id,
        Worker.date_deleted == None,
    ).first()
    if worker is None:
        return return_not_found_error(Worker.REPR_MODEL_NAME)
    group: Group = db.session.query(Group).filter(
        Group.id == group_id,
    ).first()
    if group is None:
        return return_not_found_error(Group.REPR_MODEL_NAME)
    WorkersManager.remove_group_from_worker(worker, group)
    return {'worker': worker, 'group': group, 'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['show_worker', 'show_group'])
def resolve_worker_groups(obj: Worker, *_, current_user):
    return {'groups': obj.groups, 'status': {
        'success': True,
    }}
