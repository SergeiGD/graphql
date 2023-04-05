import math
from datetime import datetime
from typing import Optional

from sqlalchemy import desc
from ..models.base import db
from ..models.sales import Sale
from ..settings import settings
from ..utils.file_manager import FileManager
from werkzeug.datastructures import FileStorage


class SalesManager:
    @staticmethod
    def save_sale(sale: Sale, file: Optional[FileStorage]):
        db.session.add(sale)
        if file is not None:
            sale.image_path = FileManager.save_file(file, sale.image_path)
        db.session.commit()

    @staticmethod
    def delete_sale(sale: Sale):
        db.session.add(sale)
        sale.date_deleted = datetime.now(tz=settings.TIMEZONE)
        FileManager.delete_file(sale.image_path)
        db.session.commit()

    @staticmethod
    def filter(filter: dict):
        sales = db.session.query(Sale).filter_by(date_deleted=None)
        if 'id' in filter:
            sales = sales.filter(
                Sale.id == filter['id']
            )
        if 'name' in filter:
            sales = sales.filter(
                Sale.name.icontains(filter['name'])
            )
        if 'discount_from' in filter:
            sales = sales.filter(
                Sale.discount >= filter['discount_from']
            )
        if 'discount_until' in filter:
            sales = sales.filter(
                Sale.discount <= filter['discount_until']
            )
        if 'date_from' in filter:
            sales = sales.filter(
                Sale.start_date >= filter['date_from']
            )
        if 'date_until' in filter:
            sales = sales.filter(
                Sale.end_date <= filter['date_until']
            )

        if filter['desc']:
            sales = sales.order_by(desc(filter['sort_by']))
        else:
            sales = sales.order_by(filter['sort_by'])

        if filter['page_size'] < 1 or filter['page'] < 1:
            raise ValueError('страница и кол-во выводимых элментов не может быть меньше 1')

        limit = filter['page_size']
        offset = filter['page_size'] * (filter['page'] - 1)
        pages_count = math.ceil(sales.count() / filter['page_size'])
        return sales.offset(offset).limit(limit), pages_count
