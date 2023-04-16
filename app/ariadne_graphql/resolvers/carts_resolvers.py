from hotel_business.models.orders import Cart
from hotel_business.gateways.carts_gateway import CartsGateway
from ..utils import return_validation_error, return_not_found_error
from hotel_business.session.session import get_session


def resolve_create_cart(*_):
    with get_session() as db:
        try:
            cart = Cart()
            CartsGateway.save_cart(cart, db)
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return cart


def resolve_cart(*_, cart_uuid: str):
    with get_session() as db:
        cart = CartsGateway.get_by_uuid(cart_uuid, db)
        if cart is None:
            return return_not_found_error(Cart.REPR_MODEL_NAME)
        return {'cart': cart, 'status': {
            'success': True,
        }}


def resolve_confirm_cart(*_, cart_uuid: str, email: str, is_fully_paid: bool = False):
    with get_session() as db:
        cart = CartsGateway.get_by_uuid(cart_uuid, db)
        if cart is None:
            return return_not_found_error(Cart.REPR_MODEL_NAME)
        if len(cart.purchases) == 0:
            return {'status': {
                'success': False,
                'error': 'Нельзя подтврдить корзину, в которой нету покупок'
            }}
        try:
            order = CartsGateway.confirm_cart(cart, email, db, is_fully_paid=is_fully_paid)
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'order': order, 'status': {
            'success': True,
        }}

