import uuid
from .base import db
from sqlalchemy.orm import Mapped, mapped_column


class BlackListJWT(db.Model):
    __tablename__ = 'black_list_jwt'
    REPR_MODEL_NAME = 'использованный токен'

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str]
