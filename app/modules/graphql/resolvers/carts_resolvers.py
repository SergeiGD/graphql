from ...models.orders import Cart
from ...models.base import db
from ...managers.carts_manager import CartsManger
from ..utils import return_validation_error, return_not_found_error


def resolve_create_cart(*_):
    try:
        cart = Cart()
        CartsManger.save_cart(cart)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return cart


def resolve_cart(*_, cart_uuid: str):
    cart = db.session.query(Cart).filter_by(cart_uuid=cart_uuid).first()
    if cart is None:
        return return_not_found_error(Cart.REPR_MODEL_NAME)
    return {'cart': cart, 'status': {
        'success': True,
    }}


def resolve_confirm_cart(*_, cart_uuid: str, email: str, is_fully_paid: bool = False):
    cart = db.session.query(Cart).filter_by(cart_uuid=cart_uuid).first()
    if cart is None:
        return return_not_found_error(Cart.REPR_MODEL_NAME)
    if len(cart.purchases) == 0:
        return {'status': {
            'success': False,
            'error': 'Нельзя подтврдить корзину, в которой нету покупок'
        }}
    try:
        order = CartsManger.confirm_cart(cart, email, is_fully_paid=is_fully_paid)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'order': order, 'status': {
        'success': True,
    }}

