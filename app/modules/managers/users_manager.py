from ..models.base import db
from ..models.users import User
from bcrypt import checkpw


class UsersManager:
    @staticmethod
    def check_password(login: str, password: str):
        user = db.session.query(User).filter_by(email=login).first()
        print(password)
        print(user.password)
        if user is None or not checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise ValueError('Пользователь с таким логином и паролем не найден')
        return user

