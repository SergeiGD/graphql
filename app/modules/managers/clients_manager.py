from datetime import datetime
from ..models.base import db
from ..models.users import Client, User
from ..models.tokens import Token, TokenType
from ..settings import settings
from ..utils.email_sender import send_email
import uuid
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

