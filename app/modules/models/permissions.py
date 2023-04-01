from .base import db
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import ForeignKey
# import modules.models.users as user


class Permission(db.Model):
    __tablename__ = 'permission'
    REPR_MODEL_NAME = 'разрешение'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    code: Mapped[str] = mapped_column(unique=True)

    # category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    # category: Mapped['categories.Category'] = relationship(back_populates='photos')

