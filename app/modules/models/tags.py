from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship, validates
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

    @validates('name')
    def validate_name(self, key, name):
        if db.session.query(
                db.session.query(Tag).filter(
                    Tag.name == name
                ).exists()
        ).scalar():
            raise ValueError('Уже есть тег с таким наименованием')
        return name

