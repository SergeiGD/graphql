from datetime import datetime
from ..models.base import db
from ..models.users import Client
from ..settings import settings


class ClientsManager:
    @staticmethod
    def save_client(client: Client):
        db.session.add(client)
        db.session.commit()

    @staticmethod
    def delete_client(client: Client):
        db.session.add(client)
        client.date_deleted = datetime.now(tz=settings.TIMEZONE)
        db.session.commit()
