from datetime import datetime
from ..models.base import db
from ..models.users import Client, User
from ..settings import settings
import bcrypt


class ClientsManager:
    """
    Класс для управления клиентами
    """
    @staticmethod
    def save_client(client: Client):
        db.session.add(client)
        db.session.commit()

    @staticmethod
    def delete_client(client: Client):
        db.session.add(client)
        client.date_deleted = datetime.now(tz=settings.TIMEZONE)
        db.session.commit()

    @staticmethod
    def register_client(client: Client):
        """
        Регистрация клиентов
        :param client: клиент, которого нужно зарегистрировать
        :return:
        """
        # проверяем есть ли зарегестрированный (с паролем) пользователь с такой эл. почтой
        if db.session.query(
            db.session.query(User).filter(
                User.email == client.email,
                User.password != None,
            ).exists()
        ).scalar():
            raise ValueError('Пользователь с таким адресом эл. почты уже ререгестрирован')

        # хэшируем пароль (bcrypt сохраняет соль прямо в хэш)
        hashed_password = bcrypt.hashpw(client.password.encode('utf-8'), bcrypt.gensalt())

        unregistered_client = db.session.query(Client).filter(
            Client.email == client.email,
        ).first()
        if unregistered_client is not None:
            # если есть созданный, но не зарегестрированный (без пароля) клиент, то устанавливаем регестрируем его
            client = unregistered_client

        client.password = hashed_password.decode('utf8')
        db.session.add(client)
        db.session.commit()
        return client
