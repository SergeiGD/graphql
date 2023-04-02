from typing import Optional
from ...models.orders import Purchase
from ...models.categories import Category
from ...models.orders import Cart
from ...models.base import db
from ...managers.purchase_manager import PurchasesManager
from ..utils import return_validation_error, return_not_found_error, update_fields, permission_required, token_required


@token_required
@permission_required(permissions=['add_purchase'])
def resolve_create_purchase(*_, input: dict, current_user):
    category: Category = db.session.query(Category).get(input['category_id'])
    if category is None:
        return return_not_found_error(Category.REPR_MODEL_NAME)
    try:
        args = {attr: val for attr, val in input.items() if attr != 'category_id'}
        purchase = Purchase(**args)
        PurchasesManager.save_purchase(purchase=purchase, category=category)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'purchase': purchase, 'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['edit_purchase'])
def resolve_update_purchase(*_, id: int, input: dict, current_user):
    purchase: Purchase = db.session.query(Purchase).filter(
        Purchase.id == id,
        Purchase.is_canceled == False,
    ).first()
    if purchase is None:
        return return_not_found_error(Purchase.REPR_MODEL_NAME)
    try:
        update_fields(purchase, input)
        PurchasesManager.save_purchase(purchase)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'purchase': purchase, 'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['cancel_purchase'])
def resolve_cancel_purchase(*_, id: int, current_user):
    purchase: Purchase = db.session.query(Purchase).filter(
        Purchase.id == id,
        Purchase.is_canceled == False,
    ).first()
    if purchase is None:
        return return_not_found_error(Purchase.REPR_MODEL_NAME)
    PurchasesManager.mark_as_canceled(purchase)
    return {'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['show_purchase'])
def resolve_purchases(*_, purchase_id: Optional[int] = None, current_user):
    if purchase_id:
        purchase = db.session.query(Purchase).filter_by(id=purchase_id)
        return {'purchases': purchase, 'status': {
            'success': True,
        }}
    purchases = db.session.query(Purchase).all()
    return {'purchases': purchases, 'status': {
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
    cart = db.session.query(Cart).filter_by(cart_uuid=cart_uuid).first()
    if cart is None:
        return return_not_found_error(Cart.REPR_MODEL_NAME)
    category: Category = db.session.query(Category).get(input['category_id'])
    if category is None:
        return return_not_found_error(Category.REPR_MODEL_NAME)
    try:
        args = {attr: val for attr, val in input.items() if attr != 'category_id'}
        args['order'] = cart
        purchase = Purchase(**args)
        PurchasesManager.save_purchase(purchase=purchase, category=category)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'purchase': purchase, 'status': {
        'success': True,
    }}


def resolve_update_cart_purchase(*_, cart_uuid: str, id: int, input: dict):
    cart = db.session.query(Cart).filter_by(cart_uuid=cart_uuid).first()
    if cart is None:
        return return_not_found_error(Cart.REPR_MODEL_NAME)

    purchase: Purchase = db.session.query(Purchase).filter(
        Purchase.id == id,
    ).first()
    if purchase is None:
        return return_not_found_error(Purchase.REPR_MODEL_NAME)

    if purchase.order_id != cart.id:
        return {'status': {
            'success': False,
            'error': 'Эта покупка не принадлежит к этой корзине'
        }}

    try:
        update_fields(purchase, input)
        PurchasesManager.save_purchase(purchase)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'purchase': purchase, 'status': {
        'success': True,
    }}


def resolve_cancel_cart_purchase(*_, cart_uuid: str, id: int):
    cart = db.session.query(Cart).filter_by(cart_uuid=cart_uuid).first()
    if cart is None:
        return return_not_found_error(Cart.REPR_MODEL_NAME)

    purchase: Purchase = db.session.query(Purchase).filter(
        Purchase.id == id,
    ).first()
    if purchase is None:
        return return_not_found_error(Purchase.REPR_MODEL_NAME)

    if purchase.order_id != cart.id:
        return {'status': {
            'success': False,
            'error': 'Эта покупка не принадлежит к этой корзине'
        }}
    if purchase is None:
        return return_not_found_error(Purchase.REPR_MODEL_NAME)

    PurchasesManager.mark_as_canceled(purchase)
    return {'status': {
        'success': True,
    }}
