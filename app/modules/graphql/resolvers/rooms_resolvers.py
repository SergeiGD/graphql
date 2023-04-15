from typing import Optional
from ...models.rooms import Room
from ...db_gateways.rooms_gateway import RoomsGateway
from ..utils import return_validation_error, return_not_found_error, update_fields, token_required, permission_required
from ...session.session import get_session
from sqlalchemy import inspect


# @token_required
# @permission_required(permissions=['add_room'])
# def resolve_create_room(*_, input: dict, current_user):
def resolve_create_room(*_, input: dict):
    with get_session() as db:
        try:
            room = Room(**input)
            RoomsGateway.save_room(room, db)
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'room': room, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['edit_room'])
def resolve_update_room(*_, id: int, input: dict, current_user):
    with get_session() as db:
        room: Room = RoomsGateway.get_by_id(id, db)
        if room is None:
            return return_not_found_error(Room.REPR_MODEL_NAME)
        try:
            update_fields(room, input)
            RoomsGateway.save_room(room)
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'room': room, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['delete_room'])
def resolve_delete_room(*_, id: int, current_user):
    with get_session() as db:
        room: Room = RoomsGateway.get_by_id(id, db)
        if room is None:
            return return_not_found_error(Room.REPR_MODEL_NAME)
        RoomsGateway.delete_room(room, db)
        return {'status': {
            'success': True,
        }}


def resolve_rooms(*_, room_id: Optional[int] = None):
    with get_session() as db:
        if room_id:
            return {'rooms': [RoomsGateway.get_by_id(room_id, db)], 'status': {
                'success': True,
            }}
        return {'rooms': RoomsGateway.get_all(db), 'status': {
            'success': True,
        }}
