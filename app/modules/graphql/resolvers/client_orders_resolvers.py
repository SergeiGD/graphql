from typing import Optional
from ...models.orders import Order
from ...db_gateways.orders_gateway import OrdersGateway
from ...db_gateways.clients_gateway import ClientsGateway
from ..utils import return_not_found_error, token_required
from ...session.session import get_session


@token_required
def resolve_cancel_client_order(*_, id: int, current_user):
    with get_session() as db:
        order: Order = db.query(Order).filter(
            Order.id == id,
            Order.date_canceled == None,
            Order.client_id == current_user.id,
        ).first()
        if order is None:
            return return_not_found_error(Order.REPR_MODEL_NAME)
        OrdersGateway.mark_as_canceled(order, db)
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
def resolve_client_pay_order(*_, id: int, current_user):
    with get_session() as db:
        order = db.query(Order).filter(
            Order.id == id,
            Order.client_id == current_user.id,
            Order.date_canceled == None,
            Order.date_finished == None,
            Order.date_full_paid == None,
        ).first()
        if order is None:
            return {'status': {
                'success': False,
                'error': ' Не найден активный неоплаченный заказ с таким id'
            }}
        OrdersGateway.mark_as_paid(order, db)
        return {'order': order, 'status': {
            'success': True,
        }}


@token_required
def resolve_profile_info(*_, current_user):
    return {'user': current_user, 'status': {
        'success': True,
    }}
