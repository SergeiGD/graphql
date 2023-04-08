from ..models.base import db
from ..models.groups import Group
from ..models.permissions import Permission


class GroupsManager:
    @staticmethod
    def save_group(group: Group):
        db.session.add(group)
        db.session.commit()

    @staticmethod
    def delete_group(group: Group):
        db.session.delete(group)
        db.session.commit()

    @staticmethod
    def add_permission_to_group(group: Group, permission: Permission):
        db.session.add(group)
        group.permissions.append(permission)
        db.session.commit()

    @staticmethod
    def remove_permission_from_group(group: Group, permission: Permission):
        db.session.add(group)
        group.permissions.remove(permission)
        db.session.commit()
        