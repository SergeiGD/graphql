from datetime import datetime
from ..settings import settings
from ..models.base import db
from ..models.rooms import Room
from sqlalchemy import func


class RoomsManager:
    @staticmethod
    def save_room(room: Room):
        db.session.add(room)

        if room.id is None and room.room_number is None:
            current_max = db.session.query(func.max(Room.room_number)).filter(
                Room.date_deleted == None
            ).scalar()
            if current_max is None:
                room.room_number = 1
            else:
                room.room_number = current_max + 1

        db.session.commit()

    @staticmethod
    def delete_room(room: Room):
        db.session.add(room)
        room.date_deleted = datetime.now(tz=settings.TIMEZONE)
        db.session.commit()
