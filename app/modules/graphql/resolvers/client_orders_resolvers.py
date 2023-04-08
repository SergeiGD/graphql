from typing import Optional
from ...models.orders import Order
from ...models.base import db
from ...managers.orders_manager import OrdersManager
from ..utils import return_validation_error, return_not_found_error, update_fields, token_required, permission_required


@token_required
def resolve_cancel_client_order(*_, id: int, current_user):
    order: Order = db.session.query(Order).filter(
        Order.id == id,
        Order.date_canceled == None,
        Order.client_id == current_user.id,
    ).first()
    if order is None:
        return return_not_found_error(Order.REPR_MODEL_NAME)
    OrdersManager.mark_as_canceled(order)
    return {'order': order, 'status': {
        'success': True,
    }}


@token_required
def resolve_client_profile_orders(*_, order_id: Optional[int] = None, current_user):
    if order_id:
        order = db.session.query(Order).filter_by(id=order_id, client_id=current_user.id)
        return {'orders': order, 'status': {
            'success': True,
        }}
    orders = db.session.query(Order).filter_by(client_id=current_user.id)
    return {'orders': orders, 'status': {
        'success': True,
    }}


@token_required
def resolve_client_pay_order(*_, id: int, current_user):
    order = db.session.query(Order).filter(
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
    OrdersManager.mark_as_paid(order)
    return {'order': order, 'status': {
        'success': True,
    }}


@token_required
def resolve_profile_info(*_, current_user):
    return {'user': current_user, 'status': {
        'success': True,
    }}
