from datetime import datetime
from ..models.base import db
from ..models.sales import Sale
from ..settings import settings


class SalesManager:
    @staticmethod
    def save_sale(sale: Sale):
        db.session.add(sale)
        db.session.commit()

    @staticmethod
    def delete_sale(sale: Sale):
        db.session.add(sale)
        sale.date_deleted = datetime.now(tz=settings.TIMEZONE)
        db.session.commit()
