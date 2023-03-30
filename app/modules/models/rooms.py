from datetime import datetime
from typing import Optional
from .base import db
from ..settings import settings
from sqlalchemy.orm import Mapped, validates, mapped_column, relationship
from sqlalchemy import ForeignKey
import modules.models.categories as categories
import modules.models.orders as orders


class Room(db.Model):
    __tablename__ = 'room'
    REPR_MODEL_NAME = 'комната'

    id: Mapped[int] = mapped_column(primary_key=True)
    room_number: Mapped[int]
    date_created: Mapped[datetime] = mapped_column(default=datetime.now(tz=settings.TIMEZONE))
    date_deleted: Mapped[Optional[datetime]]

    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    category: Mapped['categories.Category'] = relationship(back_populates='rooms')

    purchases: Mapped['orders.Purchase'] = relationship(back_populates='room')

    @validates('room_number')
    def validate_room_number(self, key, room_number):
        if db.session.query(
                Room.query.filter(
                    Room.room_number == room_number,
                    Room.date_deleted == None,
                    Room.id != self.id
                ).exists()
        ).scalar():
            raise ValueError('Уже существует комната с этим номером')

        if room_number <= 0:
            raise ValueError('Номер комнаты не может быть меньше 1')

        return room_number

    @validates('category_id')
    def validate_category_id(self, key, category_id):
        if not db.session.query(
                categories.Category.query.filter(
                    categories.Category.id == category_id,
                    categories.Category.date_deleted == None,
                ).exists()
        ).scalar():
            raise ValueError('Не найдена категория с таким id')

        return category_id


# @event.listens_for(Room, 'before_insert')
# def set_room_number_before_insert(mapper, connect, target: Room):
#     if target.room_number is None:
#         current_max = db.session.query(func.max(Room.room_number)).filter(
#             Room.date_deleted == None
#         ).scalar()
#         if current_max is None:
#             target.room_number = 1
#         else:
#             target.room_number = current_max + 1


