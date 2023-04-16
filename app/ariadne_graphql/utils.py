from typing import Any, List
from functools import wraps
import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError
from hotel_business.gateways.users_gateway import UsersGateway
from hotel_business.settings import settings
from hotel_business.session.session import get_session


def return_validation_error(validation_error: Exception):
    """
    Возврат ошибок валидации при сохранении сущности
    :param validation_error: полученные ошибки
    :return:
    """
    return {'status': {
        'success': False,
        'error': str(validation_error),
    }}


def return_not_found_error(model_name: str):
    """
    Возврат ошибки, если сушность не найдена
    :param model_name: понятное пользователю название модели
    :return:
    """
    return {'status': {
        'success': False,
        'error': f'Не найден(а) актин(ый/ая) {model_name} с таким id',
    }}


def update_fields(obj: Any, data: dict):
    """
    Автоматическое обновление полей модели, с помощью данных, полученных от инпута мутации
    :param obj: объект, который нужно обновить
    :param data: данные из инпута мутации
    :return:
    """
    for attr, value in data.items():
        setattr(obj, attr, value)


def token_required(f):
    """
    Докератор для резольверов для проверка авторизации (токена) и получения текущего авторизованного пользователя
    :param f:
    :return:
    """
    @wraps(f)
    def decorated_token(*args, **kwargs):
        info = args[1]  # втором аргументом резольверу всегда приходит информация о запросе
        request = info.context['request']  # получаем реквест
        auth_header = request.headers.get('Authorization', '')  # получаем значения в заголовке Authorization
        keys = auth_header.split()  # т.к. это будет строка вида Bearer token, приводим ее к списку для удобства

        # проверяем в правильном ли формате пришел заголовок
        if len(keys) < 2 or keys[0] != 'Bearer':
            return {'status': {
                'success': False,
                'error': f'Отсутствует или имеет неверный формат токен доступа (заголовок Authorization, ключ Bearer)',
            }}
        try:
            # вторым элементов у нас лежит сам токен
            token = keys[1]
            # пытаемся декодировать токен
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except (DecodeError, ExpiredSignatureError):
            return {'status': {
                'success': False,
                'error': f'Недействительный токен доступа',
            }}

        # проверяем, что пришел access, а не refresh токен
        if payload['is_refresh_token']:
            return {'status': {
                'success': False,
                'error': f'Недействительный токен доступа',
            }}

        with get_session() as db:
            # получаем пользователя из payload'а токена
            current_user = UsersGateway.get_by_id(payload['id'], db)
        # пихаем полученного пользователя в аргументы резольвера
        kwargs['current_user'] = current_user
        return f(*args, **kwargs)

    return decorated_token


def permission_required(permissions: List[str]):
    """
    Докератор для резольверов для проверки прав пользователя
    :param permissions: список необходимых для доступа прав
    :return:
    """
    def inner(f):
        @wraps(f)
        def check_permissions(*args, **kwargs):

            user = kwargs.get('current_user', None)
            if user is None:
                return {'status': {
                    'success': False,
                    'error': f'Для доступа к этой секции необходимо быть авторизированным пользователем',
                }}

            with get_session() as db:
                if UsersGateway.can_actions(user, permissions, db):
                    return f(*args, **kwargs)

            return {'status': {
                'success': False,
                'error': f'У Вас нету разрешений для доступа к этой секции',
            }}

        return check_permissions
    return inner
