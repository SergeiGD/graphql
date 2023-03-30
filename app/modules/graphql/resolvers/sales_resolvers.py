from typing import Optional
from ...models.sales import Sale
from ...models.base import db
from ...managers.sales_manager import SalesManager
from ..utils import return_validation_error, return_not_found_error, update_fields


def resolve_create_sale(*_, input: dict):
    try:
        sale = Sale(**input)
        SalesManager.save_sale(sale)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'sale': sale, 'status': {
        'success': True,
    }}


def resolve_update_sale(*_, id: int, input: dict):
    sale: Sale = db.session.query(Sale).filter(
        Sale.id == id
    ).first()
    if sale is None:
        return return_not_found_error(Sale.REPR_MODEL_NAME)
    try:
        update_fields(sale, input)
        SalesManager.save_sale(sale)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'sale': sale, 'status': {
        'success': True,
    }}


def resolve_delete_sale(*_, id: int):
    sale: Sale = db.session.query(Sale).filter(
        Sale.id == id,
        Sale.date_deleted == None,
    ).first()
    if sale is None:
        return return_not_found_error(Sale.REPR_MODEL_NAME)
    SalesManager.delete_sale(sale)
    return {'status': {
        'success': True,
    }}


def resolve_sales(*_, sale_id: Optional[int] = None):
    if sale_id:
        return db.session.query(Sale).filter_by(id=sale_id, date_deleted=None)
    return db.session.query(Sale).filter_by(date_deleted=None)


