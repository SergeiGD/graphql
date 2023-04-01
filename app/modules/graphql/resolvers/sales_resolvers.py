from typing import Optional
from ...models.sales import Sale
from ...models.base import db
from ...managers.sales_manager import SalesManager
from ..utils import return_validation_error, return_not_found_error, update_fields, token_required, permission_required


@token_required
@permission_required(permissions=['add_sale'])
def resolve_create_sale(*_, input: dict, current_user):
    try:
        sale = Sale(**input)
        SalesManager.save_sale(sale)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'sale': sale, 'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['edit_sale'])
def resolve_update_sale(*_, id: int, input: dict, current_user):
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


@token_required
@permission_required(permissions=['delete_sale'])
def resolve_delete_sale(*_, id: int, current_user):
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
        sale = db.session.query(Sale).filter_by(id=sale_id, date_deleted=None)
        return {'sales': sale, 'status': {
            'success': True,
        }}
    sales = db.session.query(Sale).filter_by(date_deleted=None)
    return {'sales': sales, 'status': {
        'success': True,
    }}
