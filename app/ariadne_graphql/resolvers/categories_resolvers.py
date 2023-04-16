from typing import Optional
from datetime import date
from hotel_business.models.categories import Category
from hotel_business.models.tags import Tag
from hotel_business.models.sales import Sale
from hotel_business.gateways.categories_gateway import CategoriesGateway
from hotel_business.gateways.tags_gateway import TagsGateway
from hotel_business.gateways.sales_gateway import SalesGateway
from ..utils import return_validation_error, return_not_found_error, update_fields, token_required, permission_required
from hotel_business.session.session import get_session
from starlette.datastructures import UploadFile


@token_required
@permission_required(permissions=['add_category'])
def resolve_create_category(*_, input: dict, file: UploadFile, current_user):
    with get_session() as db:
        try:
            category = Category(**input)
            CategoriesGateway.save_category(
                category=category,
                db=db,
                file=file.file,
                file_name=file.filename,
            )
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'category': category, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['edit_category'])
def resolve_update_category(*_, id: int, input: dict, file: Optional[UploadFile] = None, current_user):
    with get_session() as db:
        category: Category = CategoriesGateway.get_by_id(id, db)
        if category is None:
            return return_not_found_error(Category.REPR_MODEL_NAME)
        try:
            update_fields(category, input)
            CategoriesGateway.save_category(
                category=category,
                db=db,
                file=file.file,
                file_name=file.filename,
            )
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'category': category, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['delete_category'])
def resolve_delete_category(*_, id: int, current_user):
    with get_session() as db:
        category: Category = CategoriesGateway.get_by_id(id, db)
        if category is None:
            return return_not_found_error(Category.REPR_MODEL_NAME)
        CategoriesGateway.delete_category(category, db)
        return {'status': {
            'success': True,
        }}


def resolve_categories(*_, filter: dict):
    with get_session() as db:
        try:
            categories, pages_count = CategoriesGateway.filter(filter, db)
        except ValueError as filter_error:
            return return_validation_error(filter_error)
        return {'categories': categories, 'pages_count': pages_count, 'status': {
            'success': True,
        }}


def resolve_category_familiar(obj: Category, *_):
    with get_session() as db:
        return CategoriesGateway.get_familiar(obj, db)


def resolve_category_busy_dates(obj: Category, _, date_start: date, date_end: date):
    with get_session() as db:
        if (date_end - date_start).days > 31:
            return {'status': {
                'success': False,
                'error': 'нельзя запросить больше 31 дня'
            }}
        return {'dates': CategoriesGateway.get_busy_dates(obj, date_start, date_end, db), 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['edit_category', 'edit_tag'])
def resolve_add_tag_to_category(*_, tag_id: int, category_id: int, current_user):
    with get_session() as db:
        tag: Tag = TagsGateway.get_by_id(tag_id, db)
        if tag is None:
            return return_not_found_error(Tag.REPR_MODEL_NAME)
        category: Category = CategoriesGateway.get_by_id(category_id, db)
        if category is None:
            return return_not_found_error(Category.REPR_MODEL_NAME)
        CategoriesGateway.add_tag_to_category(category, tag, db)
        return {'tag': tag, 'category': category, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['edit_category', 'edit_tag'])
def resolve_remove_tag_from_category(*_, tag_id: int, category_id: int, current_user):
    with get_session() as db:
        tag: Tag = TagsGateway.get_by_id(tag_id, db)
        if tag is None:
            return return_not_found_error(Tag.REPR_MODEL_NAME)
        category: Category = CategoriesGateway.get_by_id(category_id, db)
        if category is None:
            return return_not_found_error(Category.REPR_MODEL_NAME)
        CategoriesGateway.remove_tag_from_category(category, tag, db)
        return {'tag': tag, 'category': category, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['edit_category', 'edit_sale'])
def resolve_add_sale_to_category(*_, sale_id: int, category_id: int, current_user):
    with get_session() as db:
        sale: Sale = SalesGateway.get_by_id(sale_id, db)
        if sale is None:
            return return_not_found_error(Sale.REPR_MODEL_NAME)
        category: Category = CategoriesGateway.get_by_id(category_id, db)
        if category is None:
            return return_not_found_error(Category.REPR_MODEL_NAME)
        CategoriesGateway.add_sale_to_category(category, sale, db)
        return {'sale': sale, 'category': category, 'status': {
            'success': True,
        }}


@token_required
@permission_required(permissions=['edit_category', 'edit_sale'])
def resolve_remove_sale_from_category(*_, sale_id: int, category_id: int, current_user):
    with get_session() as db:
        sale: Sale = SalesGateway.get_by_id(sale_id, db)
        if sale is None:
            return return_not_found_error(Sale.REPR_MODEL_NAME)
        category: Category = CategoriesGateway.get_by_id(category_id, db)
        if category is None:
            return return_not_found_error(Category.REPR_MODEL_NAME)
        CategoriesGateway.remove_sale_to_category(category, sale, db)
        return {'sale': sale, 'category': category, 'status': {
            'success': True,
        }}
