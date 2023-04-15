from typing import Optional
from ...models.orders import Purchase
from ...models.categories import Category
from ...models.orders import Cart
from ...db_gateways.purchase_gateway import PurchasesGateway
from ...db_gateways.categories_gateway import CategoriesGateway
from ...db_gateways.carts_gateway import CartsGateway
from ..utils import return_validation_error, return_not_found_error, update_fields, permission_required, token_required
from ...session.session import get_session


@token_required
@permission_required(permissions=['add_purchase'])
def resolve_create_purchase(*_, input: dict, current_user):
    with get_session() as db:
        category: Category = CategoriesGateway.get_by_id(input['category_id'], db)
        if category is None:
            return return_not_found_error(Category.REPR_MODEL_NAME)
        try:
            args = {attr: val for attr, val in input.items() if attr != 'category_id'}
            purchase = Purchase(**args)
            PurchasesGateway.save_purchase(purchase=purchase, category=category, db=db)
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'purchase': purchase, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['edit_purchase'])
def resolve_update_purchase(*_, id: int, input: dict, current_user):
    with get_session() as db:
        purchase: Purchase = PurchasesGateway.get_by_id(id, db)
        if purchase is None:
            return return_not_found_error(Purchase.REPR_MODEL_NAME)
        try:
            update_fields(purchase, input)
            PurchasesGateway.save_purchase(purchase, db)
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'purchase': purchase, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['cancel_purchase'])
def resolve_cancel_purchase(*_, id: int, current_user):
    with get_session() as db:
        purchase: Purchase = PurchasesGateway.get_by_id(id, db)
        if purchase is None:
            return return_not_found_error(Purchase.REPR_MODEL_NAME)
        PurchasesGateway.mark_as_canceled(purchase, db)
        return {'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['show_purchase'])
def resolve_purchases(*_, purchase_id: Optional[int] = None, current_user):
    with get_session() as db:
        if purchase_id:
            return {'purchases': [PurchasesGateway.get_by_id(purchase_id, db)], 'status': {
                'success': True,
            }}
        return {'purchases': PurchasesGateway.get_all(db), 'status': {
            'success': True,
        }}


def resolve_purchase_order(obj: Purchase, *args):
    # если заказ - корзина, то не проверяем права
    if isinstance(obj.order, Cart):
        return {'order': obj.order, 'status': {
            'success': True,
        }}
    else:
        # иначе пропускаем проверка прав
        @token_required
        @permission_required(permissions=['show_order'])
        def inner_resolver(obj: Purchase, *_, current_user):
            return {'order': obj.order, 'status': {
                'success': True,
            }}
        return inner_resolver(obj, *args)


def resolve_create_cart_purchase(*_, cart_uuid: str, input: dict):
    with get_session() as db:
        cart = CartsGateway.get_by_uuid(cart_uuid, db)
        if cart is None:
            return return_not_found_error(Cart.REPR_MODEL_NAME)
        category: Category = CategoriesGateway.get_by_id(input['category_id'], db)
        if category is None:
            return return_not_found_error(Category.REPR_MODEL_NAME)
        try:
            args = {attr: val for attr, val in input.items() if attr != 'category_id'}
            args['order'] = cart
            purchase = Purchase(**args)
            PurchasesGateway.save_purchase(purchase=purchase, category=category, db=db)
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'purchase': purchase, 'status': {
            'success': True,
        }}


def resolve_update_cart_purchase(*_, cart_uuid: str, id: int, input: dict):
    with get_session() as db:
        cart = CartsGateway.get_by_uuid(cart_uuid, db)
        if cart is None:
            return return_not_found_error(Cart.REPR_MODEL_NAME)
        purchase: Purchase = PurchasesGateway.get_by_id(id, db)
        if purchase is None:
            return return_not_found_error(Purchase.REPR_MODEL_NAME)

        if purchase.order_id != cart.id:
            return {'status': {
                'success': False,
                'error': 'Эта покупка не принадлежит к этой корзине'
            }}

        try:
            update_fields(purchase, input)
            PurchasesGateway.save_purchase(purchase, db)
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'purchase': purchase, 'status': {
            'success': True,
        }}


def resolve_cancel_cart_purchase(*_, cart_uuid: str, id: int):
    with get_session() as db:
        cart = CartsGateway.get_by_uuid(cart_uuid, db)
        if cart is None:
            return return_not_found_error(Cart.REPR_MODEL_NAME)

        purchase: Purchase = PurchasesGateway.get_by_id(id, db)
        if purchase is None:
            return return_not_found_error(Purchase.REPR_MODEL_NAME)

        if purchase.order_id != cart.id:
            return {'status': {
                'success': False,
                'error': 'Эта покупка не принадлежит к этой корзине'
            }}
        if purchase is None:
            return return_not_found_error(Purchase.REPR_MODEL_NAME)

        PurchasesGateway.mark_as_canceled(purchase, db)
        return {'status': {
            'success': True,
        }}
