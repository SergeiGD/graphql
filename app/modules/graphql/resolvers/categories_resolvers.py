from typing import Optional
from datetime import date
from ...models.categories import Category
from ...models.tags import Tag
from ...models.sales import Sale
from ...models.base import db
from ...managers.categories_manager import CategoriesManager
from ..utils import return_validation_error, return_not_found_error, update_fields, token_required, permission_required
from werkzeug.datastructures import FileStorage


@token_required
@permission_required(permissions=['add_category'])
def resolve_create_category(*_, input: dict, file: FileStorage, current_user):
    try:
        category = Category(**input)
        CategoriesManager.save_category(category, file)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'category': category, 'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['edit_category'])
def resolve_update_category(*_, id: int, input: dict, file: Optional[FileStorage] = None, current_user):
    category: Category = db.session.query(Category).filter(
        Category.id == id
    ).first()
    if category is None:
        return return_not_found_error(Category.REPR_MODEL_NAME)
    try:
        update_fields(category, input)
        CategoriesManager.save_category(category, file)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'category': category, 'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['delete_category'])
def resolve_delete_category(*_, id: int, current_user):
    category: Category = db.session.query(Category).filter(
        Category.id == id,
        Category.date_deleted == None,
    ).first()
    if category is None:
        return return_not_found_error(Category.REPR_MODEL_NAME)
    CategoriesManager.delete_category(category)
    return {'status': {
        'success': True,
    }}


def resolve_categories(*_, filter: dict):
    try:
        categories, pages_count = CategoriesManager.filter(filter)
    except ValueError as filter_error:
        return return_validation_error(filter_error)
    return {'categories': categories, 'pages_count': pages_count, 'status': {
        'success': True,
    }}


def resolve_category_familiar(obj: Category, *_):
    return CategoriesManager.get_familiar(obj)


def resolve_category_busy_dates(obj: Category, _, date_start: date, date_end: date):
    if (date_end - date_start).days > 31:
        return {'status': {
            'success': False,
            'error': 'нельзя запросить больше 31 дня'
        }}
    return {'dates': CategoriesManager.get_busy_dates(obj, date_start, date_end), 'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['edit_category', 'edit_tag'])
def resolve_add_tag_to_category(*_, tag_id: int, category_id: int, current_user):
    tag: Tag = db.session.query(Tag).filter(
        Tag.id == tag_id
    ).first()
    if tag is None:
        return return_not_found_error(Tag.REPR_MODEL_NAME)
    category: Category = db.session.query(Category).filter(
        Category.id == category_id,
        Category.date_deleted == None
    ).first()
    if category is None:
        return return_not_found_error(Category.REPR_MODEL_NAME)
    CategoriesManager.add_tag_to_category(category, tag)
    return {'tag': tag, 'category': category, 'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['edit_category', 'edit_tag'])
def resolve_remove_tag_from_category(*_, tag_id: int, category_id: int, current_user):
    tag: Tag = db.session.query(Tag).filter(
        Tag.id == tag_id
    ).first()
    if tag is None:
        return return_not_found_error(Tag.REPR_MODEL_NAME)
    category: Category = db.session.query(Category).filter(
        Category.id == category_id,
        Category.date_deleted == None
    ).first()
    if category is None:
        return return_not_found_error(Category.REPR_MODEL_NAME)
    CategoriesManager.remove_tag_from_category(category, tag)
    return {'tag': tag, 'category': category, 'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['edit_category', 'edit_sale'])
def resolve_add_sale_to_category(*_, sale_id: int, category_id: int, current_user):
    sale: Sale = db.session.query(Sale).filter(
        Sale.id == sale_id,
        Sale.date_deleted == None,
    ).first()
    if sale is None:
        return return_not_found_error(Sale.REPR_MODEL_NAME)
    category: Category = db.session.query(Category).filter(
        Category.id == category_id,
        Category.date_deleted == None
    ).first()
    if category is None:
        return return_not_found_error(Category.REPR_MODEL_NAME)
    CategoriesManager.add_sale_to_category(category, sale)
    return {'tag': tag, 'category': category, 'status': {
        'success': True,
    }}


@token_required
@permission_required(permissions=['edit_category', 'edit_sale'])
def resolve_remove_sale_from_category(*_, sale_id: int, category_id: int, current_user):
    sale: Sale = db.session.query(Sale).filter(
        Sale.id == sale_id,
        Sale.date_deleted == None,
    ).first()
    if sale is None:
        return return_not_found_error(Sale.REPR_MODEL_NAME)
    category: Category = db.session.query(Category).filter(
        Category.id == category_id,
        Category.date_deleted == None
    ).first()
    if category is None:
        return return_not_found_error(Category.REPR_MODEL_NAME)
    CategoriesManager.remove_sale_to_category(category, sale)
    return {'sale': sale, 'category': category, 'status': {
        'success': True,
    }}
