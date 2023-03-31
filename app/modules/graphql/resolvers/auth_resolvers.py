from flask import current_app
from datetime import datetime, timedelta
from ...settings import settings
import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError
from ariadne.types import GraphQLResolveInfo
from ..utils import return_validation_error
from ...models.users import Client
from ...managers.users_manager import UsersManager
from ...managers.clients_manager import ClientsManager


def resolve_login(*_, login: str, password: str):
    try:
        user = UsersManager.check_password(login, password)
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
        client = ClientsManager.register_client(Client(**input))
    except ValueError as validation_error:
        return return_validation_error(validation_error)
    return {'client': client, 'status': {
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





