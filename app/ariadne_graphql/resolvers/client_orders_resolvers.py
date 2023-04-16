from typing import Optional
from hotel_business.models.orders import Order
from hotel_business.gateways.orders_gateway import OrdersGateway
from hotel_business.gateways.clients_gateway import ClientsGateway
from ..utils import return_not_found_error, token_required, return_validation_error
from hotel_business.session.session import get_session


@token_required
def resolve_cancel_client_order(*_, id: int, current_user):
    with get_session() as db:
        order = ClientsGateway.get_client_order_by_id(current_user, id, db)
        if order is None:
            return return_not_found_error(Order.REPR_MODEL_NAME)
        OrdersGateway.mark_as_canceled(order, db)
        return {'order': order, 'status': {
            'success': True,
        }}


@token_required
def resolve_client_pay_order(*_, id: int, current_user):
    with get_session() as db:
        order = ClientsGateway.get_client_order_by_id(current_user, id, db)
        if order is None:
            return return_not_found_error(Order.REPR_MODEL_NAME)
        try:
            OrdersGateway.mark_as_paid(order, db)
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'order': order, 'status': {
            'success': True,
        }}


@token_required
def resolve_client_profile_orders(*_, order_id: Optional[int] = None, current_user):
    with get_session() as db:
        if order_id:
            return {'orders': [ClientsGateway.get_client_order_by_id(current_user, order_id, db)], 'status': {
                'success': True,
            }}
        return {'orders': ClientsGateway.get_all_client_orders(current_user, db), 'status': {
            'success': True,
        }}


@token_required
def resolve_profile_info(*_, current_user):
    return {'user': current_user, 'status': {
        'success': True,
    }}
