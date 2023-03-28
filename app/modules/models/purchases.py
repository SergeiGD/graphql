from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import ForeignKey
from _decimal import Decimal
from datetime import date
from .base import db
import modules.models.rooms as rooms
import modules.models.orders as orders


# class Purchase(db.Model):
#     __tablename__ = 'purchase'
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     start: Mapped[date]
#     end: Mapped[date]
#     price: Mapped[Decimal] = mapped_column(default=0)
#     prepayment: Mapped[Decimal] = mapped_column(default=0)
#     refund: Mapped[Decimal] = mapped_column(default=0)
#     is_paid: Mapped[bool]
#     is_prepayment_paid: Mapped[bool]
#     is_refund_made: Mapped[bool]
#     is_canceled: Mapped[bool]
#
#     order_id: Mapped[int] = mapped_column(ForeignKey('base_order.id'))
#     order: Mapped['orders.BaseOrder'] = relationship(back_populates='purchases')
#
#     room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
#     room: Mapped['rooms.Room'] = relationship(back_populates='purchases')
#
#     @validates('start', 'end')
#     def validate_dates(self, key, field):
#         if key == 'start' and isinstance(self.start, date):
#             if field >= self.end:
#                 raise ValueError('Начало должно быть раньше конца')
#
#         if key == 'end' and isinstance(self.end, date):
#             if self.start >= field:
#                 raise ValueError('Начало должно быть раньше конца')
#
#         return field
