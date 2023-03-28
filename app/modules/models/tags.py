from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Table, ForeignKey
from typing import List
from .base import db
import modules.models.categories as categories


category_tag = Table(
    'category_tag',
    db.metadata,
    Column('tag_id', ForeignKey('tag.id'), primary_key=True),
    Column('category_id', ForeignKey('category.id'), primary_key=True),
)


class Tag(db.Model):
    __tablename__ = 'tag'
    REPR_MODEL_NAME = 'тег'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    categories: Mapped[List['categories.Category']] = relationship(
        secondary=category_tag,
        back_populates='tags',
    )

