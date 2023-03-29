from datetime import date, timedelta, datetime
from typing import Optional

from ..models.categories import Category
from ..models.rooms import Room
from ..models.tags import Tag
from ..models.base import db
from ..models.orders import Purchase
from ..settings import settings


class CategoriesManager:
    @staticmethod
    def pick_room(category: Category, start: date, end: date, purchase_id: Optional[int] = None):
        rooms = db.session.query(Room).filter(
            Room.date_deleted == None,
            Room.category_id == category.id
        ).with_entities(Room.id).all()
        free_rooms = {item[0] for item in rooms}
        day_to_check = start

        while free_rooms and day_to_check < end:
            busy_rooms = db.session.query(Purchase).filter(
                Purchase.room_id.in_(free_rooms),
                Purchase.is_canceled == False,
                Purchase.start <= day_to_check,
                Purchase.end > day_to_check,
                Purchase.id != purchase_id
            ).with_entities(Purchase.room_id).all()

            free_rooms -= {item[0] for item in busy_rooms}
            day_to_check += timedelta(days=1)

        if not free_rooms:
            return None

        picked_room_id = list(free_rooms)[0]
        return picked_room_id

    @staticmethod
    def save_category(category: Category):
        db.session.add(category)
        db.session.commit()

    @staticmethod
    def delete_category(category: Category):
        db.session.add(category)
        category.date_deleted = datetime.now(tz=settings.TIMEZONE)
        db.session.commit()

    @staticmethod
    def add_tag_to_category(category: Category, tag: Tag):
        db.session.add(category)
        category.tags.append(tag)
        db.session.commit()
