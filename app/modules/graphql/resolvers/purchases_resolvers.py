from typing import Optional
from ...models.orders import Purchase
from ...models.categories import Category
from ...models.base import db
from ...managers.purchase_manager import PurchasesManager
from ..utils import return_validation_error, return_not_found_error, update_fields


def resolve_create_purchase(*_, input: dict):
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


def resolve_update_purchase(*_, id: int, input: dict):
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


def resolve_cancel_purchase(*_, id: int):
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


def resolve_purchases(*_, purchase_id: Optional[int] = None):
    if purchase_id:
        return db.session.query(Purchase).filter_by(id=purchase_id)
    return db.session.query(Purchase).all()
