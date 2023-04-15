from typing import Optional
from ...models.orders import Order
from ...db_gateways.orders_gateway import OrdersGateway
from ..utils import return_validation_error, return_not_found_error, update_fields, token_required, permission_required
from ...session.session import get_session


@token_required
@permission_required(permissions=['add_order'])
def resolve_create_order(*_, input: dict, current_user):
    with get_session() as db:
        try:
            order = Order(**input)
            OrdersGateway.save_order(order, db)
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'order': order, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['edit_order'])
def resolve_update_order(*_, id: int, input: dict, current_user):
    with get_session() as db:
        order: Order = OrdersGateway.get_by_id(id, db)
        if order is None:
            return return_not_found_error(Order.REPR_MODEL_NAME)
        try:
            update_fields(order, input)
            OrdersGateway.save_order(order, db)
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'order': order, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['cancel_order'])
def resolve_cancel_order(*_, id: int, current_user):
    with get_session() as db:
        order: Order = OrdersGateway.get_by_id(id, db)
        if order is None:
            return return_not_found_error(Order.REPR_MODEL_NAME)
        OrdersGateway.mark_as_canceled(order, db)
        return {'order': order, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['show_order'])
def resolve_orders(*_, order_id: Optional[int] = None, current_user):
    with get_session() as db:
        if order_id:
            return {'orders': [OrdersGateway.get_by_id(order_id, db)], 'status': {
                'success': True,
            }}
        return {'orders': OrdersGateway.get_all(db), 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['show_purchase'])
def resolve_order_purchases(obj: Order, *_, current_user):
    return {'purchases': obj.purchases, 'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['show_purchase'])
def resolve_order_client(obj: Order, *_, current_user):
    return {'client': obj.client, 'status': {
        'success': True,
    }}
