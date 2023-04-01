from typing import List, re

from ..models.base import db
from ..models.users import User
from ..models.permissions import Permission
from ..models.groups import Group, group_permission
from ..models.users import user_group
from bcrypt import checkpw


class UsersManager:
    @staticmethod
    def check_password(login: str, password: str):
        user = db.session.query(User).filter_by(email=login).first()
        if user is None or not checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise ValueError('Пользователь с таким логином и паролем не найден')
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
