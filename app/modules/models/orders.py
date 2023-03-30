from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates, Session, column_property
from sqlalchemy import ForeignKey, func, select, event, case, and_
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.types import DECIMAL
from _decimal import Decimal
from datetime import datetime, date
from ..settings import settings
from .base import db
import modules.models.users as users
import modules.models.rooms as rooms
# import modules.models.purchases as purchases


class Purchase(db.Model):
    __tablename__ = 'purchase'
    REPR_MODEL_NAME = 'покупка'

    id: Mapped[int] = mapped_column(primary_key=True)
    start: Mapped[date]
    end: Mapped[date]
    price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2), default=0)
    prepayment: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2), default=0)
    refund: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2), default=0)
    is_paid: Mapped[bool] = mapped_column(default=False)
    is_prepayment_paid: Mapped[bool] = mapped_column(default=False)
    is_canceled: Mapped[bool] = mapped_column(default=False)

    order_id: Mapped[int] = mapped_column(ForeignKey('base_order.id'))
    order: Mapped['BaseOrder'] = relationship(back_populates='purchases')

    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    room: Mapped['rooms.Room'] = relationship(back_populates='purchases')

    @validates('order_id')
    def validate_order_id(self, key, order_id):
        if not db.session.query(
                Order.query.filter(
                    Order.id == order_id,
                    Order.date_canceled == None,
                    Order.date_finished == None,
                ).exists()
        ).scalar():
            raise ValueError('Не найден активный заказ с таким id')

        return order_id


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
        func.coalesce(
            select(func.sum(
                case(
                    (and_(Purchase.is_canceled == True, Purchase.is_paid == True), Purchase.price - Purchase.refund),
                    (and_(Purchase.is_canceled == True, Purchase.is_paid == False), Purchase.prepayment),
                    else_=Purchase.price
                )
            ))
            .where(Purchase.order_id == id)
            .correlate_except(Purchase)
            .scalar_subquery(),
            0
        )
    )

    prepayment = column_property(
        func.coalesce(
            select(func.sum(Purchase.prepayment))
            .where(Purchase.order_id == id)
            .correlate_except(Purchase)
            .scalar_subquery(),
            0
        )
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
    paid: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2), default=0)
    refunded: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2), default=0)
    date_full_prepayment: Mapped[Optional[datetime]]
    date_full_paid: Mapped[Optional[datetime]]
    date_finished: Mapped[Optional[datetime]]
    date_canceled: Mapped[Optional[datetime]]

    client_id: Mapped[int] = mapped_column(ForeignKey("people.id"))
    client: Mapped['users.User'] = relationship(back_populates='orders')

    __mapper_args__ = {
        'polymorphic_identity': 'order',
    }

    @hybrid_property
    def left_to_pay(self):
        left_to_pay = self.price - self.paid
        if left_to_pay > 0:
            return left_to_pay
        return 0

    @hybrid_property
    def left_to_refund(self):
        """
        Свойство для получения сумму, которую ОСТАЛОСЬ вернуть
        """
        left_to_refund = self.paid - self.price - self.refunded
        if left_to_refund > 0:
            return left_to_refund
        return 0

    @validates('refunded')
    def validate_refunded(self, key, refunded):
        if refunded < 0:
            raise ValueError('Сумма возврата не должна быть меньше 0')
        if refunded > self.paid:
            raise ValueError('Сумма возврата не должна быть больше суммы оплаты')
        return refunded

    @validates('paid')
    def validate_refunded(self, key, paid):
        if paid < 0:
            raise ValueError('Сумма оплаты не должна быть меньше 0')
        if paid < self.refunded:
            raise ValueError('Сумма оплаты не должна быть меньше суммы возврата')
        return paid

    @validates('category_id')
    def validate_client_id(self, key, client_id):
        if not db.session.query(
                users.User.query.filter(
                    users.User.id == client_id,
                    users.User.date_deleted == None,
                ).exists()
        ).scalar():
            raise ValueError('Не найден клиент с таким id')

        return client_id


class Cart(BaseOrder):
    __tablename__ = 'cart'
    REPR_MODEL_NAME = 'корзина'

    id: Mapped[int] = mapped_column(ForeignKey("base_order.id"), primary_key=True)
    cart_uuid: Mapped[str] = mapped_column(unique=True)

    __mapper_args__ = {
        'polymorphic_identity': 'cart',
    }

