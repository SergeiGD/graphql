from typing import Optional
from hotel_business_module.models.sales import Sale
from hotel_business_module.gateways.sales_gateway import SalesGateway
from ..utils import return_validation_error, return_not_found_error, update_fields, token_required, permission_required
from hotel_business_module.session.session import get_session
from starlette.datastructures import UploadFile


@token_required
@permission_required(permissions=['add_sale'])
def resolve_create_sale(*_, input: dict, file: UploadFile, current_user):
    with get_session() as db:
        try:
            sale = Sale(**input)
            SalesGateway.save_sale(
                sale=sale,
                db=db,
                file=file.file,
                file_name=file.filename,
            )
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'sale': sale, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['edit_sale'])
def resolve_update_sale(*_, id: int, input: dict, file: Optional[UploadFile] = None, current_user):
    with get_session() as db:
        sale: Sale = SalesGateway.get_by_id(id, db)
        if sale is None:
            return return_not_found_error(Sale.REPR_MODEL_NAME)
        try:
            update_fields(sale, input)
            SalesGateway.save_sale(
                sale=sale,
                db=db,
                file=file.file,
                file_name=file.filename,
            )
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'sale': sale, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['delete_sale'])
def resolve_delete_sale(*_, id: int, current_user):
    with get_session() as db:
        sale: Sale = SalesGateway.get_by_id(id, db)
        if sale is None:
            return return_not_found_error(Sale.REPR_MODEL_NAME)
        SalesGateway.delete_sale(sale, db)
        return {'status': {
            'success': True,
        }}


def resolve_sales(*_, filter: dict):
    with get_session() as db:
        try:
            sales, pages_count = SalesGateway.filter(filter, db)
        except ValueError as filter_error:
            return return_validation_error(filter_error)
        return {'sales': sales, 'pages_count': pages_count, 'status': {
            'success': True,
        }}

