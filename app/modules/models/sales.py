from datetime import datetime
from ..settings import settings
from sqlalchemy.orm import Mapped, relationship, mapped_column, validates
from typing import List, Optional
from .base import db
from sqlalchemy import Column, Table, ForeignKey
import modules.models.categories as categories


category_sale = Table(
    'category_sale',
    db.metadata,
    Column('sale_id', ForeignKey('sale.id'), primary_key=True),
    Column('category_id', ForeignKey('category.id'), primary_key=True),
)


class Sale(db.Model):
    __tablename__ = 'sale'
    REPR_MODEL_NAME = 'скидка'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    discount: Mapped[float]
    image_path: Mapped[str]
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]
    date_created: Mapped[datetime] = mapped_column(default=datetime.now(tz=settings.TIMEZONE))
    date_deleted: Mapped[Optional[datetime]]

    categories: Mapped[List['categories.Category']] = relationship(
        secondary=category_sale,
        back_populates='sales',
    )

    @validates('discount')
    def validate_discount(self, key, discount):
        if discount <= 0 or discount >= 100:
            raise ValueError('Размер скидки должен быть больше 0 и меньше 100')
        return discount

    @validates('start_date', 'end_date')
    def validate_dates(self, key, field):
        if key == 'start_date' and isinstance(self.start_date, datetime):
            if field >= self.end_date:
                raise ValueError('Начало должно быть раньше конца')

        if key == 'end_date' and isinstance(self.end_date, datetime):
            if self.start_date >= field:
                raise ValueError('Начало должно быть раньше конца')

        return field
