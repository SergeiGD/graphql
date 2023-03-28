from datetime import datetime
from _decimal import Decimal
from typing import List
from ..settings import settings
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import ForeignKey
from typing import Optional
from .base import db
import modules.models.orders as orders


class User(db.Model):
    __tablename__ = 'people'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    date_created: Mapped[datetime] = mapped_column(default=datetime.now(tz=settings.TIMEZONE))
    date_deleted: Mapped[Optional[datetime]]
    type: Mapped[str]

    orders: Mapped[List['orders.Order']] = relationship(back_populates='client')

    __mapper_args__ = {
        'polymorphic_abstract': True,
        'polymorphic_on': 'type',
    }

    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError('Неверный формат адреса эл. почты')
        return email


class Client(User):
    __tablename__ = 'client'

    id: Mapped[int] = mapped_column(ForeignKey("people.id"), primary_key=True)
    date_of_birth: Mapped[Optional[datetime]]

    __mapper_args__ = {
        'polymorphic_identity': 'client',
    }


class Worker(User):
    __tablename__ = 'worker'
    id: Mapped[int] = mapped_column(ForeignKey("people.id"), primary_key=True)
    salary: Mapped[Decimal]

    __mapper_args__ = {
        'polymorphic_identity': 'worker',
    }


# class User(db.Model):
#     __tablename__ = 'people'
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     first_name: Mapped[Optional[str]]
#     last_name: Mapped[Optional[str]]
#     email: Mapped[str] = mapped_column(unique=True)
#     password: Mapped[str]
#     date_created: Mapped[datetime] = mapped_column(default=datetime.now(tz=settings.TIMEZONE))
#     date_deleted: Mapped[Optional[datetime]]
#     type: Mapped[str]
#
#     orders: Mapped[List['orders.Order']] = relationship(back_populates='client')
#
#     __mapper_args__ = {
#         'polymorphic_abstract': True,
#         'polymorphic_on': 'type',
#     }
#
#     @validates('email')
#     def validate_email(self, key, email):
#         if '@' not in email:
#             raise ValueError('Неверный формат адреса эл. почты')
#         return email
#
#
# class Client(User):
#     date_of_birth: Mapped[Optional[datetime]]
#
#     __mapper_args__ = {
#         'polymorphic_identity': 'client',
#     }
#
#
# class Worker(User):
#     salary: Mapped[Optional[Decimal]]
#
#     __mapper_args__ = {
#         'polymorphic_identity': 'worker',
#     }
