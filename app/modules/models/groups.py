from typing import List

from .base import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column
import modules.models.users as users
# from modules.models.users import user_group
import modules.models.permissions as permission


group_permission = Table(
    'group_permission',
    db.metadata,
    Column('group_id', ForeignKey('group.id'), primary_key=True),
    Column('permission_id', ForeignKey('permission.id'), primary_key=True),
)


class Group(db.Model):
    __tablename__ = 'group'
    REPR_MODEL_NAME = 'группа'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    permissions: Mapped[List['permission.Permission']] = relationship(
        secondary=group_permission,
    )

    users: Mapped[List['users.User']] = relationship(
        secondary='user_group',
        back_populates='groups',
    )


