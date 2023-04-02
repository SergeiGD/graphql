from typing import List, re
from datetime import datetime
from ..models.base import db
from ..models.users import User
from ..models.permissions import Permission
from ..models.groups import group_permission
from ..models.users import user_group
import bcrypt
from ..models.tokens import Token, TokenType
from ..settings import settings
from ..utils.email_sender import send_email


class UsersManager:
    @staticmethod
    def authenticate_user(login: str, password: str):
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

        # генерируем токен подтверждения регистрации
        confirm_token = Token(user=user, token_type=TokenType.register)
        db.session.add(confirm_token)
        db.session.commit()
        confirm_link = f'{settings.SITE_URL}/confirm_registration/{confirm_token.token}'

        # отправляем письмо
        send_email(
            subject='Подтверждение регистрации',
            content=f'Для подтверждения регистрации перейдите по следующей ссылке: \n {confirm_link}',
            send_to=user.email,
        )
        return user, confirm_token.token

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
        reset_token = Token(user=user, token_type=TokenType.reset)
        db.session.add(reset_token)
        db.session.commit()
        confirm_link = f'{settings.SITE_URL}/reset_password/{reset_token.token}'

        # отправляем письмо
        send_email(
            subject='Сброс пароля',
            content=f'Для сброса пароля перейдите по следующей ссылке: \n {confirm_link}',
            send_to=user.email,
        )
        return user, reset_token.token

    @staticmethod
    def confirm_reset(token: Token, password: str):
        db.session.add(token)
        db.session.add(token.user)
        token.user.is_confirmed = True
        # отмечаем токен как использованный
        token.is_used = True
        # хэшируем пароль
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        token.user.password = hashed_password.decode('utf8')
        db.session.commit()

    @staticmethod
    def check_token(token: str, token_type: TokenType):
        """
        Проверка активности токена
        :param token: токен
        :param token_type: тип токена
        :return:
        """
        try:
            return db.session.query(Token).filter(
                Token.token == token,
                Token.token_type == token_type,
                Token.expires > datetime.now(tz=settings.TIMEZONE),
            ).first()
        except Exception:
            return None
