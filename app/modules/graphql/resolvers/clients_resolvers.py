from typing import Optional
from ...models.users import Client
from ...models.base import db
from ...managers.clients_manager import ClientsManager
from ..utils import return_validation_error, return_not_found_error, update_fields, token_required, permission_required


@token_required
@permission_required(permissions=['add_client'])
def resolve_create_client(*_, input: dict, current_user):
    try:
        client = Client(**input)
        ClientsManager.save_client(client)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'client': client, 'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['edit_client'])
def resolve_update_client(*_, id: int, input: dict, current_user):
    client: Client = db.session.query(Client).filter(
        Client.id == id,
        Client.date_deleted == None
    ).first()
    if client is None:
        return return_not_found_error(Client.REPR_MODEL_NAME)
    try:
        update_fields(client, input)
        ClientsManager.save_client(client)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'client': client, 'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['show_client'])
def resolve_clients(*_, client_id: Optional[int] = None, current_user):
    if client_id:
        client = db.session.query(Client).filter_by(id=client_id, date_deleted=None)
        return {'clients': client, 'status': {
            'success': True,
        }}
    clients = db.session.query(Client).filter_by(date_deleted=None).all()
    return {'clients': clients, 'status': {
        'success': True,
    }}
