from os import environ
from typing import Optional, Any
from datetime import date, datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from ariadne import gql, QueryType, make_executable_schema, ObjectType, graphql_sync, MutationType, ScalarType
from ariadne.types import GraphQLResolveInfo
from ariadne.asgi import GraphQL
from ariadne.explorer import ExplorerGraphiQL
from flask import Flask, jsonify, request
from modules.models.base import db

# from modules.models.base import Base
from modules.models.tags import Tag
from modules.models.categories import Category
from modules.models.photos import Photo
from modules.models.rooms import Room
from modules.models.orders import Order, Purchase
from modules.models.users import Client, User
from modules.graphql.schema import type_defs
from modules.models.types_protocols import SupportsId, SupportsName
from modules.managers.photos_manager import PhotosManager
from modules.managers.orders_manager import PurchasesManager, OrdersManager
from modules.managers.categories_manager import CategoriesManager
from modules.managers.photos_manager import PhotosManager
from modules.managers.rooms_manager import RoomsManager
from modules.managers.tags_manager import TagsManager

# TODO: индексы прокинуть
# TODO: cron для очищения корзины и заказов
# TODO: ключи индепотентности
# TODO: права
# TODO: ресольверы в отдельную папку
# TODO: dataclasses

query = QueryType()
mutation = MutationType()
tag = ObjectType('Tag')
category = ObjectType('Category')
room = ObjectType('Room')
photo = ObjectType('Photo')
datetime_scalar = ScalarType('Datetime')
date_scalar = ScalarType('Date')


@datetime_scalar.serializer
def serialize_datetime(value: datetime):
    return value.isoformat()


@datetime_scalar.value_parser
def parse_datetime_value(value: str):
    try:
        return datetime.fromisoformat(value)
    except (ValueError, TypeError):
        raise ValueError(f'"{value}" is not a valid ISO 8601 string')


@date_scalar.serializer
def serialize_date(value: date):
    return value.isoformat()


@date_scalar.value_parser
def parse_date_value(value: str):
    try:
        return date.fromisoformat(value)
    except (ValueError, TypeError):
        raise ValueError(f'"{value}" is not a valid ISO 8601 string')


def return_validation_error(validation_error: Exception):
    return {'status': {
        'success': False,
        'error': str(validation_error),
    }}


def return_not_found_error(model_name: str):
    return {'status': {
        'success': False,
        'error': f'Не найден(а) {model_name} с таким id',
    }}


def update_fields(obj: Any, data: dict):
    for attr, value in data.items():
        setattr(obj, attr, value)


@mutation.field('createRoom')
def resolve_create_room(*_, input: dict):
    try:
        room = Room(**input)
        RoomsManager.save_room(room)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'room': room, 'status': {
        'success': True,
    }}


@mutation.field('updateRoom')
def resolve_update_room(*_, id: int, input: dict):
    room: Room = db.session.query(Room).filter(
        Room.id == id,
        Room.date_deleted == None
    ).first()
    if room is None:
        return return_not_found_error(Room.REPR_MODEL_NAME)
    try:
        update_fields(room, input)
        RoomsManager.save_room(room)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'room': room, 'status': {
        'success': True,
    }}


@mutation.field('createPhoto')
def resolve_create_photo(*_, input: dict):
    try:
        photo = Photo(**input)
        PhotosManager.save_photo(photo)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'photo': photo, 'status': {
        'success': True,
    }}


@mutation.field('updatePhoto')
def resolve_update_photo(*_, id: int, input: dict):
    photo: Photo = db.session.query(Photo).filter(
        Photo.id == id
    ).first()
    if photo is None:
        return return_not_found_error(Photo.REPR_MODEL_NAME)
    try:
        update_fields(photo, input)
        PhotosManager.save_photo(photo)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'photo': photo, 'status': {
        'success': True,
    }}


@mutation.field('createCategory')
def resolve_create_category(*_, input: dict):
    try:
        category = Category(**input)
        CategoriesManager.save_category(category)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'category': category, 'status': {
        'success': True,
    }}


@mutation.field('updateCategory')
def resolve_update_category(*_, id: int, input: dict):
    category: Category = db.session.query(Category).filter(
        Category.id == id
    ).first()
    if category is None:
        return return_not_found_error(Category.REPR_MODEL_NAME)
    try:
        update_fields(category, input)
        CategoriesManager.save_category(category)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'category': category, 'status': {
        'success': True,
    }}


@mutation.field('createTag')
def resolve_create_tag(*_, input: dict):
    try:
        tag = Tag(**input)
        TagsManager.save_tag(tag)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'tag': tag, 'status': {
        'success': True,
    }}


@mutation.field('updateTag')
def resolve_update_tag(*_, id: int, input: dict):
    tag: Tag = db.session.query(Tag).filter(
        Tag.id == id
    ).first()
    if tag is None:
        return return_not_found_error(Tag.REPR_MODEL_NAME)
    try:
        update_fields(tag, input)
        TagsManager.save_tag(tag)
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'tag': tag, 'status': {
        'success': True,
    }}


@mutation.field('addTagToCategory')
def resolve_add_tag_to_category(*_, tag_id: int, category_id: int):
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


@query.field('tags')
def resolve_tags(*_, tag_id: Optional[int] = None):
    if tag_id:
        return db.session.query(Tag).filter_by(id=tag_id)
    return db.session.query(Tag).all()


@query.field('categories')
def resolve_categories(*_, cat_id: Optional[int] = None):
    # TODO: ВО ТУТ ПРОВЕРКА ПРАВ?
    if cat_id:
        return db.session.query(Category).filter_by(id=cat_id, date_deleted=None)
    return db.session.query(Category).filter_by(date_deleted=None)


@query.field('rooms')
def resolve_rooms(*_, room_id: Optional[int] = None):
    if room_id:
        return db.session.query(Room).filter_by(id=room_id, date_deleted=None)
    return db.session.query(Room).filter_by(date_deleted=None)


@query.field('photos')
def resolve_photos(*_, photo_id: Optional[int] = None):
    if photo_id:
        return db.session.query(Photo).filter_by(id=photo_id)
    return db.session.query(Photo).all()


checked_types = gql(type_defs)
schema = make_executable_schema(
    checked_types,
    [query, mutation, tag, category, room, photo, date_scalar, datetime_scalar],
    convert_names_case=True
)
explorer_html = ExplorerGraphiQL().html(None)
app = Flask(__name__)


@app.route("/graphql", methods=["GET"])
def graphql_explorer():
    return explorer_html, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value={"request": request},
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    db_name = environ.get('DB_NAME', 'db_graphql')
    db_user = environ.get('DB_USER', 'db_user')
    db_password = environ.get('DB_PASSWORD', 'db_password')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{db_user}:{db_password}@db/{db_name}'
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')



