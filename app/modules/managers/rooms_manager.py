from ..models.base import db
from ..models.rooms import Room
from ..models.categories import Category
from sqlalchemy import func


class RoomsManager:
    @staticmethod
    def save_room(room: Room):
        db.session.add(room)

        if room.id is None and room.room_number is None:
            with db.session.no_autoflush:
                current_max = db.session.query(func.max(Room.room_number)).filter(
                    Room.date_deleted == None
                ).scalar()
                if current_max is None:
                    room.room_number = 1
                else:
                    room.room_number = current_max + 1

        db.session.commit()
