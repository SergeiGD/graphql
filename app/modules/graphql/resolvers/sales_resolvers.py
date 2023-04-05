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


def resolve_sales(*_, filter: dict):
    try:
        sales, pages_count = SalesManager.filter(filter)
    except ValueError as filter_error:
        return return_validation_error(filter_error)
    return {'sales': sales, 'pages_count': pages_count, 'status': {
        'success': True,
    }}

