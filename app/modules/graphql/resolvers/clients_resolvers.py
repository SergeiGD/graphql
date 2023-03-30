from typing import Optional
from ...models.users import Client
from ...models.base import db
from ...managers.clients_manager import ClientsManager
from ..utils import return_validation_error, return_not_found_error, update_fields


def resolve_create_client(*_, input: dict):
    try:
        client = Client(**input)
        ClientsManager.save_client(client)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'client': client, 'status': {
        'success': True,
    }}


def resolve_update_client(*_, id: int, input: dict):
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


def resolve_clients(*_, client_id: Optional[int] = None):
    if client_id:
        return db.session.query(Client).filter_by(id=client_id, date_deleted=None)
    return db.session.query(Client).filter_by(date_deleted=None)
