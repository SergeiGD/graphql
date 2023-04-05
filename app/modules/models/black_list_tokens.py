from datetime import datetime
from .base import db
from sqlalchemy.orm import Mapped, mapped_column
from ..settings import settings


class BlackListJWT(db.Model):
    __tablename__ = 'black_list_jwt'
    REPR_MODEL_NAME = 'использованный токен'

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(index=True)
