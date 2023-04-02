from ..models.base import db
from ..models.groups import Group
from ..models.users import Worker
from sqlalchemy import inspect
import bcrypt


class WorkersManager:
    @staticmethod
    def save_worker(worker: Worker):
        db.session.add(worker)
        db.session.commit()

    @staticmethod
    def delete_worker(worker: Worker):
        db.session.delete(worker)
        db.session.commit()

    @staticmethod
    def add_group_to_worker(worker: Worker, group: Group):
        db.session.add(worker)
        worker.groups.append(group)
        db.session.commit()

    @staticmethod
    def remove_group_from_worker(worker: Worker, group: Group):
        db.session.commit(worker)
        worker.groups.remove(group)
        db.session.commit()

