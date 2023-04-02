from flask import current_app
from datetime import datetime, timedelta
from ...settings import settings
import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError
from ..utils import return_validation_error, return_not_found_error
from ...models.users import Client, User
from ...models.base import db
from ...models.tokens import Token, TokenType
from ...managers.users_manager import UsersManager


def resolve_login(*_, login: str, password: str):
    try:
        user = UsersManager.authenticate_user(login, password)
    except ValueError as validation_error:
        return return_validation_error(validation_error)

    access_token = jwt.encode({
        'id': user.id,
        'exp': datetime.now(tz=settings.TIMEZONE) + timedelta(minutes=30),
        'is_refresh_token': False,
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

    refresh_token = jwt.encode({
        'id': user.id,
        'exp': datetime.now(tz=settings.TIMEZONE) + timedelta(days=7),
        'is_refresh_token': True,
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

    return {
        'tokens': {
            'access_token': access_token,
            'refresh_token': refresh_token,
        },
        'status': {
            'success': True,
        }
    }


def resolve_sing_up(*_, input: dict):
    try:
        user, token = UsersManager.register_user(Client(**input))
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'user': user, 'token': token,  'status': {
        'success': True,
    }}


def resolve_account_confirm(*_, token: str):
    register_token = UsersManager.check_token(token, TokenType.register)
    if register_token is None:
        return {'status': {
            'success': False,
            'error': 'Не найден активный токен с таким значением'
        }}
    UsersManager.confirm_account(register_token)
    return {'user': register_token.user, 'status': {
        'success': True,
    }}


def resolve_request_reset(*_, email: str):
    user = db.session.query(User).filter(
        User.email == email,
        User.is_confirmed == True,
    ).first()
    # проверяем есть ли такой пользователь
    if user is None:
        return {'status': {
            'success': False,
            'error': 'Не активный пользователь с такой эл. почтой'
        }}
    user, token = UsersManager.request_reset(user)
    return {'user': user, 'token': token, 'status': {
        'success': True,
    }}


def resolve_reset_confirm(*_, token: str, password: str):
    reset_token = UsersManager.check_token(token, TokenType.reset)
    if reset_token is None:
        return {'status': {
            'success': False,
            'error': 'Не найден активный токен с таким значением'
        }}
    UsersManager.confirm_reset(reset_token, password)
    return {'user': reset_token.user, 'status': {
        'success': True,
    }}


def resolve_refresh(*_, refresh_token: str):
    if refresh_token is None:
        return {'status': {
            'success': False,
            'error': f'Токен обновления не был предоставлен',
        }}
    try:
        payload = jwt.decode(refresh_token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    except (DecodeError, ExpiredSignatureError):
        return {'status': {
            'success': False,
            'error': f'Недействительный токен обновления',
        }}

    # TODO вот тут же проверку, не забанен ли токен
    if not payload['is_refresh_token']:
        return {'status': {
            'success': False,
            'error': f'Недействительный токен обновления',
        }}

    access_token = jwt.encode({
        'id': payload['id'],
        'exp': datetime.now(tz=settings.TIMEZONE) + timedelta(minutes=30),
        'is_refresh_token': False,
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

    refresh_token = jwt.encode({
        'id': payload['id'],
        'exp': datetime.now(tz=settings.TIMEZONE) + timedelta(days=7),
        'is_refresh_token': True,
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

    return {
        'tokens': {
            'access_token': access_token,
            'refresh_token': refresh_token,
        },
        'status': {
            'success': True,
        }
    }





