from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates, Session, column_property
from sqlalchemy import ForeignKey, func, select, event
from sqlalchemy.ext.hybrid import hybrid_property
from _decimal import Decimal
from datetime import datetime, date
from ..settings import settings
from .base import db
import modules.models.users as users
import modules.models.rooms as rooms
# import modules.models.purchases as purchases


class Purchase(db.Model):
    __tablename__ = 'purchase'

    id: Mapped[int] = mapped_column(primary_key=True)
    start: Mapped[date]
    end: Mapped[date]
    price: Mapped[Decimal] = mapped_column(default=0)
    prepayment: Mapped[Decimal] = mapped_column(default=0)
    refund: Mapped[Decimal] = mapped_column(default=0)
    is_paid: Mapped[bool] = mapped_column(default=False)
    is_prepayment_paid: Mapped[bool] = mapped_column(default=False)
    is_refund_made: Mapped[bool] = mapped_column(default=False)
    is_canceled: Mapped[bool] = mapped_column(default=False)

    order_id: Mapped[int] = mapped_column(ForeignKey('base_order.id'))
    order: Mapped['BaseOrder'] = relationship(back_populates='purchases')

    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    room: Mapped['rooms.Room'] = relationship(back_populates='purchases')


def validate_dates(mapper, connection, target: Purchase):
    if target.start >= target.end:
        raise ValueError('Начало должно быть раньше конца')


event.listen(Purchase, 'before_insert', validate_dates)
event.listen(Purchase, 'before_update', validate_dates)


class BaseOrder(db.Model):
    __tablename__ = 'base_order'
    REPR_MODEL_NAME = 'заказ'

    id: Mapped[int] = mapped_column(primary_key=True)
    date_created: Mapped[datetime] = mapped_column(default=datetime.now(tz=settings.TIMEZONE))
    type: Mapped[str]

    price = column_property(
        select(func.sum(Purchase.price))
        .where(Purchase.order_id == id)
        .correlate_except(Purchase)
        .scalar_subquery()
    )

    prepayment = column_property(
        select(func.sum(Purchase.prepayment))
        .where(Purchase.order_id == id)
        .correlate_except(Purchase)
        .scalar_subquery()
    )

    purchases: Mapped[List['Purchase']] = relationship(back_populates='order', viewonly=True)

    __mapper_args__ = {
        'polymorphic_abstract': True,
        'polymorphic_on': 'type',
    }


class Order(BaseOrder):
    __tablename__ = 'client_order'
    id: Mapped[int] = mapped_column(ForeignKey("base_order.id"), primary_key=True)

    comment: Mapped[Optional[str]]
    paid: Mapped[Decimal] = mapped_column(default=0)
    refunded: Mapped[Decimal] = mapped_column(default=0)
    date_full_prepayment: Mapped[Optional[datetime]]
    date_full_paid: Mapped[Optional[datetime]]
    date_finished: Mapped[Optional[datetime]]
    date_canceled: Mapped[Optional[datetime]]

    client_id: Mapped[int] = mapped_column(ForeignKey("people.id"))
    client: Mapped['users.User'] = relationship(back_populates='orders')

    __mapper_args__ = {
        'polymorphic_identity': 'order',
    }

    @validates('refunded')
    def validate_refunded(self, key, refunded):
        if refunded < 0:
            raise ValueError('Сумма возврата не должна быть меньше 0')
        return refunded

    @validates('paid')
    def validate_refunded(self, key, paid):
        if paid < 0:
            raise ValueError('Сумма оплаты не должна быть меньше 0')
        return paid


class Cart(BaseOrder):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(ForeignKey("base_order.id"), primary_key=True)
    cart_uuid: Mapped[str] = mapped_column(unique=True)

    __mapper_args__ = {
        'polymorphic_identity': 'cart',
    }

