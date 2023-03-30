from typing import Optional
from ...models.orders import Order
from ...models.base import db
from ...managers.orders_manager import OrdersManager
from ..utils import return_validation_error, return_not_found_error, update_fields


def resolve_create_order(*_, input: dict):
    try:
        order = Order(**input)
        OrdersManager.save_order(order)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'order': order, 'status': {
        'success': True,
    }}


def resolve_update_order(*_, id: int, input: dict):
    order: Order = db.session.query(Order).filter(
        Order.id == id,
        Order.date_canceled == None,
    ).first()
    if order is None:
        return return_not_found_error(Order.REPR_MODEL_NAME)
    try:
        update_fields(order, input)
        OrdersManager.save_order(order)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'order': order, 'status': {
        'success': True,
    }}


def resolve_cancel_order(*_, id: int):
    order: Order = db.session.query(Order).filter(
        Order.id == id,
        Order.date_canceled == None,
    ).first()
    if order is None:
        return return_not_found_error(Order.REPR_MODEL_NAME)
    OrdersManager.mark_as_canceled(order)
    return {'order': order, 'status': {
        'success': True,
    }}


def resolve_orders(*_, order_id: Optional[int] = None):
    if order_id:
        return db.session.query(Order).filter_by(id=order_id)
    return db.session.query(Order).all()


