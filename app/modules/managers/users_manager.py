from typing import List
from datetime import datetime, timedelta
from ..models.base import db
from ..models.users import User
from ..models.permissions import Permission
from ..models.groups import group_permission
from ..models.users import user_group
from ..models.black_list_tokens import BlackListJWT
import bcrypt
from ..models.tokens import Token, TokenType
from ..settings import settings
from ..utils.email_sender import send_email
import jwt
import hashlib
import uuid
from jwt.exceptions import DecodeError, ExpiredSignatureError


def gen_confirm_token():
    """
    Генерация токенов для регестрации и сброса пароля
    :return:
    """
    clean_token = uuid.uuid4().hex
    hashed_token = hashlib.sha512(
        clean_token.encode('utf-8')
    ).hexdigest()
    return clean_token, hashed_token


class UsersManager:
    """
    Класс для работы с пользователями (аутентификация, сброс пароля, регистрация и т.п.)
    """
    @staticmethod
    def authenticate_user(login: str, password: str):
        """
        Аутнетификация пользоватя
        :param login: логин (почта)
        :param password: пароль (в чистом виде)
        :return:
        """
        user = db.session.query(User).filter_by(email=login).first()
        if user is None \
                or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')) \
                or not user.is_confirmed:
            raise ValueError('Активный пользователь с таким логином и паролем не найден')
        return user

    @staticmethod
    def can_actions(user: User, codes: List[str]):
        """
        Проверка, если ли у пользователя права на выполение действий
        :param user: пользователь, разрешения которого будут проверятся
        :param codes: список кодов разрешений
        :return:
        """
        if hasattr(user, 'is_superuser') and user.is_superuser:
            return True

        # получаем id разрешений пользователя
        user_permissions = db.session.query(group_permission.c.permission_id).filter(
            group_permission.c.group_id.in_(
                db.session.query(user_group.c.group_id).filter(
                    user_group.c.user_id == user.id,
                )
            )
        )

        # подзапрос, в котором получаем id необходимых разрешений
        required_permissions = db.session.query(Permission.id.label('permission_id')).filter(
            Permission.code.in_(codes),
        ).subquery('required_permissions')

        if db.session.query(
            db.session.query(required_permissions).filter(
                required_permissions.c.permission_id.not_in(user_permissions)
            ).exists()
        ).scalar():
            # если не хватет каких-то прав, то возращаем False
            return False

        return True

    @staticmethod
    def register_user(user: User):
        # проверяем есть ли зарегестрированный (с паролем) пользователь с такой эл. почтой
        if db.session.query(
            db.session.query(User).filter(
                User.email == user.email,
                User.is_confirmed == True,
            ).exists()
        ).scalar():
            raise ValueError('Пользователь с таким адресом эл. почты уже ререгестрирован')

        unregistered_user = db.session.query(User).filter(
            User.email == user.email,
            User.is_confirmed == False,
        ).first()
        if unregistered_user is not None:
            # если есть созданный, но не зарегестрированный (без пароля) клиент, то устанавливаем регестрируем его
            user = unregistered_user

        # хэшируем пароль (bcrypt сохраняет соль прямо в хэш)
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        user.password = hashed_password.decode('utf8')
        db.session.add(user)
        db.session.flush()

        clean_token, hashed_token = gen_confirm_token()
        confirm_token = Token(user=user, token_type=TokenType.register, token=hashed_token)
        db.session.add(confirm_token)
        db.session.commit()
        confirm_link = f'{settings.SITE_URL}/confirm_registration/{clean_token}'

        # отправляем письмо
        send_email(
            subject='Подтверждение регистрации',
            content=f'Для подтверждения регистрации перейдите по следующей ссылке: \n {confirm_link}',
            send_to=user.email,
        )
        return user, clean_token

    @staticmethod
    def confirm_account(token: Token):
        """
        Подтверждение аккаунта после регистрации
        :param token: токен
        :return:
        """
        db.session.add(token)
        db.session.add(token.user)
        token.user.is_confirmed = True
        # отмечаем токен как использованный
        token.is_used = True
        db.session.commit()

    @staticmethod
    def request_reset(user: User):
        """
        Запроса сброса пароля
        :param user: пользователь, которому нужно сбросить пароль
        :return:
        """
        # генерируем токены
        clean_token, hashed_token = gen_confirm_token()
        reset_token = Token(user=user, token_type=TokenType.reset, token=hashed_token)
        db.session.add(reset_token)
        db.session.commit()
        # формируем ссылку, которая будет отправена на почту
        confirm_link = f'{settings.SITE_URL}/reset_password/{clean_token}'

        # отправляем письмо
        send_email(
            subject='Сброс пароля',
            content=f'Для сброса пароля перейдите по следующей ссылке: \n {confirm_link}',
            send_to=user.email,
        )
        return user, clean_token

    @staticmethod
    def confirm_reset(token: Token, password: str):
        """
        Подтверждение сброса пароля
        :param token: токен сброса пароля
        :param password: пароль (в чистом виде)
        :return:
        """
        db.session.add(token)
        db.session.add(token.user)
        # отмечаем токен как использованный
        token.is_used = True
        # хэшируем пароль
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        token.user.password = hashed_password.decode('utf8')
        db.session.commit()

    @staticmethod
    def check_token(token: str, token_type: TokenType):
        """
        Проверка валидности токена (токен сброса пароля/регистрации)
        :param token: токен (сброса пароля/регистрации)
        :param token_type: тип токена
        :return:
        """
        try:
            hashed_token = hashlib.sha512(
                token.encode('utf-8')
            ).hexdigest()
            return db.session.query(Token).filter(
                Token.token == hashed_token,
                Token.token_type == token_type,
                Token.expires > datetime.now(tz=settings.TIMEZONE),
                Token.is_used == False,
            ).first()
        except Exception:
            return None

    @staticmethod
    def generate_auth_tokens(user_id: int):
        """
        Генерация jwt токенов после аутентификации
        :param user_id: id пользователя, прошеднего аутентификацию
        :return:
        """
        access_token = jwt.encode({
            'id': user_id,
            'exp': datetime.now(tz=settings.TIMEZONE) + settings.ACCESS_TOKEN_LIVE_TIME,
            'is_refresh_token': False,
        }, settings.SECRET_KEY, algorithm='HS256')

        refresh_token = jwt.encode({
            'id': user_id,
            'exp': datetime.now(tz=settings.TIMEZONE) + settings.REFRESH_TOKEN_LIVE_TIME,
            'is_refresh_token': True,
        }, settings.SECRET_KEY, algorithm='HS256')

        return access_token, refresh_token

    @staticmethod
    def refresh_auth_tokens(refresh_token: str):
        """
        Обновление jwt токенов
        :param refresh_token: токен обновления
        :return:
        """
        try:
            # пытаемся декодировать токен
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
        except (DecodeError, ExpiredSignatureError):
            raise ValueError('Недействительный токен обновления')

        # проверяем не забанен ли (уже не использован) токен
        is_banned = db.session.query(
            db.session.query(BlackListJWT).filter(
                BlackListJWT.token == refresh_token,
            ).exists()
        ).scalar()

        if not payload['is_refresh_token'] or is_banned:
            raise ValueError('Недействительный токен обновления')

        # помечаем токен как использованный
        db.session.add(
            BlackListJWT(token=refresh_token)
        )
        db.session.commit()

        # генерируем новые токен
        access_token = jwt.encode({
            'id': payload['id'],
            'exp': datetime.now(tz=settings.TIMEZONE) + settings.ACCESS_TOKEN_LIVE_TIME,
            'is_refresh_token': False,
        }, settings.SECRET_KEY, algorithm='HS256')

        refresh_token = jwt.encode({
            'id': payload['id'],
            'exp': datetime.now(tz=settings.TIMEZONE) + settings.REFRESH_TOKEN_LIVE_TIME,
            'is_refresh_token': True,
        }, settings.SECRET_KEY, algorithm='HS256')

        return access_token, refresh_token
