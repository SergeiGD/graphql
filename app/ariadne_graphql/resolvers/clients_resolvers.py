from typing import Optional
from hotel_business_module.models.users import Client
from hotel_business_module.gateways.clients_gateway import ClientsGateway
from ..utils import return_validation_error, return_not_found_error, update_fields, token_required, permission_required
from hotel_business_module.session.session import get_session


@token_required
@permission_required(permissions=['add_client'])
def resolve_create_client(*_, input: dict, current_user):
    with get_session() as db:
        try:
            client = Client(**input)
            ClientsGateway.save_client(client, db)
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'client': client, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['edit_client'])
def resolve_update_client(*_, id: int, input: dict, current_user):
    with get_session() as db:
        client: Client = ClientsGateway.get_by_id(id, db)
        if client is None:
            return return_not_found_error(Client.REPR_MODEL_NAME)
        try:
            update_fields(client, input)
            ClientsGateway.save_client(client, db)
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'client': client, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['delete_client'])
def resolve_delete_client(*_, id: int, current_user):
    with get_session() as db:
        client: Client = ClientsGateway.get_by_id(id, db)
        if client is None:
            return return_not_found_error(Client.REPR_MODEL_NAME)
        ClientsGateway.delete_client(client, db)
        return {'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['show_client'])
def resolve_clients(*_, client_id: Optional[int] = None, current_user):
    with get_session() as db:
        if client_id:
            return {'clients': [ClientsGateway.get_by_id(client_id, db)], 'status': {
                'success': True,
            }}
        return {'clients': ClientsGateway.get_all(db), 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['show_order'])
def resolve_client_orders(obj: Client, *_, current_user):
    return {'orders': obj.orders, 'status': {
        'success': True,
    }}
